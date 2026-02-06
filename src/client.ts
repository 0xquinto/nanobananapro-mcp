// src/client.ts
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";
import {
  encodeImageToBase64,
  getMimeType,
  validateAspectRatio,
  validateModel,
  validateResolution,
  validateSeed,
} from "./utils";
import { withRetry, DEFAULT_RETRY_CONFIG } from "./retry";

export class ImageGenerationResult {
  text: string | null;
  imageData: Buffer | null;
  mimeType: string | null;
  groundingMetadata: unknown | null;

  constructor(
    text: string | null = null,
    imageData: Buffer | null = null,
    mimeType: string | null = null,
    groundingMetadata: unknown | null = null
  ) {
    this.text = text;
    this.imageData = imageData;
    this.mimeType = mimeType;
    this.groundingMetadata = groundingMetadata;
  }

  static fromResponse(response: any): ImageGenerationResult {
    let text: string | null = null;
    let imageData: Buffer | null = null;
    let mimeType: string | null = null;

    const parts = response.candidates?.[0]?.content?.parts ?? [];
    for (const part of parts) {
      if (part.text != null) {
        text = part.text;
      } else if (part.inlineData != null) {
        imageData = Buffer.from(part.inlineData.data, "base64");
        mimeType = part.inlineData.mimeType;
      }
    }

    const grounding = response.candidates?.[0]?.groundingMetadata ?? null;

    return new ImageGenerationResult(text, imageData, mimeType, grounding);
  }
}

export class GeminiImageClient {
  private ai: InstanceType<typeof GoogleGenAI>;

  constructor(apiKey?: string) {
    const key = apiKey || process.env.GEMINI_API_KEY;
    if (!key) {
      throw new Error(
        "GEMINI_API_KEY environment variable is required. Set it or pass apiKey parameter."
      );
    }
    this.ai = new GoogleGenAI({ apiKey: key });
  }

  async generateImage(
    prompt: string,
    model: string = "gemini-3-pro-image-preview",
    aspectRatio: string | null = null,
    resolution: string | null = null,
    seed: number | null = null
  ): Promise<ImageGenerationResult> {
    model = validateModel(model);
    aspectRatio = validateAspectRatio(aspectRatio);
    resolution = validateResolution(resolution, model);
    validateSeed(seed);

    const config: any = {
      responseModalities: ["TEXT", "IMAGE"],
      imageConfig: {
        aspectRatio,
        imageSize: model === "gemini-3-pro-image-preview" ? resolution : undefined,
      },
    };

    const response = await withRetry(() =>
      this.ai.models.generateContent({
        model,
        contents: prompt,
        config,
      })
    );

    return ImageGenerationResult.fromResponse(response);
  }

  async editImage(
    prompt: string,
    imagePath: string,
    model: string = "gemini-3-pro-image-preview",
    aspectRatio: string | null = null,
    resolution: string | null = null,
    seed: number | null = null
  ): Promise<ImageGenerationResult> {
    model = validateModel(model);
    aspectRatio = validateAspectRatio(aspectRatio);
    resolution = validateResolution(resolution, model);
    validateSeed(seed);

    const imageBase64 = encodeImageToBase64(imagePath);
    const imageMimeType = getMimeType(imagePath);

    const config: any = {
      responseModalities: ["TEXT", "IMAGE"],
      imageConfig: {
        aspectRatio,
        imageSize: model === "gemini-3-pro-image-preview" ? resolution : undefined,
      },
    };

    const response = await withRetry(() =>
      this.ai.models.generateContent({
        model,
        contents: [
          { text: prompt },
          { inlineData: { data: imageBase64, mimeType: imageMimeType } },
        ],
        config,
      })
    );

    return ImageGenerationResult.fromResponse(response);
  }

  async composeImages(
    prompt: string,
    imagePaths: string[],
    model: string = "gemini-3-pro-image-preview",
    aspectRatio: string | null = null,
    resolution: string | null = null,
    seed: number | null = null
  ): Promise<ImageGenerationResult> {
    model = validateModel(model);
    aspectRatio = validateAspectRatio(aspectRatio);
    resolution = validateResolution(resolution, model);
    validateSeed(seed);

    if (imagePaths.length > 14) {
      throw new Error(`Maximum 14 images supported, got ${imagePaths.length}`);
    }

    const contents: any[] = [{ text: prompt }];
    for (const p of imagePaths) {
      contents.push({
        inlineData: { data: encodeImageToBase64(p), mimeType: getMimeType(p) },
      });
    }

    const config: any = {
      responseModalities: ["TEXT", "IMAGE"],
      imageConfig: {
        aspectRatio,
        imageSize: model === "gemini-3-pro-image-preview" ? resolution : undefined,
      },
    };

    const response = await withRetry(() =>
      this.ai.models.generateContent({ model, contents, config })
    );

    return ImageGenerationResult.fromResponse(response);
  }

  async searchGroundedImage(
    prompt: string,
    aspectRatio: string | null = null,
    resolution: string | null = null
  ): Promise<ImageGenerationResult> {
    const model = "gemini-3-pro-image-preview";
    aspectRatio = validateAspectRatio(aspectRatio);
    resolution = validateResolution(resolution, model);

    const config: any = {
      responseModalities: ["TEXT", "IMAGE"],
      imageConfig: { aspectRatio, imageSize: resolution },
      tools: [{ googleSearch: {} }],
    };

    const response = await withRetry(() =>
      this.ai.models.generateContent({ model, contents: prompt, config })
    );

    return ImageGenerationResult.fromResponse(response);
  }

  /** Expose the underlying GoogleGenAI instance for chat creation */
  get genai(): InstanceType<typeof GoogleGenAI> {
    return this.ai;
  }
}
