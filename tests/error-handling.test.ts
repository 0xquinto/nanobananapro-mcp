// tests/error-handling.test.ts
import { describe, test, expect, mock, beforeEach } from "bun:test";

// Mock @google/genai
const mockGenerateContent = mock();
mock.module("@google/genai", () => ({
  GoogleGenAI: mock(() => ({
    models: { generateContent: mockGenerateContent },
    chats: { create: mock() },
  })),
}));

import { GeminiImageClient } from "../src/client";

describe("error propagation", () => {
  beforeEach(() => { mockGenerateContent.mockReset(); });

  test("API errors propagate to caller", async () => {
    process.env.GEMINI_API_KEY = "test-key";

    const apiError = new Error("400 Bad Request");
    (apiError as any).status = 400;
    mockGenerateContent.mockRejectedValueOnce(apiError);

    const client = new GeminiImageClient();
    expect(client.generateImage("test prompt")).rejects.toThrow("400 Bad Request");
  });

  test("retryable errors are retried before propagating", async () => {
    process.env.GEMINI_API_KEY = "test-key";

    const retryableError = new Error("Service Unavailable");
    (retryableError as any).status = 503;
    // Fail twice with 503, then succeed
    mockGenerateContent
      .mockRejectedValueOnce(retryableError)
      .mockRejectedValueOnce(retryableError)
      .mockResolvedValueOnce({
        candidates: [{ content: { parts: [{ text: "ok" }] } }],
      });

    const client = new GeminiImageClient();
    // Default retry config has 2s initial delay with jitter, so this needs a longer timeout
    const result = await client.generateImage("test prompt");
    expect(result.text).toBe("ok");
    expect(mockGenerateContent).toHaveBeenCalledTimes(3);
  }, 15000);
});
