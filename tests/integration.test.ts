// tests/integration.test.ts
import { describe, test, expect, beforeAll } from "bun:test";
import * as fs from "node:fs";
import * as path from "node:path";
import * as os from "node:os";

// Skip all tests if no real API key (other test files may set GEMINI_API_KEY="test-key")
const hasApiKey = !!process.env.GEMINI_API_KEY && process.env.GEMINI_API_KEY.length > 20;

describe.skipIf(!hasApiKey)("integration", () => {
  test("generate simple image", async () => {
    // Dynamic import to avoid initialization errors when no key
    const { GeminiImageClient } = await import("../src/client");
    const client = new GeminiImageClient();
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "nbp-int-"));
    const outputPath = path.join(tmpDir, "test.png");

    const result = await client.generateImage(
      "A simple red circle on white background",
      "pro",
      "1:1",
      "1K"
    );

    expect(result.imageData).not.toBeNull();
    if (result.imageData) {
      fs.writeFileSync(outputPath, result.imageData);
      expect(fs.existsSync(outputPath)).toBe(true);
    }

    fs.rmSync(tmpDir, { recursive: true });
  }, 60000);

  test("chat session flow: start, continue, end", async () => {
    const { ChatSessionManager } = await import("../src/sessions");
    const manager = new ChatSessionManager();

    // Start
    const sessionId = manager.createSession("pro");
    const session = manager.getSession(sessionId);

    // First message
    const result1 = await session.sendMessage("Draw a blue square");
    expect(result1.text).not.toBeNull();
    expect(session.history).toHaveLength(2); // user + assistant

    // Continue
    const result2 = await session.sendMessage("Now make it red");
    expect(result2.text).not.toBeNull();
    expect(session.history).toHaveLength(4); // 2 turns

    // End
    manager.deleteSession(sessionId);
    expect(() => manager.getSession(sessionId)).toThrow("Session not found");
    expect(manager.listSessions()).not.toContain(sessionId);
  }, 120000);
});
