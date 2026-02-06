// src/server.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import * as fs from "node:fs";
import * as path from "node:path";

import { GeminiImageClient, ImageGenerationResult } from "./client";
import { ChatSessionManager } from "./sessions";
import { validateSeed } from "./utils";

export const DEFAULT_OUTPUT_DIR = "outputs";

let _client: GeminiImageClient | null = null;
const sessionManager = new ChatSessionManager();

function getClient(): GeminiImageClient {
  if (!_client) _client = new GeminiImageClient();
  return _client;
}

export function generateOutputPath(
  prefix: string = "image",
  outputDir: string = DEFAULT_OUTPUT_DIR
): string {
  fs.mkdirSync(outputDir, { recursive: true });
  const now = new Date();
  const timestamp =
    now.getFullYear().toString() +
    String(now.getMonth() + 1).padStart(2, "0") +
    String(now.getDate()).padStart(2, "0") +
    "_" +
    String(now.getHours()).padStart(2, "0") +
    String(now.getMinutes()).padStart(2, "0") +
    String(now.getSeconds()).padStart(2, "0") +
    "_" +
    String(now.getMilliseconds()).padStart(3, "0") +
    String(Math.floor(Math.random() * 1000)).padStart(3, "0");
  return path.join(outputDir, `${prefix}_${timestamp}.png`);
}

export function resultToDict(
  result: ImageGenerationResult,
  outputPath: string | null = null,
  defaultOutputDir: string = DEFAULT_OUTPUT_DIR
): Record<string, any> {
  const response: Record<string, any> = {
    text: result.text,
    mime_type: result.mimeType,
    saved_path: null,
  };

  if (result.imageData) {
    let savePath: string;
    if (outputPath) {
      savePath = outputPath;
      fs.mkdirSync(path.dirname(savePath), { recursive: true });
    } else {
      savePath = generateOutputPath("image", defaultOutputDir);
    }
    fs.writeFileSync(savePath, result.imageData);
    response.saved_path = path.resolve(savePath);
  }

  if (result.groundingMetadata) {
    response.grounding_metadata = result.groundingMetadata;
  }

  return response;
}

// Create MCP server
export const server = new McpServer({
  name: "nanobananapro",
  version: "0.1.0",
});

// Tool: generate_image
server.tool(
  "generate_image",
  "Generate an image from a text prompt.",
  {
    prompt: z.string().describe("Text description of the image to generate"),
    model: z.string().default("gemini-3-pro-image-preview").describe('Model to use - "pro", "nano-banana-pro", or full model name'),
    aspect_ratio: z.string().default("1:1").describe("Output aspect ratio (1:1, 16:9, 9:16, etc.)"),
    resolution: z.string().default("1K").describe("Output resolution (1K, 2K, 4K)"),
    output_path: z.string().optional().describe("Path to save the image (default: outputs/image_TIMESTAMP.png)"),
    seed: z.number().int().optional().describe("Optional seed for reproducible generation (0 to 2147483647)"),
  },
  async ({ prompt, model, aspect_ratio, resolution, output_path, seed }) => {
    const validatedSeed = validateSeed(seed ?? null);
    const client = getClient();
    const result = await client.generateImage(prompt, model, aspect_ratio, resolution, validatedSeed);
    const dict = resultToDict(result, output_path ?? null);
    return { content: [{ type: "text" as const, text: JSON.stringify(dict) }] };
  }
);

// Tool: edit_image
server.tool(
  "edit_image",
  "Edit an existing image using a text prompt.",
  {
    prompt: z.string().describe("Instructions for editing the image"),
    image_path: z.string().describe("Path to the input image file"),
    model: z.string().default("gemini-3-pro-image-preview").describe('Model to use'),
    aspect_ratio: z.string().optional().describe("Output aspect ratio (optional, defaults to input)"),
    resolution: z.string().default("1K").describe("Output resolution (1K, 2K, 4K)"),
    output_path: z.string().optional().describe("Path to save the image"),
    seed: z.number().int().optional().describe("Optional seed for reproducible generation"),
  },
  async ({ prompt, image_path, model, aspect_ratio, resolution, output_path, seed }) => {
    const validatedSeed = validateSeed(seed ?? null);
    const client = getClient();
    const result = await client.editImage(prompt, image_path, model, aspect_ratio ?? null, resolution, validatedSeed);
    const dict = resultToDict(result, output_path ?? null);
    return { content: [{ type: "text" as const, text: JSON.stringify(dict) }] };
  }
);

