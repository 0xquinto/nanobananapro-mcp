// tests/digest-schema.test.ts
import { describe, test, expect } from "bun:test";
import { DigestSchema } from "../src/digest-schema";

describe("DigestSchema", () => {
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
});
