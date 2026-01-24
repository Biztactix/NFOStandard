using System.Collections.Generic;

namespace NFOStandard.Validator;

public sealed class ValidationResult
{
    public ValidationResult(bool isValid, string? schemaSource, IReadOnlyList<string> errors)
    {
        IsValid = isValid;
        SchemaSource = schemaSource;
        Errors = errors;
    }

    public bool IsValid { get; }

    public string? SchemaSource { get; }

    public IReadOnlyList<string> Errors { get; }
}
