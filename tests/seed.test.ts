// tests/seed.test.ts
import { describe, test, expect, mock, beforeEach } from "bun:test";
import { validateSeed } from "../src/utils";

// Mock @google/genai to verify seed flows through
const mockGenerateContent = mock();
mock.module("@google/genai", () => ({
  GoogleGenAI: mock(() => ({
    models: { generateContent: mockGenerateContent },
    chats: { create: mock() },
  })),
}));

import { GeminiImageClient } from "../src/client";

describe("seed validation", () => {
  test("accepts valid integers", () => {
    expect(validateSeed(12345)).toBe(12345);
    expect(validateSeed(0)).toBe(0);
    expect(validateSeed(2147483647)).toBe(2147483647);
  });

  test("accepts null", () => {
    expect(validateSeed(null)).toBeNull();
  });

  test("rejects negative", () => {
    expect(() => validateSeed(-1)).toThrow("non-negative");
  });

  test("rejects too large", () => {
    expect(() => validateSeed(2147483648)).toThrow("exceed");
  });

  test("rejects non-integer", () => {
    expect(() => validateSeed("12345" as any)).toThrow("integer");
    expect(() => validateSeed(3.14)).toThrow("integer");
  });
});

describe("seed parameter integration", () => {
  beforeEach(() => { mockGenerateContent.mockReset(); });

  test("generate_image accepts seed without error", async () => {
    process.env.GEMINI_API_KEY = "test-key";
    mockGenerateContent.mockResolvedValueOnce({
      candidates: [{ content: { parts: [{ text: "ok" }] } }],
    });

    const client = new GeminiImageClient();
    const result = await client.generateImage("test", "pro", "1:1", "1K", 42);
    expect(result.text).toBe("ok");
  });

  test("seed is optional (null)", async () => {
    process.env.GEMINI_API_KEY = "test-key";
    mockGenerateContent.mockResolvedValueOnce({
      candidates: [{ content: { parts: [{ text: "ok" }] } }],
    });

    const client = new GeminiImageClient();
    const result = await client.generateImage("test", "pro", "1:1", "1K", null);
    expect(result.text).toBe("ok");
  });

  test("edit_image accepts seed", async () => {
    process.env.GEMINI_API_KEY = "test-key";
    const tmpFile = `/tmp/test-seed-edit-${Date.now()}.png`;
    require("fs").writeFileSync(tmpFile, Buffer.from("fake_png"));
    mockGenerateContent.mockResolvedValueOnce({
      candidates: [{ content: { parts: [{ text: "edited" }] } }],
    });

    const client = new GeminiImageClient();
    const result = await client.editImage("brighten", tmpFile, "pro", "1:1", "1K", 123);
    expect(result.text).toBe("edited");
    require("fs").unlinkSync(tmpFile);
  });
});
