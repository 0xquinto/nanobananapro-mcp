// tests/client.test.ts
import { describe, test, expect, mock, beforeEach, afterEach } from "bun:test";

// Mock @google/genai before importing client
const mockGenerateContent = mock();
const mockGoogleGenAI = mock(() => ({
  models: { generateContent: mockGenerateContent },
  chats: { create: mock() },
}));

mock.module("@google/genai", () => ({
  GoogleGenAI: mockGoogleGenAI,
}));

import { GeminiImageClient, ImageGenerationResult } from "../src/client";

describe("GeminiImageClient", () => {
  const originalEnv = process.env.GEMINI_API_KEY;

  afterEach(() => {
    if (originalEnv) {
      process.env.GEMINI_API_KEY = originalEnv;
    } else {
      delete process.env.GEMINI_API_KEY;
    }
    mockGenerateContent.mockReset();
  });

  test("requires API key", () => {
    delete process.env.GEMINI_API_KEY;
    expect(() => new GeminiImageClient()).toThrow("GEMINI_API_KEY");
  });

  test("initializes with env key", () => {
    process.env.GEMINI_API_KEY = "test-key";
    const client = new GeminiImageClient();
    expect(client).toBeDefined();
  });

  test("initializes with explicit key", () => {
    delete process.env.GEMINI_API_KEY;
    const client = new GeminiImageClient("explicit-key");
    expect(client).toBeDefined();
  });
});

describe("ImageGenerationResult.fromResponse", () => {
  test("extracts text from response", () => {
    const response = {
      candidates: [
        {
          content: {
            parts: [{ text: "Generated description" }],
          },
        },
      ],
    };
    const result = ImageGenerationResult.fromResponse(response);
    expect(result.text).toBe("Generated description");
    expect(result.imageData).toBeNull();
  });

  test("extracts image from response", () => {
    const base64Data = Buffer.from("fake_image_data").toString("base64");
    const response = {
      candidates: [
        {
          content: {
            parts: [{ inlineData: { data: base64Data, mimeType: "image/png" } }],
          },
        },
      ],
    };
    const result = ImageGenerationResult.fromResponse(response);
    expect(result.text).toBeNull();
    expect(result.imageData).toEqual(Buffer.from("fake_image_data"));
    expect(result.mimeType).toBe("image/png");
  });

  test("extracts both text and image", () => {
    const base64Data = Buffer.from("img").toString("base64");
    const response = {
      candidates: [
        {
          content: {
            parts: [
              { text: "Here's your image" },
              { inlineData: { data: base64Data, mimeType: "image/png" } },
            ],
          },
        },
      ],
    };
    const result = ImageGenerationResult.fromResponse(response);
    expect(result.text).toBe("Here's your image");
    expect(result.imageData).toEqual(Buffer.from("img"));
  });
});

describe("GeminiImageClient.generateImage", () => {
  beforeEach(() => { mockGenerateContent.mockReset(); });
  test("calls API and returns result", async () => {
    process.env.GEMINI_API_KEY = "test-key";
    const base64Data = Buffer.from("generated").toString("base64");
    mockGenerateContent.mockResolvedValueOnce({
      candidates: [
        {
          content: {
            parts: [
              { text: "A sunset" },
              { inlineData: { data: base64Data, mimeType: "image/png" } },
            ],
          },
        },
      ],
    });

    const client = new GeminiImageClient();
    const result = await client.generateImage("a sunset over mountains");

    expect(result.text).toBe("A sunset");
    expect(result.imageData).toEqual(Buffer.from("generated"));
    expect(mockGenerateContent).toHaveBeenCalledTimes(1);
  });
});

describe("GeminiImageClient.editImage", () => {
  beforeEach(() => { mockGenerateContent.mockReset(); });
  test("loads image and calls API", async () => {
    process.env.GEMINI_API_KEY = "test-key";
    // Create a temp image file
    const tmpFile = `/tmp/test-client-edit-${Date.now()}.png`;
    require("fs").writeFileSync(tmpFile, Buffer.from("fake_png"));

    mockGenerateContent.mockResolvedValueOnce({
      candidates: [
        {
          content: { parts: [{ text: "Edited" }] },
        },
      ],
    });

    const client = new GeminiImageClient();
    const result = await client.editImage("make it brighter", tmpFile);

    expect(result.text).toBe("Edited");
    expect(mockGenerateContent).toHaveBeenCalledTimes(1);

    // Verify image was included in contents
    const callArgs = mockGenerateContent.mock.calls[0][0];
    expect(callArgs.contents).toBeArrayOfSize(2);

    require("fs").unlinkSync(tmpFile);
  });
});

describe("GeminiImageClient.composeImages", () => {
  test("rejects more than 14 images", async () => {
    process.env.GEMINI_API_KEY = "test-key";
    const client = new GeminiImageClient();
    const paths = Array.from({ length: 15 }, (_, i) => `/tmp/img${i}.png`);
    expect(client.composeImages("combine", paths)).rejects.toThrow("Maximum 14");
  });
});

describe("GeminiImageClient.searchGroundedImage", () => {
  beforeEach(() => { mockGenerateContent.mockReset(); });
  test("calls API with google search tool", async () => {
    process.env.GEMINI_API_KEY = "test-key";
    mockGenerateContent.mockResolvedValueOnce({
      candidates: [
        {
          content: { parts: [{ text: "Grounded result" }] },
          groundingMetadata: { searchQueries: ["test"] },
        },
      ],
    });

    const client = new GeminiImageClient();
    const result = await client.searchGroundedImage("current weather");

    expect(result.text).toBe("Grounded result");
    const callArgs = mockGenerateContent.mock.calls[0][0];
    expect(callArgs.config.tools).toBeDefined();
  });
});
