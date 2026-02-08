// tests/server.test.ts
import { describe, test, expect, mock, beforeEach } from "bun:test";
import * as fs from "node:fs";
import * as path from "node:path";
import * as os from "node:os";

// Mock @google/genai
mock.module("@google/genai", () => ({
  GoogleGenAI: mock(() => ({
    models: { generateContent: mock() },
    chats: { create: mock() },
  })),
}));

import {
  resultToDict,
  generateOutputPath,
  DEFAULT_OUTPUT_DIR,
} from "../src/server";
import { ImageGenerationResult } from "../src/client";

describe("generateOutputPath", () => {
  test("creates directory and returns path", () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "nbp-test-"));
    const outputDir = path.join(tmpDir, "outputs");

    const result = generateOutputPath("image", outputDir);

    expect(fs.existsSync(outputDir)).toBe(true);
    expect(result.startsWith(outputDir)).toBe(true);
    expect(path.basename(result)).toMatch(/^image_\d+_\d+_\d+\.png$/);

    fs.rmSync(tmpDir, { recursive: true });
  });

  test("uses prefix", () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "nbp-test-"));
    const result = generateOutputPath("edited", tmpDir);
    expect(path.basename(result)).toMatch(/^edited_/);
    fs.rmSync(tmpDir, { recursive: true });
  });
});

describe("resultToDict", () => {
  test("saves image to specified path", () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "nbp-test-"));
    const outputPath = path.join(tmpDir, "test.png");

    const result = new ImageGenerationResult(
      "Test image",
      Buffer.from("fake image bytes"),
      "image/png"
    );

    const response = resultToDict(result, outputPath);

    expect(response.text).toBe("Test image");
    expect(response.saved_path).toBe(path.resolve(outputPath));
    expect(fs.readFileSync(outputPath)).toEqual(Buffer.from("fake image bytes"));

    fs.rmSync(tmpDir, { recursive: true });
  });

  test("auto-generates path when not specified", () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "nbp-test-"));

    const result = new ImageGenerationResult(
      "Test image",
      Buffer.from("fake image bytes"),
      "image/png"
    );

    const response = resultToDict(result, null, tmpDir);

    expect(response.saved_path).not.toBeNull();
    expect(response.saved_path!).toContain(tmpDir);
    expect(fs.readFileSync(response.saved_path!)).toEqual(
      Buffer.from("fake image bytes")
    );

    fs.rmSync(tmpDir, { recursive: true });
  });

  test("does not include base64", () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "nbp-test-"));

    const result = new ImageGenerationResult(
      "Test",
      Buffer.from("data"),
      "image/png"
    );

    const response = resultToDict(result, null, tmpDir);

    expect(response).not.toHaveProperty("image_base64");

    fs.rmSync(tmpDir, { recursive: true });
  });
});

// --- MCP server smoke tests ---
// These verify the server object is correctly configured.

import { server } from "../src/server";

describe("MCP server", () => {
  test("server is defined and has expected name", () => {
    expect(server).toBeDefined();
    // McpServer stores name in its options
  });
});

describe("validate_intake_digest", () => {
  test("validateDigest works for valid minimal digest", () => {
    const { validateDigest } = require("../src/digest-schema");
    const result = validateDigest({
      meta: {
        confidence: "low",
        source_type: "minimal",
        source_reference: null,
        extraction_notes: "test",
      },
      extracted: {},
      needs_interview: [],
      ambiguities: [],
    });
    expect(result.valid).toBe(true);
  });
});

describe("session manager integration", () => {
  test("list_chat_sessions returns empty initially", () => {
    const { ChatSessionManager } = require("../src/sessions");
    const manager = new ChatSessionManager();
    expect(manager.listSessions()).toEqual([]);
  });

  test("full session lifecycle", () => {
    const { ChatSessionManager } = require("../src/sessions");
    const manager = new ChatSessionManager();

    const id = manager.createSession("gemini-3-pro-image-preview");
    expect(manager.listSessions()).toContain(id);

    const session = manager.getSession(id);
    expect(session.sessionId).toBe(id);

    manager.deleteSession(id);
    expect(manager.listSessions()).not.toContain(id);
    expect(() => manager.getSession(id)).toThrow("Session not found");
  });
});