// Tool: compose_images
server.tool(
  "compose_images",
  "Compose a new image from multiple reference images.",
  {
    prompt: z.string().describe("Instructions for composing the images"),
    image_paths: z.array(z.string()).describe("List of paths to input images (max 14)"),
    model: z.string().default("gemini-3-pro-image-preview").describe('Model to use'),
    aspect_ratio: z.string().default("1:1").describe("Output aspect ratio"),
    resolution: z.string().default("2K").describe("Output resolution"),
    output_path: z.string().optional().describe("Path to save the image"),
    seed: z.number().int().optional().describe("Optional seed for reproducible generation"),
  },
  async ({ prompt, image_paths, model, aspect_ratio, resolution, output_path, seed }) => {
    const validatedSeed = validateSeed(seed ?? null);
    const client = getClient();
    const result = await client.composeImages(prompt, image_paths, model, aspect_ratio, resolution, validatedSeed);
    const dict = resultToDict(result, output_path ?? null);
    return { content: [{ type: "text" as const, text: JSON.stringify(dict) }] };
  }
);

// Tool: search_grounded_image
server.tool(
  "search_grounded_image",
  "Generate an image grounded with Google Search data (Pro only).",
  {
    prompt: z.string().describe("Description incorporating real-time data needs"),
    aspect_ratio: z.string().default("16:9").describe("Output aspect ratio"),
    resolution: z.string().default("2K").describe("Output resolution (1K, 2K, 4K)"),
    output_path: z.string().optional().describe("Path to save the image"),
  },
  async ({ prompt, aspect_ratio, resolution, output_path }) => {
    const client = getClient();
    const result = await client.searchGroundedImage(prompt, aspect_ratio, resolution);
    const dict = resultToDict(result, output_path ?? null);
    return { content: [{ type: "text" as const, text: JSON.stringify(dict) }] };
  }
);

// Tool: start_image_chat
server.tool(
  "start_image_chat",
  "Start a new multi-turn image editing session.",
  {
    initial_prompt: z.string().describe("First prompt to generate the initial image"),
    model: z.string().default("gemini-3-pro-image-preview").describe("Model to use for the session"),
    output_path: z.string().optional().describe("Path to save the image"),
    seed: z.number().int().optional().describe("Optional seed (currently ignored in chat sessions)"),
  },
  async ({ initial_prompt, model, output_path, seed }) => {
    validateSeed(seed ?? null);
    const sessionId = sessionManager.createSession(model);
    const session = sessionManager.getSession(sessionId);
    const result = await session.sendMessage(initial_prompt);
    const dict = resultToDict(result, output_path ?? null);
    dict.session_id = sessionId;
    return { content: [{ type: "text" as const, text: JSON.stringify(dict) }] };
  }
);

// Tool: continue_image_chat
server.tool(
  "continue_image_chat",
  "Continue an existing image chat session.",
  {
    session_id: z.string().describe("ID of the session to continue"),
    prompt: z.string().describe("Next instruction for image modification"),
    aspect_ratio: z.string().optional().describe("Optional new aspect ratio"),
    resolution: z.string().optional().describe("Optional new resolution"),
    output_path: z.string().optional().describe("Path to save the image"),
  },
  async ({ session_id, prompt, aspect_ratio, resolution, output_path }) => {
    const session = sessionManager.getSession(session_id);
    const result = await session.sendMessage(prompt, aspect_ratio ?? null, resolution ?? null);
    const dict = resultToDict(result, output_path ?? null);
    dict.session_id = session_id;
    dict.turn_count = Math.floor(session.history.length / 2);
    return { content: [{ type: "text" as const, text: JSON.stringify(dict) }] };
  }
);

// Tool: end_image_chat
server.tool(
  "end_image_chat",
  "End and clean up an image chat session.",
  {
    session_id: z.string().describe("ID of the session to end"),
  },
  async ({ session_id }) => {
    const session = sessionManager.getSession(session_id);
    const turnCount = Math.floor(session.history.length / 2);
    sessionManager.deleteSession(session_id);
    const dict = { status: "ended", session_id, total_turns: turnCount };
    return { content: [{ type: "text" as const, text: JSON.stringify(dict) }] };
  }
);

// Tool: list_chat_sessions
server.tool(
  "list_chat_sessions",
  "List all active chat sessions.",
  {},
  async () => {
    const sessions = sessionManager.listSessions();
    const dict = { sessions, count: sessions.length };
    return { content: [{ type: "text" as const, text: JSON.stringify(dict) }] };
  }
);

export async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("nanobananapro MCP server running on stdio");
}
