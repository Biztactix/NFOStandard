# NFOStandard .NET Validator

This tool provides a .NET validator for NFO Standard XML files. It includes a
class library for integration and a small CLI wrapper for local validation.

## Projects

- `NFOStandard.Validator`: class library intended for NuGet packaging
- `NFOStandard.Validator.Console`: CLI for validating XML files

## Requirements

- .NET 6.0 SDK or later

## Build

```bash
dotnet build tools/dotnet-validator/NFOStandard.Validator.Console/NFOStandard.Validator.Console.csproj
```

## CLI Usage

```bash
dotnet run --project tools/dotnet-validator/NFOStandard.Validator.Console -- \
  --file examples/tvshow.xml \
  --schema-dir v2
```

Arguments:
- `--file`, `-f`: XML file to validate (required)
- `--schema-dir`, `-s`: Path containing `main.xsd` and `Schemas/` (defaults to `./v2` when present)
- `--json`: Output results as JSON

## NuGet Packaging

```bash
dotnet pack tools/dotnet-validator/NFOStandard.Validator/NFOStandard.Validator.csproj -c Release
```

The package metadata is configured in `NFOStandard.Validator.csproj` and is
ready for future publishing.
