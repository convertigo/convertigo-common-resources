# Maintenance

Convertigo Studio downloads these files when it configures continuous
integration for a project. The files are templates: they are copied into the
project, and an existing file is renamed before an update so that local changes
are preserved.

## Version branches

- Maintain one mutable `X.Y.x` branch for each supported Convertigo line.
- Studio versions using this convention always download from their `X.Y.x`
  branch, so changes must remain compatible with every released patch in that
  line.
- Use the latest **released** `X.Y` Convertigo Gradle plugin on the shared
  branch. Never use a `-SNAPSHOT` version there: a later beta would otherwise
  change the resources downloaded by an already released Studio.
- Exact `X.Y.Z` branches are compatibility aliases for Studio versions released
  before the `X.Y.x` convention. Keep them fixed at compatible content.
- Tags, when introduced, are immutable release records and must never be moved.
- Develop changes for the next line on its own branch. Do not merge templates
  that require a newer engine, plugin or Java version into an older line.

## Release review

Before a Convertigo release, review the active `X.Y.x` branch:

1. Check the Gradle wrapper, the Convertigo Gradle plugin and its repositories.
2. Check the Java version required by the engine and by CI runners.
3. Review GitHub Actions, GitLab CI and CircleCI action/plugin versions.
4. Validate every root JSON manifest and every file referenced by its `imports`.
5. Fetch the root manifests through their raw GitHub `X.Y.x` URLs.

During beta, keep the branch on the latest stable plugin for the line. After
the release pipeline publishes `com.convertigo:gradle-plugin:X.Y.Z`, update the
branch to that stable version and repeat the validation.

The Convertigo engine release checklist in `convertigo/RELEASE.md` is the
coordinating procedure.

## Local validation

Run the repository validation with:

```sh
python3 scripts/validate.py
cd gradle && ./gradlew help --no-daemon --warning-mode all
```

The GitHub validation workflow runs these checks and parses the three CI YAML
templates. Build a representative project with the Gradle template when the
wrapper, plugin, Java version, or Gradle script changes.
