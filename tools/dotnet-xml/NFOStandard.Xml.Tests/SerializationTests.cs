using System;
using System.IO;
using Xunit;

namespace NFOStandard.Xml.Tests;

public sealed class SerializationTests
{
    [Fact]
    public void LoadSaveValidateMovie()
    {
        var repoRoot = FindRepoRoot();
        var inputPath = Path.Combine(repoRoot, "ExampleMovie.xml");
        Assert.True(File.Exists(inputPath), $"Missing input file: {inputPath}");

        var root = NfoSerializer.Load(inputPath);
        Assert.NotNull(root.Media.Movie);
        root.Media.Movie!.Title = "Updated Title";

        var outputPath = Path.Combine(Path.GetTempPath(), $"nfo_movie_{Guid.NewGuid()}.xml");
        NfoSerializer.Save(root, outputPath);

        try
        {
            var validator = new NfoValidator();
            var result = validator.ValidateFile(outputPath);
            Assert.True(result.IsValid, string.Join(Environment.NewLine, result.Errors));
        }
        finally
        {
            if (File.Exists(outputPath))
            {
                File.Delete(outputPath);
            }
        }
    }

    private static string FindRepoRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current != null)
        {
            if (Directory.Exists(Path.Combine(current.FullName, ".git")))
            {
                return current.FullName;
            }

            current = current.Parent;
        }

        throw new DirectoryNotFoundException("Could not locate repository root.");
    }
}
