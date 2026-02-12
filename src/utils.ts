// src/utils.ts
import * as fs from "node:fs";
import * as path from "node:path";

export const VALID_ASPECT_RATIOS = [
  "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9",
];

export const VALID_RESOLUTIONS = ["1K", "2K", "4K"];

export const MAX_SEED_VALUE = 2147483647; // 2^31 - 1

export const MODEL_ALIASES: Record<string, string> = {
  pro: "gemini-3-pro-image-preview",
  "nano-banana-pro": "gemini-3-pro-image-preview",
};

export const VALID_MODELS = ["gemini-3-pro-image-preview"];

export const SAFETY_THRESHOLDS: Record<string, string> = {
  block_none: "BLOCK_NONE",
  block_low: "BLOCK_LOW_AND_ABOVE",
  block_medium: "BLOCK_MEDIUM_AND_ABOVE",
  block_high: "BLOCK_ONLY_HIGH",
};

export const HARM_CATEGORIES = [
  "HARM_CATEGORY_HARASSMENT",
  "HARM_CATEGORY_HATE_SPEECH",
  "HARM_CATEGORY_SEXUALLY_EXPLICIT",
  "HARM_CATEGORY_DANGEROUS_CONTENT",
] as const;

export function encodeImageToBase64(image: Buffer | string): string {
  if (typeof image === "string") {
    const imageBytes = fs.readFileSync(image);
    return imageBytes.toString("base64");
  }
  return image.toString("base64");
}

export function decodeBase64ToBytes(data: string): Buffer {
  return Buffer.from(data, "base64");
}

export function validateAspectRatio(ratio: string | null): string {
  if (ratio === null) return "1:1";
  if (!VALID_ASPECT_RATIOS.includes(ratio)) {
    throw new Error(
      `Invalid aspect ratio: ${ratio}. Must be one of: ${VALID_ASPECT_RATIOS.join(", ")}`
    );
  }
  return ratio;
}

export function validateResolution(resolution: string | null, model: string): string {
  if (resolution === null) return "1K";
  if (!VALID_RESOLUTIONS.includes(resolution)) {
    throw new Error(
      `Invalid resolution: ${resolution}. Must be one of: ${VALID_RESOLUTIONS.join(", ")}`
    );
  }
  return resolution;
}

export function validateModel(model: string): string {
  const lower = model.toLowerCase();
  if (lower in MODEL_ALIASES) return MODEL_ALIASES[lower];
  if (VALID_MODELS.includes(model)) return model;
  throw new Error(
    `Invalid model: ${model}. Must be one of: ${VALID_MODELS.join(", ")} or aliases: ${Object.keys(MODEL_ALIASES).join(", ")}`
  );
}

export function validateSeed(seed: number | null): number | null {
  if (seed === null) return null;
  if (typeof seed !== "number" || !Number.isInteger(seed)) {
    throw new Error(`Seed must be an integer, got ${typeof seed}`);
  }
  if (seed < 0) throw new Error("Seed must be non-negative");
  if (seed > MAX_SEED_VALUE) throw new Error(`Seed must not exceed ${MAX_SEED_VALUE}`);
  return seed;
}

export function validateSafetyThreshold(threshold: string | null): string | null {
  if (threshold === null) return null;
  if (!(threshold in SAFETY_THRESHOLDS)) {
    throw new Error(
      `Invalid safety threshold: ${threshold}. Must be one of: ${Object.keys(SAFETY_THRESHOLDS).join(", ")}`
    );
  }
  return SAFETY_THRESHOLDS[threshold];
}

export function buildSafetySettings(apiThreshold: string): Array<{ category: string; threshold: string }> {
  return HARM_CATEGORIES.map((category) => ({
    category,
    threshold: apiThreshold,
  }));
}

export function getMimeType(filePath: string): string {
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes: Record<string, string> = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
  };
  return mimeTypes[ext] || "image/png";
}
