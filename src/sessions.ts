// src/sessions.ts
import { GeminiImageClient, ImageGenerationResult } from "./client";
import { validateModel, validateAspectRatio, validateResolution } from "./utils";

interface HistoryEntry {
  role: "user" | "assistant";
  content: string | null;
  hasImage?: boolean;
}

export class ChatSession {
  readonly sessionId: string;
  readonly model: string;
  readonly history: HistoryEntry[] = [];
  private chat: any;

  constructor(model: string) {
    this.model = validateModel(model);
    this.sessionId = crypto.randomUUID();

    const client = new GeminiImageClient();
    this.chat = client.genai.chats.create({
      model: this.model,
      config: {
        responseModalities: ["TEXT", "IMAGE"],
        tools: this.model.includes("pro") ? [{ googleSearch: {} }] : undefined,
      },
    });
  }

  async sendMessage(
    prompt: string,
    aspectRatio: string | null = null,
    resolution: string | null = null
  ): Promise<ImageGenerationResult> {
    aspectRatio = validateAspectRatio(aspectRatio);
    resolution = validateResolution(resolution, this.model);

    this.history.push({ role: "user", content: prompt });

    // IMPORTANT: per-request config REPLACES chat-level config (no merging),
    // so we must re-include responseModalities and tools here.
    const response = await this.chat.sendMessage({
      message: prompt,
      config: {
        responseModalities: ["TEXT", "IMAGE"],
        tools: this.model.includes("pro") ? [{ googleSearch: {} }] : undefined,
        imageConfig: {
          aspectRatio,
          imageSize: this.model.includes("pro") ? resolution : undefined,
        },
      },
    });

    const result = ImageGenerationResult.fromResponse(response);

    this.history.push({
      role: "assistant",
      content: result.text,
      hasImage: result.imageData !== null,
    });

    return result;
  }
}

export class ChatSessionManager {
  private sessions = new Map<string, ChatSession>();

  createSession(model: string = "gemini-3-pro-image-preview"): string {
    const session = new ChatSession(model);
    this.sessions.set(session.sessionId, session);
    return session.sessionId;
  }

  getSession(sessionId: string): ChatSession {
    const session = this.sessions.get(sessionId);
    if (!session) throw new Error(`Session not found: ${sessionId}`);
    return session;
  }

  deleteSession(sessionId: string): void {
    if (!this.sessions.has(sessionId)) {
      throw new Error(`Session not found: ${sessionId}`);
    }
    this.sessions.delete(sessionId);
  }

  listSessions(): string[] {
    return Array.from(this.sessions.keys());
  }
}
