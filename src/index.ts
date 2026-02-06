// src/index.ts
import { main } from "./server";

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
