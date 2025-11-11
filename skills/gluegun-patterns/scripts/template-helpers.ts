/**
 * Template Helper Functions for Gluegun
 * Useful utilities for EJS templates
 */

/**
 * String case conversions
 */
export const caseConverters = {
  /**
   * Convert to PascalCase
   * Example: "hello-world" => "HelloWorld"
   */
  pascalCase: (str: string): string => {
    return str
      .replace(/[-_\s](.)/g, (_, char) => char.toUpperCase())
      .replace(/^(.)/, (_, char) => char.toUpperCase())
  },

  /**
   * Convert to camelCase
   * Example: "hello-world" => "helloWorld"
   */
  camelCase: (str: string): string => {
    return str
      .replace(/[-_\s](.)/g, (_, char) => char.toUpperCase())
      .replace(/^(.)/, (_, char) => char.toLowerCase())
  },

  /**
   * Convert to kebab-case
   * Example: "HelloWorld" => "hello-world"
   */
  kebabCase: (str: string): string => {
    return str
      .replace(/([a-z])([A-Z])/g, '$1-$2')
      .replace(/[\s_]+/g, '-')
      .toLowerCase()
  },

  /**
   * Convert to snake_case
   * Example: "HelloWorld" => "hello_world"
   */
  snakeCase: (str: string): string => {
    return str
      .replace(/([a-z])([A-Z])/g, '$1_$2')
      .replace(/[\s-]+/g, '_')
      .toLowerCase()
  },

  /**
   * Convert to Title Case
   * Example: "hello world" => "Hello World"
   */
  titleCase: (str: string): string => {
    return str
      .toLowerCase()
      .split(/[\s-_]+/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }
}

/**
 * Pluralization helpers
 */
export const pluralize = {
  /**
   * Simple pluralization
   */
  plural: (word: string): string => {
    if (word.endsWith('y')) {
      return word.slice(0, -1) + 'ies'
    }
    if (word.endsWith('s') || word.endsWith('x') || word.endsWith('z')) {
      return word + 'es'
    }
    return word + 's'
  },

  /**
   * Simple singularization
   */
  singular: (word: string): string => {
    if (word.endsWith('ies')) {
      return word.slice(0, -3) + 'y'
    }
    if (word.endsWith('es')) {
      return word.slice(0, -2)
    }
    if (word.endsWith('s')) {
      return word.slice(0, -1)
    }
    return word
  }
}

/**
 * File path helpers
 */
export const pathHelpers = {
  /**
   * Convert name to file path
   * Example: "UserProfile" => "user-profile.ts"
   */
  toFilePath: (name: string, extension: string = 'ts'): string => {
    const kebab = caseConverters.kebabCase(name)
    return `${kebab}.${extension}`
  },

  /**
   * Convert name to directory path
   * Example: "UserProfile" => "user-profile"
   */
  toDirPath: (name: string): string => {
    return caseConverters.kebabCase(name)
  }
}

/**
 * Comment generators
 */
export const comments = {
  /**
   * Generate file header comment
   */
  fileHeader: (filename: string, description: string, author?: string): string => {
    const lines = [
      '/**',
      ` * ${filename}`,
      ` * ${description}`,
    ]

    if (author) {
      lines.push(` * @author ${author}`)
    }

    lines.push(` * @generated ${new Date().toISOString()}`)
    lines.push(' */')

    return lines.join('\n')
  },

  /**
   * Generate JSDoc comment
   */
  jsDoc: (description: string, params?: Array<{ name: string; type: string; description: string }>, returns?: string): string => {
    const lines = [
      '/**',
      ` * ${description}`
    ]

    if (params && params.length > 0) {
      lines.push(' *')
      params.forEach(param => {
        lines.push(` * @param {${param.type}} ${param.name} - ${param.description}`)
      })
    }

    if (returns) {
      lines.push(' *')
      lines.push(` * @returns {${returns}}`)
    }

    lines.push(' */')

    return lines.join('\n')
  }
}

/**
 * Import statement generators
 */
export const imports = {
  /**
   * Generate TypeScript import
   */
  typescript: (items: string[], from: string): string => {
    if (items.length === 1) {
      return `import { ${items[0]} } from '${from}'`
    }
    return `import {\n  ${items.join(',\n  ')}\n} from '${from}'`
  },

  /**
   * Generate CommonJS require
   */
  commonjs: (name: string, from: string): string => {
    return `const ${name} = require('${from}')`
  }
}

/**
 * Code formatting helpers
 */
export const formatting = {
  /**
   * Indent text by specified spaces
   */
  indent: (text: string, spaces: number = 2): string => {
    const indent = ' '.repeat(spaces)
    return text
      .split('\n')
      .map(line => indent + line)
      .join('\n')
  },

  /**
   * Wrap text in quotes
   */
  quote: (text: string, style: 'single' | 'double' = 'single'): string => {
    const quote = style === 'single' ? "'" : '"'
    return `${quote}${text}${quote}`
  }
}

/**
 * Validation helpers
 */
export const validate = {
  /**
   * Check if string is valid identifier
   */
  isValidIdentifier: (str: string): boolean => {
    return /^[a-zA-Z_$][a-zA-Z0-9_$]*$/.test(str)
  },

  /**
   * Check if string is valid package name
   */
  isValidPackageName: (str: string): boolean => {
    return /^(@[a-z0-9-~][a-z0-9-._~]*\/)?[a-z0-9-~][a-z0-9-._~]*$/.test(str)
  }
}

/**
 * All helpers combined for easy import
 */
export const helpers = {
  ...caseConverters,
  pluralize,
  pathHelpers,
  comments,
  imports,
  formatting,
  validate
}

export default helpers
