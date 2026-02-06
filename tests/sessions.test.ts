// tests/sessions.test.ts
import { describe, test, expect, mock, beforeEach } from "bun:test";

// Mock @google/genai (not ../src/client) to avoid contaminating other test files
const mockSendMessage = mock(async () => ({
  candidates: [
    {
      content: {
        parts: [{ text: "response" }],
      },
    },
  ],
}));

mock.module("@google/genai", () => ({
  GoogleGenAI: mock(() => ({
    models: { generateContent: mock() },
    chats: {
      create: () => ({
        sendMessage: mockSendMessage,
      }),
    },
  })),
}));

import { ChatSessionManager, ChatSession } from "../src/sessions";

describe("ChatSessionManager", () => {
  beforeEach(() => {
    process.env.GEMINI_API_KEY = "test-key";
  });

  test("create session returns id", () => {
    const manager = new ChatSessionManager();
    const id = manager.createSession("gemini-3-pro-image-preview");
    expect(typeof id).toBe("string");
    expect(id.length).toBeGreaterThan(0);
  });

  test("get session returns session", () => {
    const manager = new ChatSessionManager();
    const id = manager.createSession("gemini-3-pro-image-preview");
    const session = manager.getSession(id);
    expect(session).toBeDefined();
    expect(session).toBeInstanceOf(ChatSession);
  });

  test("get nonexistent session throws", () => {
    const manager = new ChatSessionManager();
    expect(() => manager.getSession("nonexistent")).toThrow("Session not found");
  });

  test("delete session removes it", () => {
    const manager = new ChatSessionManager();
    const id = manager.createSession("gemini-3-pro-image-preview");
    manager.deleteSession(id);
    expect(() => manager.getSession(id)).toThrow("Session not found");
  });

  test("delete nonexistent session throws", () => {
    const manager = new ChatSessionManager();
    expect(() => manager.deleteSession("nonexistent")).toThrow("Session not found");
  });

  test("list sessions returns all ids", () => {
    const manager = new ChatSessionManager();
    const id1 = manager.createSession("gemini-3-pro-image-preview");
    const id2 = manager.createSession("pro");
    const sessions = manager.listSessions();
    expect(sessions).toContain(id1);
    expect(sessions).toContain(id2);
  });
});

describe("ChatSession", () => {
  beforeEach(() => {
    process.env.GEMINI_API_KEY = "test-key";
    mockSendMessage.mockClear();
  });

  test("send message stores history", async () => {
    const manager = new ChatSessionManager();
    const id = manager.createSession("gemini-3-pro-image-preview");
    const session = manager.getSession(id);

    await session.sendMessage("test prompt");

    expect(session.history).toHaveLength(2);
    expect(session.history[0].role).toBe("user");
    expect(session.history[0].content).toBe("test prompt");
    expect(session.history[1].role).toBe("assistant");
  });
});
