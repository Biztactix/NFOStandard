import * as fs from 'fs';
import * as path from 'path';
import axios from 'axios';
import * as libxmljs from 'libxmljs2';
import { glob } from 'glob';

export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings?: string[];
}

export interface ValidationError {
  message: string;
  line?: number;
  column?: number;
  level: 'error' | 'warning';
}

export interface ValidatorOptions {
  strict?: boolean;
  offline?: boolean;
  schemaDir?: string;
  skipContent?: boolean;
}

export class NFOValidator {
  private schemaCache: Map<string, libxmljs.Document> = new Map();
  private options: ValidatorOptions;

  constructor(options: ValidatorOptions = {}) {
    this.options = options;
  }

  async validateFile(filepath: string): Promise<ValidationResult> {
    const errors: ValidationError[] = [];
    const warnings: string[] = [];

    try {
      // Read the file
      const content = fs.readFileSync(filepath, 'utf-8');
      
      // Parse XML
      let xmlDoc: libxmljs.Document;
      try {
        xmlDoc = libxmljs.parseXml(content);
      } catch (parseError: any) {
        errors.push({
          message: `XML parsing error: ${parseError.message}`,
          line: parseError.line,
          column: parseError.column,
          level: 'error'
        });
        return { isValid: false, errors };
      }

      // Get schema location
      const root = xmlDoc.root();
      if (!root) {
        errors.push({
          message: 'No root element found',
          level: 'error'
        });
        return { isValid: false, errors };
      }

      const schemaLocation = root.attr('xsi:schemaLocation')?.value();
      if (!schemaLocation) {
        errors.push({
          message: 'No xsi:schemaLocation attribute found',
          level: 'error'
        });
        return { isValid: false, errors };
      }

      // Extract schema URL
      const schemaUrl = schemaLocation.split(' ')[1];
      if (!schemaUrl) {
        errors.push({
          message: 'Invalid xsi:schemaLocation format',
          level: 'error'
        });
        return { isValid: false, errors };
      }

      // Load and validate against schema
      const schema = await this.loadSchema(schemaUrl);
      const validationErrors = xmlDoc.validate(schema);
      
      if (validationErrors !== true) {
        const xmlErrors = xmlDoc.validationErrors;
        for (const error of xmlErrors) {
          errors.push({
            message: error.message || 'Unknown validation error',
            line: error.line,
            column: error.column,
            level: 'error'
          });
        }
      }

      // Strict validation
      if (this.options.strict && errors.length === 0) {
        const strictWarnings = this.performStrictValidation(xmlDoc);
        warnings.push(...strictWarnings);
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings: warnings.length > 0 ? warnings : undefined
      };

    } catch (error: any) {
      errors.push({
        message: `Unexpected error: ${error.message}`,
        level: 'error'
      });
      return { isValid: false, errors };
    }
  }

  async validateString(content: string): Promise<ValidationResult> {
    // Create a temporary file
    const tmpFile = path.join(process.cwd(), `.tmp-nfo-${Date.now()}.xml`);
    fs.writeFileSync(tmpFile, content);
    
    try {
      return await this.validateFile(tmpFile);
    } finally {
      // Clean up
      if (fs.existsSync(tmpFile)) {
        fs.unlinkSync(tmpFile);
      }
    }
  }

  async validateDirectory(
    directory: string, 
    pattern: string = '**/*.nfo',
    recursive: boolean = true
  ): Promise<Map<string, ValidationResult>> {
    const results = new Map<string, ValidationResult>();
    
    const files = await glob(pattern, {
      cwd: directory,
      absolute: true,
      nodir: true
    });

    for (const file of files) {
      const result = await this.validateFile(file);
      results.set(file, result);
    }

    return results;
  }

  private async loadSchema(schemaUrl: string): Promise<libxmljs.Document> {
    if (this.schemaCache.has(schemaUrl)) {
      return this.schemaCache.get(schemaUrl)!;
    }

    let schemaContent: string;

    if (this.options.offline && this.options.schemaDir) {
      // Load from local file
      const schemaFilename = path.basename(new URL(schemaUrl).pathname);
      const schemaPath = path.join(this.options.schemaDir, schemaFilename);
      schemaContent = fs.readFileSync(schemaPath, 'utf-8');
    } else {
      // Load from URL
      const response = await axios.get(schemaUrl, { timeout: 10000 });
      schemaContent = response.data;
    }

    const schemaDoc = libxmljs.parseXml(schemaContent);
    this.schemaCache.set(schemaUrl, schemaDoc);
    return schemaDoc;
  }

  private performStrictValidation(xmlDoc: libxmljs.Document): string[] {
    const warnings: string[] = [];
    const root = xmlDoc.root();
    
    if (!root) return warnings;

    // Find media element
    const mediaElement = root.get('//media', { 'default': 'NFOStandard' });
    if (!mediaElement) return warnings;

    // Check different media types
    const mediaTypes = ['movie', 'tvshow', 'music', 'audiobook', 'podcast'];
    for (const mediaType of mediaTypes) {
      const element = mediaElement.get(`.//${mediaType}`, { 'default': 'NFOStandard' });
      if (element) {
        const typeWarnings = this.checkRecommendedFields(element, mediaType);
        warnings.push(...typeWarnings);
      }
    }

    return warnings;
  }

  private checkRecommendedFields(element: libxmljs.Element, mediaType: string): string[] {
    const warnings: string[] = [];
    
    const recommendedFields: Record<string, string[]> = {
      movie: ['year', 'runtime', 'genre', 'director', 'actor', 'plot'],
      tvshow: ['year', 'genre', 'actor', 'plot', 'season', 'episode'],
      music: ['artist', 'album', 'year', 'genre'],
      audiobook: ['author', 'narrator', 'publisher', 'year'],
      podcast: ['author', 'category', 'pubDate', 'duration']
    };

    const fields = recommendedFields[mediaType] || [];
    for (const field of fields) {
      if (!element.get(`.//${field}`, { 'default': 'NFOStandard' })) {
        warnings.push(`Recommended field '${field}' is missing for ${mediaType}`);
      }
    }

    return warnings;
  }
}

// Export convenience functions
export async function validateNFO(filepath: string, options?: ValidatorOptions): Promise<boolean> {
  const validator = new NFOValidator(options);
  const result = await validator.validateFile(filepath);
  return result.isValid;
}

export async function parseNFO(filepath: string): Promise<any> {
  const content = fs.readFileSync(filepath, 'utf-8');
  const xmlDoc = libxmljs.parseXml(content);
  
  // Convert to JSON-like structure
  return xmlToJson(xmlDoc.root());
}

function xmlToJson(element: libxmljs.Element | null): any {
  if (!element) return null;
  
  const obj: any = {};
  
  // Add attributes
  const attrs = element.attrs();
  if (attrs.length > 0) {
    obj['@attributes'] = {};
    for (const attr of attrs) {
      obj['@attributes'][attr.name()] = attr.value();
    }
  }
  
  // Add child elements
  const children = element.childNodes();
  for (const child of children) {
    if (child.type() === 'element') {
      const childElement = child as libxmljs.Element;
      const name = childElement.name();
      const value = xmlToJson(childElement);
      
      if (obj[name]) {
        // Convert to array if multiple elements with same name
        if (!Array.isArray(obj[name])) {
          obj[name] = [obj[name]];
        }
        obj[name].push(value);
      } else {
        obj[name] = value;
      }
    } else if (child.type() === 'text') {
      const text = child.toString().trim();
      if (text && Object.keys(obj).length === 0) {
        return text;
      } else if (text) {
        obj['#text'] = text;
      }
    }
  }
  
  return obj;
}