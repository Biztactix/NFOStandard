#!/usr/bin/env python3
import re
import subprocess
import unittest
from pathlib import Path
from xml.etree import ElementTree


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = PROJECT_ROOT / 'plugins' / 'emby-jellyfin' / 'NFOStandard'
PLUGIN_CSPROJ = PLUGIN_DIR / 'NFOStandard.csproj'
PLUGIN_XML = PLUGIN_DIR / 'plugin.xml'
PLUGIN_MAIN = PLUGIN_DIR / 'NFOStandardPlugin.cs'


def _run_build(target_framework: str) -> None:
    command = [
        'dotnet',
        'build',
        str(PLUGIN_CSPROJ),
        '-f',
        target_framework,
        '-c',
        'Release',
        '--nologo',
    ]
    subprocess.run(command, check=True, cwd=PROJECT_ROOT)


class PluginBuildTests(unittest.TestCase):
    def test_builds_for_jellyfin_net8(self):
        _run_build('net8.0')

    def test_builds_for_emby_netstandard(self):
        _run_build('netstandard2.0')


class PluginXmlTests(unittest.TestCase):
    def test_plugin_xml_fields_match_plugin(self):
        xml_tree = ElementTree.parse(PLUGIN_XML)
        xml_root = xml_tree.getroot()

        guid = (xml_root.findtext('guid') or '').strip()
        name = (xml_root.findtext('name') or '').strip()
        description = (xml_root.findtext('description') or '').strip()
        assembly_filename = (xml_root.findtext('assemblyFilename') or '').strip()
        target_abi = (xml_root.findtext('targetAbi') or '').strip()
        minimum_version = (xml_root.findtext('minimumVersion') or '').strip()

        self.assertTrue(guid, 'plugin.xml guid is required')
        self.assertTrue(name, 'plugin.xml name is required')
        self.assertTrue(description, 'plugin.xml description is required')
        self.assertTrue(assembly_filename, 'plugin.xml assemblyFilename is required')
        self.assertTrue(target_abi, 'plugin.xml targetAbi is required')
        self.assertTrue(minimum_version, 'plugin.xml minimumVersion is required')

        csproj_tree = ElementTree.parse(PLUGIN_CSPROJ)
        csproj_root = csproj_tree.getroot()
        assembly_name = csproj_root.findtext('.//AssemblyName') or 'NFOStandard'
        self.assertEqual(f'{assembly_name}.dll', assembly_filename)

        plugin_source = PLUGIN_MAIN.read_text(encoding='utf-8')
        guid_match = re.search(r'Guid\.Parse\("([0-9a-fA-F-]+)"\)', plugin_source)
        self.assertIsNotNone(guid_match, 'Plugin Id guid not found in source')
        self.assertEqual(guid_match.group(1), guid)

        name_match = re.search(r'public override string Name => "([^"]+)";', plugin_source)
        self.assertIsNotNone(name_match, 'Plugin Name not found in source')
        self.assertEqual(name_match.group(1), name)

        description_match = re.search(r'public override string Description => "([^"]+)";', plugin_source)
        self.assertIsNotNone(description_match, 'Plugin Description not found in source')
        self.assertEqual(description_match.group(1), description)

        self.assertTrue(_version_tuple(minimum_version) <= _version_tuple(target_abi))


def _version_tuple(value: str):
    parts = [int(part) for part in value.split('.') if part.isdigit()]
    while len(parts) < 4:
        parts.append(0)
    return tuple(parts[:4])


if __name__ == '__main__':
    unittest.main()
