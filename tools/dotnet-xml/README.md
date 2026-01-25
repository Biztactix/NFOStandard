# NFOStandard .NET XML Toolkit

This tool provides generated .NET models and validation for NFO Standard XML
files. It includes a class library for integration and a small CLI wrapper for
local validation.

## Projects

- `NFOStandard.Xml`: class library intended for NuGet packaging
- `NFOStandard.Xml.Console`: CLI for validating XML files

## Requirements

- .NET 8.0 SDK or later

## Build

```bash
dotnet build tools/dotnet-xml/NFOStandard.Xml.Console/NFOStandard.Xml.Console.csproj
```

## CLI Usage

```bash
dotnet run --project tools/dotnet-xml/NFOStandard.Xml.Console -- \
  --file examples/tvshow.xml \
  --schema-dir v2
```

Arguments:
- `--file`, `-f`: XML file to validate (required)
- `--schema-dir`, `-s`: Path containing `main.xsd` and `Schemas/` (defaults to `./v2` when present)
- `--json`: Output results as JSON

When `--schema-dir` is omitted, the CLI uses the schema version declared in
`xsi:schemaLocation` and validates against the embedded versioned schemas.

## Library Usage

```csharp
using NFOStandard.Xml;

var root = NfoSerializer.Load("movie.nfo");
var movie = root.Media.Movie;

// Make edits using the strongly typed model
if (movie != null)
{
    movie.Title = "Updated Title";
}

NfoSerializer.Save(root, "movie.updated.nfo");
```

## NuGet Packaging

```bash
dotnet pack tools/dotnet-xml/NFOStandard.Xml/NFOStandard.Xml.csproj -c Release
```

The package metadata is configured in `NFOStandard.Xml.csproj` and is
ready for future publishing.

### Release Workflow

1. Update the version in `tools/dotnet-xml/NFOStandard.Xml/NFOStandard.Xml.csproj`.
2. Create a tag in the format `dotnet-xml-v<version>` (example: `dotnet-xml-v2.0.1`).
3. Push the tag to GitHub; the workflow `Pack NuGet (NFOStandard.Xml)` will
   build, pack, and upload the artifacts.
4. To publish to nuget.org, add a repository secret named `NUGET_API_KEY`.

## Model Generation

The models are generated at build time from versioned XSDs embedded in the
NuGet package. Updating the package is what upgrades the schema version.

## Compatibility Plan

- Package versions map to schema versions (v2 package ships v2 schemas/models).
- When v3 lands, `NFOStandard.Xml` v3 will embed both v2 and v3 schemas so it
  can read v2 or v3 inputs.
- The v3 package will only write v3 output; upgrading legacy content will be a
  one-way operation via `object.Migrate()` to a v3 model.
