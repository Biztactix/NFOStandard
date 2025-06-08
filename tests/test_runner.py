#!/usr/bin/env python3
"""
NFO Standard Test Suite Runner
Runs validation tests on all test files and reports results.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess

# Add parent directory to path for validator import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools', 'python-validator'))

try:
    from nfo_validator import NFOValidator
except ImportError:
    print("Error: Could not import NFO validator. Make sure to run from the project root.")
    sys.exit(1)


class TestRunner:
    def __init__(self):
        self.validator = NFOValidator()
        self.results = {
            'valid': {'passed': 0, 'failed': 0, 'files': []},
            'invalid': {'passed': 0, 'failed': 0, 'files': []},
            'edge_cases': {'passed': 0, 'failed': 0, 'files': []}
        }
    
    def run_tests(self, test_dir: str):
        """Run all tests in the specified directory."""
        test_path = Path(test_dir)
        
        # Test valid files (should pass validation)
        valid_dir = test_path / 'valid'
        if valid_dir.exists():
            print("Testing valid files...")
            for file in valid_dir.glob('*.xml'):
                self._test_valid_file(file)
        
        # Test invalid files (should fail validation)
        invalid_dir = test_path / 'invalid'
        if invalid_dir.exists():
            print("\nTesting invalid files...")
            for file in invalid_dir.glob('*.xml'):
                self._test_invalid_file(file)
        
        # Test edge cases
        edge_dir = test_path / 'edge-cases'
        if edge_dir.exists():
            print("\nTesting edge cases...")
            for file in edge_dir.glob('*.xml'):
                self._test_edge_case_file(file)
        
        return self._generate_report()
    
    def _test_valid_file(self, filepath: Path):
        """Test a file that should be valid."""
        is_valid, errors = self.validator.validate_file(str(filepath))
        
        result = {
            'file': filepath.name,
            'valid': is_valid,
            'errors': errors
        }
        
        if is_valid:
            self.results['valid']['passed'] += 1
            print(f"  ✓ {filepath.name}")
        else:
            self.results['valid']['failed'] += 1
            print(f"  ✗ {filepath.name}")
            for error in errors:
                print(f"    - {error}")
        
        self.results['valid']['files'].append(result)
    
    def _test_invalid_file(self, filepath: Path):
        """Test a file that should be invalid."""
        is_valid, errors = self.validator.validate_file(str(filepath))
        
        # Extract expected error from file comments
        expected_error = self._extract_expected_error(filepath)
        
        result = {
            'file': filepath.name,
            'valid': is_valid,
            'errors': errors,
            'expected_error': expected_error
        }
        
        if not is_valid:
            self.results['invalid']['passed'] += 1
            print(f"  ✓ {filepath.name} (correctly failed)")
            if expected_error:
                # Check if expected error is in actual errors
                error_found = any(expected_error.lower() in error.lower() for error in errors)
                if not error_found:
                    print(f"    ⚠️  Expected error not found: {expected_error}")
        else:
            self.results['invalid']['failed'] += 1
            print(f"  ✗ {filepath.name} (should have failed)")
        
        self.results['invalid']['files'].append(result)
    
    def _test_edge_case_file(self, filepath: Path):
        """Test an edge case file."""
        try:
            is_valid, errors = self.validator.validate_file(str(filepath))
            
            result = {
                'file': filepath.name,
                'valid': is_valid,
                'errors': errors
            }
            
            if is_valid:
                self.results['edge_cases']['passed'] += 1
                print(f"  ✓ {filepath.name}")
            else:
                self.results['edge_cases']['failed'] += 1
                print(f"  ✗ {filepath.name}")
                for error in errors:
                    print(f"    - {error}")
            
            self.results['edge_cases']['files'].append(result)
        except Exception as e:
            self.results['edge_cases']['failed'] += 1
            print(f"  ✗ {filepath.name} (exception: {str(e)})")
            self.results['edge_cases']['files'].append({
                'file': filepath.name,
                'valid': False,
                'errors': [f"Exception: {str(e)}"]
            })
    
    def _extract_expected_error(self, filepath: Path) -> str:
        """Extract expected error message from file comments."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for "Expected error:" in comments
                import re
                match = re.search(r'Expected error:\s*(.+?)\s*-->', content)
                if match:
                    return match.group(1).strip()
        except:
            pass
        return ""
    
    def _generate_report(self) -> Dict:
        """Generate a test report."""
        total_tests = 0
        total_passed = 0
        
        for category in self.results.values():
            total_tests += category['passed'] + category['failed']
            total_passed += category['passed']
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'passed': total_passed,
                'failed': total_tests - total_passed,
                'pass_rate': f"{(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "0%"
            },
            'categories': self.results
        }
        
        return report


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run NFO Standard test suite')
    parser.add_argument('test_dir', nargs='?', default='tests',
                       help='Directory containing test files')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Check if test directory exists
    if not os.path.exists(args.test_dir):
        print(f"Error: Test directory '{args.test_dir}' not found")
        sys.exit(1)
    
    # Run tests
    runner = TestRunner()
    report = runner.run_tests(args.test_dir)
    
    # Output results
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        summary = report['summary']
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Pass Rate: {summary['pass_rate']}")
        
        print("\nBy Category:")
        print(f"  Valid Files: {report['categories']['valid']['passed']}/{report['categories']['valid']['passed'] + report['categories']['valid']['failed']}")
        print(f"  Invalid Files: {report['categories']['invalid']['passed']}/{report['categories']['invalid']['passed'] + report['categories']['invalid']['failed']}")
        print(f"  Edge Cases: {report['categories']['edge_cases']['passed']}/{report['categories']['edge_cases']['passed'] + report['categories']['edge_cases']['failed']}")
    
    # Exit with appropriate code
    sys.exit(0 if summary['failed'] == 0 else 1)


if __name__ == "__main__":
    main()