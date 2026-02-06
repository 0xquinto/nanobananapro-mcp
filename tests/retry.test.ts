// tests/retry.test.ts
import { describe, test, expect, mock } from "bun:test";
import {
  RetryConfig,
  DEFAULT_RETRY_CONFIG,
  isRetryableError,
  withRetry,
} from "../src/retry";

describe("RetryConfig", () => {
  test("DEFAULT_RETRY_CONFIG has correct defaults", () => {
    expect(DEFAULT_RETRY_CONFIG.enabled).toBe(true);
    expect(DEFAULT_RETRY_CONFIG.initialDelay).toBe(2.0);
    expect(DEFAULT_RETRY_CONFIG.maxDelay).toBe(60.0);
    expect(DEFAULT_RETRY_CONFIG.multiplier).toBe(2.0);
    expect(DEFAULT_RETRY_CONFIG.timeout).toBe(180.0);
  });
});

describe("isRetryableError", () => {
  // @google/genai SDK errors have a numeric `status` property (HTTP code)
  function apiError(status: number, message: string): Error {
    const err = new Error(message);
    (err as any).status = status;
    return err;
  }

  test("503 service unavailable is retryable", () => {
    expect(isRetryableError(apiError(503, "Service Unavailable"))).toBe(true);
  });

  test("429 rate limit is retryable", () => {
    expect(isRetryableError(apiError(429, "Resource Exhausted"))).toBe(true);
  });

  test("500 internal error is retryable", () => {
    expect(isRetryableError(apiError(500, "Internal Server Error"))).toBe(true);
  });

  test("400 bad request is not retryable", () => {
    expect(isRetryableError(apiError(400, "Bad Request"))).toBe(false);
  });

  test("generic error without status is not retryable", () => {
    expect(isRetryableError(new Error("Something else"))).toBe(false);
  });

  test("falls back to message matching when no status", () => {
    expect(isRetryableError(new Error("RESOURCE_EXHAUSTED"))).toBe(true);
    expect(isRetryableError(new Error("UNAVAILABLE: Model overloaded"))).toBe(true);
  });
});

describe("withRetry", () => {
  test("returns result on first success", async () => {
    const fn = mock(() => Promise.resolve("ok"));
    const result = await withRetry(fn);
    expect(result).toBe("ok");
    expect(fn).toHaveBeenCalledTimes(1);
  });

  test("retries on retryable error then succeeds", async () => {
    let calls = 0;
    const fn = mock(async () => {
      calls++;
      if (calls === 1) {
        const err = new Error("Service Unavailable");
        (err as any).status = 503;
        throw err;
      }
      return "ok";
    });
    const config: RetryConfig = {
      enabled: true,
      initialDelay: 0.01,
      maxDelay: 0.1,
      multiplier: 2.0,
      timeout: 5.0,
    };
    const result = await withRetry(fn, config);
    expect(result).toBe("ok");
    expect(fn).toHaveBeenCalledTimes(2);
  });

  test("throws immediately on non-retryable error", async () => {
    const err = new Error("Bad Request");
    (err as any).status = 400;
    const fn = mock(() => Promise.reject(err));
    const config: RetryConfig = {
      enabled: true,
      initialDelay: 0.01,
      maxDelay: 0.1,
      multiplier: 2.0,
      timeout: 5.0,
    };
    expect(withRetry(fn, config)).rejects.toThrow("Bad Request");
  });

  test("disabled config runs function once without retry", async () => {
    const err = new Error("Service Unavailable");
    (err as any).status = 503;
    const fn = mock(() => Promise.reject(err));
    const config: RetryConfig = { ...DEFAULT_RETRY_CONFIG, enabled: false };
    expect(withRetry(fn, config)).rejects.toThrow("Service Unavailable");
    expect(fn).toHaveBeenCalledTimes(1);
  });
});
