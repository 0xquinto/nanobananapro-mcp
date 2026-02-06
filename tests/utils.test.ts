// tests/utils.test.ts
import { describe, test, expect } from "bun:test";
import {
  encodeImageToBase64,
  decodeBase64ToBytes,
  validateAspectRatio,
  validateResolution,
  validateModel,
  validateSeed,
  getMimeType,
  VALID_ASPECT_RATIOS,
  VALID_RESOLUTIONS,
  VALID_MODELS,
  MODEL_ALIASES,
  MAX_SEED_VALUE,
} from "../src/utils";

describe("encodeImageToBase64", () => {
  test("encodes bytes to base64 string", () => {
    const bytes = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
    const result = encodeImageToBase64(bytes);
    expect(typeof result).toBe("string");
    expect(Buffer.from(result, "base64")).toEqual(bytes);
  });

  test("encodes from file path", () => {
    const tmpFile = `/tmp/test-utils-${Date.now()}.png`;
    const data = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x74, 0x65, 0x73, 0x74]);
    require("fs").writeFileSync(tmpFile, data);
    const result = encodeImageToBase64(tmpFile);
    expect(typeof result).toBe("string");
    expect(Buffer.from(result, "base64")).toEqual(data);
    require("fs").unlinkSync(tmpFile);
  });
});

describe("decodeBase64ToBytes", () => {
  test("decodes base64 string to buffer", () => {
    const original = Buffer.from("test_image_data");
    const encoded = original.toString("base64");
    const result = decodeBase64ToBytes(encoded);
    expect(result).toEqual(original);
  });
});

describe("validateAspectRatio", () => {
  test.each(["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"])(
    "accepts valid ratio: %s",
    (ratio) => {
      expect(validateAspectRatio(ratio)).toBe(ratio);
    }
  );

  test("rejects invalid ratio", () => {
    expect(() => validateAspectRatio("7:3")).toThrow("Invalid aspect ratio");
  });

  test("returns default for null", () => {
    expect(validateAspectRatio(null)).toBe("1:1");
  });
});

describe("validateResolution", () => {
  test.each(["1K", "2K", "4K"])("accepts valid resolution: %s", (res) => {
    expect(validateResolution(res, "gemini-3-pro-image-preview")).toBe(res);
  });

  test("rejects invalid resolution", () => {
    expect(() => validateResolution("8K", "gemini-3-pro-image-preview")).toThrow(
      "Invalid resolution"
    );
  });

  test("returns default for null", () => {
    expect(validateResolution(null, "gemini-3-pro-image-preview")).toBe("1K");
  });
});

describe("validateModel", () => {
  test("VALID_MODELS only contains pro", () => {
    expect(VALID_MODELS).toEqual(["gemini-3-pro-image-preview"]);
  });

  test("MODEL_ALIASES maps to pro", () => {
    expect(MODEL_ALIASES["pro"]).toBe("gemini-3-pro-image-preview");
    expect(MODEL_ALIASES["nano-banana-pro"]).toBe("gemini-3-pro-image-preview");
    expect(MODEL_ALIASES["flash"]).toBeUndefined();
  });

  test("accepts pro aliases", () => {
    expect(validateModel("pro")).toBe("gemini-3-pro-image-preview");
    expect(validateModel("nano-banana-pro")).toBe("gemini-3-pro-image-preview");
    expect(validateModel("gemini-3-pro-image-preview")).toBe("gemini-3-pro-image-preview");
  });

  test("rejects flash", () => {
    expect(() => validateModel("flash")).toThrow("Invalid model");
    expect(() => validateModel("gemini-2.5-flash-image")).toThrow("Invalid model");
  });

  test("rejects unknown model", () => {
    expect(() => validateModel("gpt-4")).toThrow("Invalid model");
  });
});

describe("validateSeed", () => {
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

describe("getMimeType", () => {
  test("returns correct mime types", () => {
    expect(getMimeType("photo.png")).toBe("image/png");
    expect(getMimeType("photo.jpg")).toBe("image/jpeg");
    expect(getMimeType("photo.jpeg")).toBe("image/jpeg");
    expect(getMimeType("photo.gif")).toBe("image/gif");
    expect(getMimeType("photo.webp")).toBe("image/webp");
  });

  test("defaults to image/png for unknown", () => {
    expect(getMimeType("photo.bmp")).toBe("image/png");
  });
});
