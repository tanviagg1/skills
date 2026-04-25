Generate a changelog entry from recent commits.

Follow these steps:

1. Ask me what version this release is for (e.g. v1.2.0). If unsure, check `git tag` for the latest tag.

2. Run `git log <last-tag>..HEAD --oneline` to get commits since last release. If no tags exist, use the last 20 commits.

3. Group commits into these sections (skip empty ones):
   ### Added
   ### Changed
   ### Fixed
   ### Removed
   ### Security

4. Write each entry as a short plain-English sentence, not a raw commit message.

5. Output in Keep a Changelog format:
   ## [version] - YYYY-MM-DD
   ### Added
   - ...

6. Ask if I want to copy this to a CHANGELOG.md file.
