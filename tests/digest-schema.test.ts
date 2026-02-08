// tests/digest-schema.test.ts
import { describe, test, expect } from "bun:test";
import { DigestSchema } from "../src/digest-schema";

describe("DigestSchema", () => {
  function makeValidDigest(overrides: Record<string, any> = {}) {
    const base = {
      meta: {
        confidence: "high",
        source_type: "known_ip",
        source_reference: "Test IP",
        extraction_notes: "Test",
      },
      extracted: {
        emotional_core: "tension",
        genre: "action",
      },
      needs_interview: [],
      ambiguities: [],
    };
    return {
      ...base,
      ...overrides,
      meta: { ...base.meta, ...(overrides.meta || {}) },
      extracted: { ...base.extracted, ...(overrides.extracted || {}) },
    };
  }

  test("accepts a valid full digest", () => {
    const valid = {
      meta: {
        confidence: "high",
        source_type: "known_ip",
        source_reference: "The Witcher 3",
        extraction_notes: "Synthesized from training data",
      },
      extracted: {
        emotional_core: "grim determination",
        emotional_arc: {
          start_emotion: "uneasy calm",
          end_emotion: "desperate resolve",
          arc_type: "building",
        },
        genre: ["dark fantasy", "action"],
        tone: "gritty and visceral",
        source_material: "The Witcher 3: Wild Hunt",
        source_priorities: "Battle of Kaer Morhen sequence",
        narrative_framework: "heros_journey",
        locations: [
          { name: "Kaer Morhen", description: "ancient fortress in mountains" },
          { name: "Courtyard", description: "snow-covered stone courtyard" },
        ],
        characters: [
          {
            name: "Geralt",
            role: "protagonist",
            archetype_function: "hero",
            narrative_qualifier: "lone",
            is_non_human: false,
          },
          {
            name: "Yennefer",
            role: "ally",
            archetype_function: "mentor",
            narrative_qualifier: null,
            is_non_human: false,
          },
        ],
        total_duration_seconds: 30,
        output_format: "cinematic trailer",
        pacing_style: "building tempo",
        dynamic_range: "extreme",
        sonic_direction: "orchestral epic",
        medium: "film",
        aspect_ratio: "16:9",
      },
      needs_interview: [
        { field: "sonic_direction", reason: "Multiple valid interpretations" },
      ],
      ambiguities: [
        {
          topic: "character_count",
          detail: "Source has many characters. Recommend 3-4 for trailer.",
          options: ["Geralt, Yennefer, Ciri", "Geralt, Yennefer, Ciri, Eredin"],
        },
      ],
    };

    const result = DigestSchema.safeParse(valid);
    expect(result.success).toBe(true);
  });

  test("rejects invalid confidence value", () => {
    const invalid = makeValidDigest({ meta: { confidence: "very_high" } });
    const result = DigestSchema.safeParse(invalid);
    expect(result.success).toBe(false);
  });

  test("rejects invalid source_type", () => {
    const invalid = makeValidDigest({ meta: { source_type: "wikipedia" } });
    const result = DigestSchema.safeParse(invalid);
    expect(result.success).toBe(false);
  });

  test("rejects empty character name", () => {
    const invalid = makeValidDigest({
      extracted: {
        characters: [{ name: "", role: "protagonist", archetype_function: null, narrative_qualifier: null, is_non_human: false }],
      },
    });
    const result = DigestSchema.safeParse(invalid);
    expect(result.success).toBe(false);
  });

  test("rejects empty location name", () => {
    const invalid = makeValidDigest({
      extracted: {
        locations: [{ name: "", description: null }],
      },
    });
    const result = DigestSchema.safeParse(invalid);
    expect(result.success).toBe(false);
  });

  test("rejects ambiguity with fewer than 2 options", () => {
    const invalid = makeValidDigest({
      ambiguities: [{ topic: "chars", detail: "too few", options: ["one"] }],
    });
    const result = DigestSchema.safeParse(invalid);
    expect(result.success).toBe(false);
  });

  test("rejects ambiguity with more than 4 options", () => {
    const invalid = makeValidDigest({
      ambiguities: [{ topic: "chars", detail: "too many", options: ["a", "b", "c", "d", "e"] }],
    });
    const result = DigestSchema.safeParse(invalid);
    expect(result.success).toBe(false);
  });

  test("accepts minimal digest with empty extracted", () => {
    const minimal = {
      meta: {
        confidence: "low",
        source_type: "minimal",
        source_reference: null,
        extraction_notes: "Very little to extract",
      },
      extracted: {},
      needs_interview: [
        { field: "emotional_core", reason: "Not stated" },
        { field: "genre", reason: "Not stated" },
      ],
      ambiguities: [],
    };
    const result = DigestSchema.safeParse(minimal);
    expect(result.success).toBe(true);
  });

  test("rejects negative total_duration_seconds", () => {
    const invalid = makeValidDigest({
      extracted: { total_duration_seconds: -5 },
    });
    const result = DigestSchema.safeParse(invalid);
    expect(result.success).toBe(false);
  });
});
