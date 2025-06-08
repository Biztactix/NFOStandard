#!/usr/bin/env node

const { program } = require('commander');
const chalk = require('chalk');
const ora = require('ora');
const path = require('path');
const fs = require('fs');
const { NFOValidator } = require('../lib/validator');

program
  .name('nfo-validator')
  .description('Validate NFO files against the NFO Standard')
  .version('1.0.0')
  .argument('<files...>', 'NFO files or directories to validate')
  .option('-s, --strict', 'Enable strict validation (check recommended fields)')
  .option('-r, --recursive', 'Recursively validate directories')
  .option('-f, --format <format>', 'Output format (text, json, xml)', 'text')
  .option('--offline', 'Use offline validation with local schemas')
  .option('--schema-dir <dir>', 'Directory containing local schema files')
  .option('-q, --quiet', 'Only show files with errors')
  .option('-w, --watch', 'Watch files for changes and auto-validate')
  .action(async (files, options) => {
    const validator = new NFOValidator({
      strict: options.strict,
      offline: options.offline,
      schemaDir: options.schemaDir
    });

    let allValid = true;
    const spinner = ora('Validating files...').start();

    try {
      for (const file of files) {
        const stats = fs.statSync(file);
        
        if (stats.isDirectory()) {
          spinner.text = `Validating directory: ${file}`;
          const results = await validator.validateDirectory(
            file, 
            '**/*.nfo',
            options.recursive
          );
          
          for (const [filepath, result] of results) {
            if (!result.isValid) allValid = false;
            if (!options.quiet || !result.isValid) {
              spinner.stop();
              displayResult(filepath, result, options.format);
              spinner.start();
            }
          }
        } else {
          spinner.text = `Validating: ${file}`;
          const result = await validator.validateFile(file);
          if (!result.isValid) allValid = false;
          
          if (!options.quiet || !result.isValid) {
            spinner.stop();
            displayResult(file, result, options.format);
            spinner.start();
          }
        }
      }
      
      spinner.stop();
      
      if (allValid) {
        console.log(chalk.green('\n✓ All files are valid!'));
      } else {
        console.log(chalk.red('\n✗ Some files have validation errors.'));
        process.exit(1);
      }
      
    } catch (error) {
      spinner.stop();
      console.error(chalk.red(`Error: ${error.message}`));
      process.exit(1);
    }

    // Watch mode
    if (options.watch) {
      console.log(chalk.blue('\nWatching for changes...'));
      const chokidar = require('chokidar');
      
      const watcher = chokidar.watch(files, {
        persistent: true,
        ignoreInitial: true
      });
      
      watcher.on('change', async (filepath) => {
        console.log(chalk.yellow(`\nFile changed: ${filepath}`));
        const result = await validator.validateFile(filepath);
        displayResult(filepath, result, options.format);
      });
    }
  });

function displayResult(filepath, result, format) {
  if (format === 'json') {
    console.log(JSON.stringify({
      file: filepath,
      valid: result.isValid,
      errors: result.errors,
      warnings: result.warnings
    }, null, 2));
  } else if (format === 'xml') {
    let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
    xml += '<validation>\n';
    xml += `  <file>${filepath}</file>\n`;
    xml += `  <valid>${result.isValid}</valid>\n`;
    if (result.errors.length > 0) {
      xml += '  <errors>\n';
      for (const error of result.errors) {
        xml += `    <error line="${error.line || ''}" column="${error.column || ''}">${error.message}</error>\n`;
      }
      xml += '  </errors>\n';
    }
    if (result.warnings && result.warnings.length > 0) {
      xml += '  <warnings>\n';
      for (const warning of result.warnings) {
        xml += `    <warning>${warning}</warning>\n`;
      }
      xml += '  </warnings>\n';
    }
    xml += '</validation>';
    console.log(xml);
  } else {
    // Text format
    console.log('\n' + '='.repeat(60));
    console.log(`File: ${chalk.blue(filepath)}`);
    
    if (result.isValid) {
      console.log(`Status: ${chalk.green('VALID')} ✓`);
    } else {
      console.log(`Status: ${chalk.red('INVALID')} ✗`);
      console.log(chalk.red('Errors:'));
      for (const error of result.errors) {
        let errorMsg = `  - ${error.message}`;
        if (error.line) {
          errorMsg += ` (line ${error.line}`;
          if (error.column) {
            errorMsg += `, column ${error.column}`;
          }
          errorMsg += ')';
        }
        console.log(chalk.red(errorMsg));
      }
    }
    
    if (result.warnings && result.warnings.length > 0) {
      console.log(chalk.yellow('Warnings:'));
      for (const warning of result.warnings) {
        console.log(chalk.yellow(`  - ${warning}`));
      }
    }
  }
}

// Parse command line arguments
program.parse();