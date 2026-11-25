// Entry program for make.fun news-image-20261124 (front page).
// Copies the front-page image drawn by generate_entry.py into the
// grader's output directory. The bytes are identical on every run:
// no network, no clock, no randomness is involved anywhere.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(targetDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(targetDir, "entry.png"));
