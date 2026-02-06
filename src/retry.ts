// src/retry.ts
export interface RetryConfig {
  enabled: boolean;
  initialDelay: number;
  maxDelay: number;
  multiplier: number;
  timeout: number;
}

export const DEFAULT_RETRY_CONFIG: RetryConfig = {
  enabled: true,
  initialDelay: 2.0,
  maxDelay: 60.0,
  multiplier: 2.0,
  timeout: 180.0,
};

const RETRYABLE_STATUS_CODES = new Set([429, 500, 503]);

export function isRetryableError(error: unknown): boolean {
  if (!(error instanceof Error)) return false;
  // @google/genai SDK errors have a numeric `status` property
  const status = (error as any).status;
  if (typeof status === "number") {
    return RETRYABLE_STATUS_CODES.has(status);
  }
  // Fallback: match known error strings for non-SDK errors
  const msg = error.message.toUpperCase();
  return msg.includes("RESOURCE_EXHAUSTED") || msg.includes("UNAVAILABLE");
}

function sleep(seconds: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, seconds * 1000));
}

export async function withRetry<T>(
  fn: () => Promise<T>,
  config: RetryConfig = DEFAULT_RETRY_CONFIG
): Promise<T> {
  if (!config.enabled) return fn();

  const deadline = Date.now() + config.timeout * 1000;
  let delay = config.initialDelay;

  while (true) {
    try {
      return await fn();
    } catch (error) {
      if (!isRetryableError(error)) throw error;
      if (Date.now() + delay * 1000 > deadline) throw error;

      console.error(
        `Retrying after ${(error as Error).constructor.name}: ${(error as Error).message}`
      );
      // Add jitter (±25%) to avoid thundering herd
      const jitter = delay * (0.75 + Math.random() * 0.5);
      await sleep(jitter);
      delay = Math.min(delay * config.multiplier, config.maxDelay);
    }
  }
}
