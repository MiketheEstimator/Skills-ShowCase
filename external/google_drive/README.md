# Google Drive Integration Staging

Place synchronized files from Google Drive in this folder using your approved tooling.

## Expected flow
1. Sync source files into this directory.
2. Build or update `catalog.json` with normalized metadata (id, source path, checksum, tags, mapped skill).
3. Reference normalized entries from playbooks/skill sheets instead of direct remote URLs.

This keeps runtime behavior deterministic and fully versioned.
