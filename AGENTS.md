# Repository guidance

Read and follow `MAINTENANCE.md` before changing these templates.

- Preserve compatibility across every released patch served by an `X.Y.x`
  branch.
- Use only a released Convertigo Gradle plugin on a shared maintenance branch.
- Keep root JSON manifests valid and ensure every imported file exists.
- Review all supported CI templates when changing Java, Gradle, actions or
  plugins.
