using System;
using System.IO;
using System.Text.Json;
using NFOStandard.Xml;

namespace NFOStandard.Xml.Console;

internal static class Program
{
    private sealed class Options
    {
        public string? FilePath { get; set; }
        public string? SchemaDir { get; set; }
        public bool Json { get; set; }
        public bool ShowHelp { get; set; }
    }

    private static int Main(string[] args)
    {
        Options options;
        try
        {
            options = ParseArguments(args);
        }
        catch (ArgumentException ex)
        {
            System.Console.WriteLine($"Error: {ex.Message}");
            PrintUsage();
            return 2;
        }

        if (options.ShowHelp || string.IsNullOrWhiteSpace(options.FilePath))
        {
            PrintUsage();
            return 2;
        }

        var validator = new NfoValidator();
        var result = validator.ValidateFile(options.FilePath, options.SchemaDir);

        if (options.Json)
        {
            var payload = new
            {
                valid = result.IsValid,
                schemaSource = result.SchemaSource,
                errors = result.Errors
            };
            System.Console.WriteLine(JsonSerializer.Serialize(payload, new JsonSerializerOptions
            {
                WriteIndented = true
            }));
        }
        else
        {
            System.Console.WriteLine($"File: {options.FilePath}");
            System.Console.WriteLine($"Status: {(result.IsValid ? "VALID" : "INVALID")}");
            if (!string.IsNullOrWhiteSpace(result.SchemaSource))
            {
                System.Console.WriteLine($"Schema: {result.SchemaSource}");
            }

            if (result.Errors.Count > 0)
            {
                System.Console.WriteLine("Errors:");
                foreach (var error in result.Errors)
                {
                    System.Console.WriteLine($"  - {error}");
                }
            }
        }

        return result.IsValid ? 0 : 1;
    }

    private static Options ParseArguments(string[] args)
    {
        var options = new Options();
        for (var i = 0; i < args.Length; i++)
        {
            var arg = args[i];
            switch (arg)
            {
                case "--file":
                case "-f":
                    options.FilePath = ReadValue(args, ref i, "--file");
                    break;
                case "--schema-dir":
                case "-s":
                    options.SchemaDir = ReadValue(args, ref i, "--schema-dir");
                    break;
                case "--json":
                    options.Json = true;
                    break;
                case "--help":
                case "-h":
                    options.ShowHelp = true;
                    break;
                default:
                    options.ShowHelp = true;
                    break;
            }
        }

        return options;
    }

    private static string ReadValue(string[] args, ref int index, string optionName)
    {
        if (index + 1 >= args.Length)
        {
            throw new ArgumentException($"Missing value for {optionName}.");
        }

        index += 1;
        return args[index];
    }

    private static void PrintUsage()
    {
        System.Console.WriteLine("NFOStandard .NET XML Toolkit");
        System.Console.WriteLine("Usage:");
        System.Console.WriteLine("  nfo-xml --file <path> [--schema-dir <path>] [--json]");
        System.Console.WriteLine();
        System.Console.WriteLine("Options:");
        System.Console.WriteLine("  --file, -f         XML file to validate");
        System.Console.WriteLine("  --schema-dir, -s   Directory with main.xsd and Schemas/");
        System.Console.WriteLine("  --json             Output results as JSON");
    }
}
