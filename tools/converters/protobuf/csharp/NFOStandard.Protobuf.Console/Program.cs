using System;
using System.CommandLine;
using System.IO;
using System.Threading.Tasks;
using NFOStandard.Protobuf.Converter;

namespace NFOStandard.Protobuf.Console
{
    class Program
    {
        static async Task<int> Main(string[] args)
        {
            var rootCommand = new RootCommand("NFOStandard Protocol Buffer Converter");

            var convertCommand = new Command("convert", "Convert between XML and Protocol Buffer formats");
            
            var inputOption = new Option<FileInfo>(
                new[] { "--input", "-i" },
                "Input file path")
            {
                IsRequired = true
            };

            var outputOption = new Option<FileInfo>(
                new[] { "--output", "-o" },
                "Output file path")
            {
                IsRequired = true
            };

            var formatOption = new Option<ConversionFormat>(
                new[] { "--format", "-f" },
                getDefaultValue: () => ConversionFormat.Auto,
                "Conversion format (auto, xml-to-pb, pb-to-xml)");

            convertCommand.AddOption(inputOption);
            convertCommand.AddOption(outputOption);
            convertCommand.AddOption(formatOption);

            convertCommand.SetHandler(async (inputFile, outputFile, format) =>
            {
                await ConvertFile(inputFile!, outputFile!, format);
            }, inputOption, outputOption, formatOption);

            rootCommand.AddCommand(convertCommand);

            // Validate command
            var validateCommand = new Command("validate", "Validate an NFO file");
            var validateFileOption = new Option<FileInfo>(
                new[] { "--file", "-f" },
                "File to validate")
            {
                IsRequired = true
            };

            validateCommand.AddOption(validateFileOption);
            validateCommand.SetHandler(async (file) =>
            {
                await ValidateFile(file!);
            }, validateFileOption);

            rootCommand.AddCommand(validateCommand);

            return await rootCommand.InvokeAsync(args);
        }

        static async Task ConvertFile(FileInfo input, FileInfo output, ConversionFormat format)
        {
            try
            {
                if (!input.Exists)
                {
                    System.Console.WriteLine($"Error: Input file '{input.FullName}' does not exist.");
                    return;
                }

                // Auto-detect format if needed
                if (format == ConversionFormat.Auto)
                {
                    format = DetectFormat(input.Extension);
                }

                switch (format)
                {
                    case ConversionFormat.XmlToProtobuf:
                        await ConvertXmlToProtobuf(input, output);
                        break;
                    case ConversionFormat.ProtobufToXml:
                        await ConvertProtobufToXml(input, output);
                        break;
                    default:
                        System.Console.WriteLine("Error: Unable to determine conversion format.");
                        break;
                }
            }
            catch (Exception ex)
            {
                System.Console.WriteLine($"Error during conversion: {ex.Message}");
            }
        }

        static async Task ConvertXmlToProtobuf(FileInfo input, FileInfo output)
        {
            System.Console.WriteLine($"Converting XML to Protocol Buffer...");
            System.Console.WriteLine($"Input: {input.FullName}");
            System.Console.WriteLine($"Output: {output.FullName}");

            var xmlContent = await File.ReadAllTextAsync(input.FullName);
            var nfoRoot = NFOConverter.XmlToProtobuf(xmlContent);
            
            NFOConverter.SaveProtobuf(nfoRoot, output.FullName);
            
            System.Console.WriteLine($"Conversion complete. Output size: {new FileInfo(output.FullName).Length} bytes");
        }

        static async Task ConvertProtobufToXml(FileInfo input, FileInfo output)
        {
            System.Console.WriteLine($"Converting Protocol Buffer to XML...");
            System.Console.WriteLine($"Input: {input.FullName}");
            System.Console.WriteLine($"Output: {output.FullName}");

            var nfoRoot = NFOConverter.LoadProtobuf(input.FullName);
            var xmlContent = NFOConverter.ProtobufToXml(nfoRoot);
            
            await File.WriteAllTextAsync(output.FullName, xmlContent);
            
            System.Console.WriteLine($"Conversion complete. Output size: {new FileInfo(output.FullName).Length} bytes");
        }

        static async Task ValidateFile(FileInfo file)
        {
            try
            {
                System.Console.WriteLine($"Validating {file.FullName}...");

                if (file.Extension.ToLower() == ".xml" || file.Extension.ToLower() == ".nfo")
                {
                    var xmlContent = await File.ReadAllTextAsync(file.FullName);
                    var nfoRoot = NFOConverter.XmlToProtobuf(xmlContent);
                    
                    System.Console.WriteLine("✓ Valid NFO XML file");
                    System.Console.WriteLine($"  Media type: {nfoRoot.Media?.MediaTypeCase}");
                    
                    switch (nfoRoot.Media?.MediaTypeCase)
                    {
                        case NFOStandard.Protobuf.Media.MediaTypeOneofCase.Movie:
                            System.Console.WriteLine($"  Title: {nfoRoot.Media.Movie.Title}");
                            System.Console.WriteLine($"  Year: {nfoRoot.Media.Movie.Year}");
                            break;
                        case NFOStandard.Protobuf.Media.MediaTypeOneofCase.Tvshow:
                            System.Console.WriteLine($"  Title: {nfoRoot.Media.Tvshow.Title}");
                            break;
                        case NFOStandard.Protobuf.Media.MediaTypeOneofCase.Music:
                            System.Console.WriteLine($"  Title: {nfoRoot.Media.Music.Title}");
                            System.Console.WriteLine($"  Artist: {nfoRoot.Media.Music.Artist}");
                            break;
                    }
                }
                else
                {
                    var nfoRoot = NFOConverter.LoadProtobuf(file.FullName);
                    System.Console.WriteLine("✓ Valid Protocol Buffer file");
                    System.Console.WriteLine($"  Media type: {nfoRoot.Media?.MediaTypeCase}");
                }
            }
            catch (Exception ex)
            {
                System.Console.WriteLine($"✗ Validation failed: {ex.Message}");
            }
        }

        static ConversionFormat DetectFormat(string extension)
        {
            return extension.ToLower() switch
            {
                ".xml" or ".nfo" => ConversionFormat.XmlToProtobuf,
                ".nfpb" or ".pb" => ConversionFormat.ProtobufToXml,
                _ => ConversionFormat.Auto
            };
        }
    }

    enum ConversionFormat
    {
        Auto,
        XmlToProtobuf,
        ProtobufToXml
    }
}