// src/digest-schema.ts
import { z } from "zod";

const EmotionalArcSchema = z.object({
  start_emotion: z.string().nullable(),
  end_emotion: z.string().nullable(),
  arc_type: z.enum(["building", "shifting", "static", "cyclical"]).nullable(),
});

const LocationSchema = z.object({
  name: z.string().min(1),
  description: z.string().nullable(),
});

const CharacterSchema = z.object({
  name: z.string().min(1),
  role: z.string().nullable(),
  archetype_function: z.string().nullable(),
  narrative_qualifier: z.string().nullable(),
  is_non_human: z.boolean(),
});

const MetaSchema = z.object({
  confidence: z.enum(["high", "medium", "low"]),
  source_type: z.enum(["known_ip", "pasted_text", "user_description", "minimal"]),
  source_reference: z.string().nullable(),
  extraction_notes: z.string(),
});

const ExtractedSchema = z.object({
  emotional_core: z.string().nullable().optional(),
  emotional_arc: EmotionalArcSchema.optional(),
  genre: z.union([z.string(), z.array(z.string())]).nullable().optional(),
  tone: z.string().nullable().optional(),
  source_material: z.string().nullable().optional(),
  source_priorities: z.string().nullable().optional(),
  narrative_framework: z.string().nullable().optional(),
  locations: z.array(LocationSchema).optional(),
  characters: z.array(CharacterSchema).optional(),
  total_duration_seconds: z.number().int().positive().nullable().optional(),
  output_format: z.string().nullable().optional(),
  pacing_style: z.string().nullable().optional(),
  dynamic_range: z.string().nullable().optional(),
  sonic_direction: z.string().nullable().optional(),
  medium: z.string().nullable().optional(),
  aspect_ratio: z.string().nullable().optional(),
});

const NeedsInterviewItemSchema = z.object({
  field: z.string().min(1),
  reason: z.string().min(1),
});

const AmbiguitySchema = z.object({
  topic: z.string().min(1),
  detail: z.string().min(1),
  options: z.array(z.string().min(1)).min(2).max(4),
});

export const DigestSchema = z.object({
  meta: MetaSchema,
  extracted: ExtractedSchema,
  needs_interview: z.array(NeedsInterviewItemSchema),
  ambiguities: z.array(AmbiguitySchema),
});

export type Digest = z.infer<typeof DigestSchema>;
