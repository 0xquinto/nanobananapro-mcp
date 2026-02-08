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

export interface ValidationIssue {
  path: string;
  message: string;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationIssue[];
  warnings: ValidationIssue[];
}

export function validateDigest(input: unknown): ValidationResult {
  const errors: ValidationIssue[] = [];
  const warnings: ValidationIssue[] = [];

  // Step 1: Schema validation
  const parsed = DigestSchema.safeParse(input);
  if (!parsed.success) {
    for (const issue of parsed.error.issues) {
      errors.push({
        path: issue.path.join("."),
        message: issue.message,
      });
    }
    return { valid: false, errors, warnings };
  }

  const digest = parsed.data;

  // Step 2: Semantic checks
  const extracted = digest.extracted;
  const populatedCount = Object.entries(extracted).filter(
    ([_, v]) => v !== null && v !== undefined
  ).length;

  // High confidence but sparse extraction
  if (digest.meta.confidence === "high" && populatedCount < 6) {
    warnings.push({
      path: "meta.confidence",
      message: `high confidence but only ${populatedCount} extracted fields populated`,
    });
  }

  // Known IP but no characters
  if (
    digest.meta.source_type === "known_ip" &&
    (!extracted.characters || extracted.characters.length === 0)
  ) {
    warnings.push({
      path: "extracted.characters",
      message: "source_type is known_ip but no characters were extracted",
    });
  }

  // Duplicate character names
  if (extracted.characters && extracted.characters.length > 1) {
    const names = extracted.characters.map((c) => c.name);
    const dupes = names.filter((n, i) => names.indexOf(n) !== i);
    if (dupes.length > 0) {
      warnings.push({
        path: "extracted.characters",
        message: `duplicate character names: ${[...new Set(dupes)].join(", ")}`,
      });
    }
  }

  // Duplicate location names
  if (extracted.locations && extracted.locations.length > 1) {
    const names = extracted.locations.map((l) => l.name);
    const dupes = names.filter((n, i) => names.indexOf(n) !== i);
    if (dupes.length > 0) {
      warnings.push({
        path: "extracted.locations",
        message: `duplicate location names: ${[...new Set(dupes)].join(", ")}`,
      });
    }
  }

  return { valid: true, errors, warnings };
}
