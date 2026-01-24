# NFOStandard.Validator

`NFOStandard.Validator` provides an offline-capable XML validator for the
NFO Standard schemas. It is designed to be packaged for NuGet and embedded in
.NET applications that need to validate `.nfo` files.

## Usage

```csharp
using NFOStandard.Validator;

var document = NfoDocument.Load("movie.nfo");
var media = document.Media;

var validator = new NfoValidator();
var result = validator.ValidateFile("movie.nfo", "./v2");
if (!result.IsValid)
{
    foreach (var error in result.Errors)
    {
        Console.WriteLine(error);
    }
}

document.Save("movie.updated.nfo");
```

`schemaDir` should point to a directory that contains `main.xsd` and a
`Schemas/` folder. When omitted, the validator will look for `./v2`.
