// tests/output-path.test.ts
import { describe, test, expect } from "bun:test";
import * as fs from "node:fs";
import * as path from "node:path";
import * as os from "node:os";

// Mock @google/genai
import { mock } from "bun:test";
mock.module("@google/genai", () => ({
  GoogleGenAI: mock(() => ({
    models: { generateContent: mock() },
    chats: { create: mock() },
  })),
}));

import { resultToDict, generateOutputPath } from "../src/server";
import { ImageGenerationResult } from "../src/client";

test("resultToDict with output_path saves to specified path", () => {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "nbp-test-"));
  const outputPath = path.join(tmpDir, "test.png");
  const result = new ImageGenerationResult("Test image", Buffer.from("fake image bytes"), "image/png");

  const response = resultToDict(result, outputPath);

  expect(response.saved_path).toBe(path.resolve(outputPath));
  expect(fs.readFileSync(outputPath)).toEqual(Buffer.from("fake image bytes"));
  fs.rmSync(tmpDir, { recursive: true });
});

test("resultToDict without output_path saves to default", () => {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "nbp-test-"));
  const result = new ImageGenerationResult("Test image", Buffer.from("fake image bytes"), "image/png");

  const response = resultToDict(result, null, tmpDir);

  expect(response.saved_path).not.toBeNull();
  expect(response.saved_path!).toContain(tmpDir);
  expect(fs.existsSync(response.saved_path!)).toBe(true);
  fs.rmSync(tmpDir, { recursive: true });
});

test("generateOutputPath creates directory if needed", () => {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "nbp-test-"));
  const outputDir = path.join(tmpDir, "outputs");
  expect(fs.existsSync(outputDir)).toBe(false);

  const result = generateOutputPath("image", outputDir);

  expect(fs.existsSync(outputDir)).toBe(true);
  expect(path.basename(result)).toMatch(/^image_/);
  expect(result).toEndWith(".png");
  fs.rmSync(tmpDir, { recursive: true });
});

test("generateOutputPath uses prefix", () => {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "nbp-test-"));
  const result = generateOutputPath("edited", tmpDir);
  expect(path.basename(result)).toMatch(/^edited_/);
  fs.rmSync(tmpDir, { recursive: true });
});
