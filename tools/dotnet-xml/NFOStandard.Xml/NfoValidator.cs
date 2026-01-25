using System;
using System.Collections.Generic;
using System.IO;
using System.Xml;
using System.Xml.Schema;

namespace NFOStandard.Xml;

public sealed class NfoValidator
{
    private const string SchemaLocationNamespace = "http://www.w3.org/2001/XMLSchema-instance";
    private const string DefaultSchemaRelativePath = "v2";

    public ValidationResult ValidateFile(string xmlPath, string? schemaDir = null)
    {
        if (string.IsNullOrWhiteSpace(xmlPath))
        {
            throw new ArgumentException("XML path is required.", nameof(xmlPath));
        }

        if (!File.Exists(xmlPath))
        {
            return new ValidationResult(false, null, new List<string> { $"File not found: {xmlPath}" });
        }

        var resolvedSchemaDir = ResolveSchemaDirectory(schemaDir);
        string? schemaSource = null;
        string? embeddedVersion = null;

        var schemaSet = new XmlSchemaSet();
        XmlResolver resolver = resolvedSchemaDir != null
            ? new LocalSchemaResolver(resolvedSchemaDir)
            : new XmlUrlResolver();
        schemaSet.XmlResolver = resolver;

        try
        {
            if (resolvedSchemaDir != null)
            {
                var schemaPath = Path.Combine(resolvedSchemaDir, "main.xsd");
                if (!File.Exists(schemaPath))
                {
                    return new ValidationResult(false, resolvedSchemaDir, new List<string>
                    {
                        $"Schema not found: {schemaPath}"
                    });
                }

                schemaSource = schemaPath;
                using var schemaReader = XmlReader.Create(schemaPath, new XmlReaderSettings
                {
                    XmlResolver = resolver
                });
                schemaSet.Add(null, schemaReader);
            }
            else
            {
                schemaSource = GetSchemaLocation(xmlPath);
                if (string.IsNullOrWhiteSpace(schemaSource))
                {
                    return new ValidationResult(false, null, new List<string>
                    {
                        "No xsi:schemaLocation found and no schema directory provided."
                    });
                }

                embeddedVersion = NfoSchemaRegistry.DetectVersion(schemaSource);
                if (embeddedVersion != null && NfoSchemaRegistry.HasVersion(embeddedVersion))
                {
                    resolver = new EmbeddedSchemaResolver(embeddedVersion);
                    schemaSet.XmlResolver = resolver;
                    using var schemaStream = NfoSchemaRegistry.OpenSchema(embeddedVersion, "main.xsd");
                    if (schemaStream == null)
                    {
                        return new ValidationResult(false, schemaSource, new List<string>
                        {
                            $"Embedded schema not found for {embeddedVersion}."
                        });
                    }

                    using var schemaReader = XmlReader.Create(schemaStream, new XmlReaderSettings
                    {
                        XmlResolver = resolver
                    });
                    schemaSet.Add(null, schemaReader);
                    schemaSource = $"embedded:{embeddedVersion}";
                }
                else
                {
                    schemaSet.Add(null, schemaSource);
                }
            }
        }
        catch (Exception ex)
        {
            return new ValidationResult(false, schemaSource, new List<string>
            {
                $"Schema load failed: {ex.Message}"
            });
        }

        var errors = new List<string>();
        var settings = new XmlReaderSettings
        {
            ValidationType = ValidationType.Schema,
            Schemas = schemaSet,
            XmlResolver = resolver
        };
        settings.ValidationEventHandler += (_, args) =>
        {
            var line = args.Exception?.LineNumber ?? 0;
            var position = args.Exception?.LinePosition ?? 0;
            var location = line > 0 ? $"Line {line}, Position {position}" : "Unknown location";
            errors.Add($"{location}: {args.Message}");
        };

        try
        {
            using var reader = XmlReader.Create(xmlPath, settings);
            while (reader.Read())
            {
            }
        }
        catch (Exception ex)
        {
            errors.Add($"Validation failed: {ex.Message}");
        }

        return new ValidationResult(errors.Count == 0, schemaSource, errors);
    }

    private static string? ResolveSchemaDirectory(string? schemaDir)
    {
        if (!string.IsNullOrWhiteSpace(schemaDir))
        {
            return NormalizeSchemaDirectory(schemaDir);
        }

        var candidate = Path.Combine(Directory.GetCurrentDirectory(), DefaultSchemaRelativePath);
        return NormalizeSchemaDirectory(candidate);
    }

    private static string? NormalizeSchemaDirectory(string schemaDir)
    {
        var fullPath = Path.GetFullPath(schemaDir);
        var mainSchema = Path.Combine(fullPath, "main.xsd");
        if (File.Exists(mainSchema))
        {
            return fullPath;
        }

        var v2Path = Path.Combine(fullPath, DefaultSchemaRelativePath);
        var v2Schema = Path.Combine(v2Path, "main.xsd");
        if (File.Exists(v2Schema))
        {
            return v2Path;
        }

        return null;
    }

    private static string? GetSchemaLocation(string xmlPath)
    {
        var document = new XmlDocument();
        document.Load(xmlPath);
        var root = document.DocumentElement;
        if (root == null)
        {
            return null;
        }

        var schemaLocation = root.GetAttribute("schemaLocation", SchemaLocationNamespace);
        if (string.IsNullOrWhiteSpace(schemaLocation))
        {
            return null;
        }

        var parts = schemaLocation.Split(new[] { ' ', '\t', '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
        return parts.Length >= 2 ? parts[1] : null;
    }
}
