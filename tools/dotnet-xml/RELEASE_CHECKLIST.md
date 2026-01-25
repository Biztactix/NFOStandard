# NFOStandard.Xml NuGet Release Checklist

Use this checklist when you are ready to publish a new NuGet package.

## Preparation
- Confirm `main` is green and the .NET tests pass.
- Update `Version` in `tools/dotnet-xml/NFOStandard.Xml/NFOStandard.Xml.csproj`.
- Review `tools/dotnet-xml/NFOStandard.Xml/README.md` for any updates.
- Ensure the `NUGET_API_KEY` secret is set in GitHub Actions.

## Pack (dry run)
1. Go to Actions → **Pack NuGet (NFOStandard.Xml)**.
2. Run workflow with `publish=false`.
3. Download the `nfo-dotnet-nuget` artifact and inspect the `.nupkg`.

## Publish
1. Run the workflow again with `publish=true`.
2. Confirm the package appears on nuget.org.

## Post-release
- Update any version references in docs if needed.
- Announce the release with the changelog summary.
