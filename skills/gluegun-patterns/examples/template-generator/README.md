# Template Generator Example

Advanced template patterns for Gluegun CLI generators.

## Structure

```
template-generator/
├── src/
│   └── commands/
│       ├── new-app.ts          # Multi-file generator
│       ├── new-feature.ts      # Feature scaffold
│       └── new-config.ts       # Config generator
├── templates/
│   ├── app/
│   │   ├── package.json.ejs
│   │   ├── tsconfig.json.ejs
│   │   ├── src/
│   │   │   └── index.ts.ejs
│   │   └── README.md.ejs
│   ├── feature/
│   │   ├── component.tsx.ejs
│   │   ├── test.spec.ts.ejs
│   │   └── styles.css.ejs
│   └── config/
│       └── config.json.ejs
└── README.md
```

## Features

- Multi-file generation from template sets
- Conditional template sections
- Nested directory creation
- Template composition
- Helper functions for common operations

## Patterns

### 1. Multi-File Generation

Generate complete project structure:

```typescript
await template.generate({
  template: 'app/package.json.ejs',
  target: `${name}/package.json`,
  props: { name, version }
})

await template.generate({
  template: 'app/src/index.ts.ejs',
  target: `${name}/src/index.ts`,
  props: { name }
})
```

### 2. Conditional Templates

Templates with conditional sections:

```ejs
<% if (includeTests) { %>
import { test } from 'vitest'

test('<%= name %> works', () => {
  // Test implementation
})
<% } %>
```

### 3. Template Loops

Generate repetitive structures:

```ejs
<% features.forEach(feature => { %>
export { <%= feature.name %> } from './<%= feature.path %>'
<% }) %>
```

### 4. Nested Templates

Organize templates in directories:

```
templates/
├── react-app/
│   ├── components/
│   │   └── Component.tsx.ejs
│   ├── pages/
│   │   └── Page.tsx.ejs
│   └── layouts/
│       └── Layout.tsx.ejs
```

### 5. Template Helpers

Use helper functions in templates:

```ejs
/**
 * <%= helpers.titleCase(name) %> Component
 * File: <%= helpers.kebabCase(name) %>.ts
 */

export class <%= helpers.pascalCase(name) %> {
  // Implementation
}
```

## Commands

### new-app

Create complete application structure:

```bash
./bin/cli new-app my-project --typescript --tests
```

Options:
- `--typescript`: Include TypeScript configuration
- `--tests`: Include test setup
- `--git`: Initialize git repository
- `--install`: Run npm install

### new-feature

Scaffold a new feature with tests and styles:

```bash
./bin/cli new-feature UserProfile --redux --tests
```

Options:
- `--redux`: Include Redux setup
- `--tests`: Generate test files
- `--styles`: Include CSS/SCSS files

### new-config

Generate configuration files:

```bash
./bin/cli new-config --eslint --prettier --jest
```

Options:
- `--eslint`: ESLint configuration
- `--prettier`: Prettier configuration
- `--jest`: Jest configuration
- `--typescript`: TypeScript configuration

## Template Variables

### Common Props

```typescript
{
  name: string              // Component/project name
  description: string       // Description
  author: string           // Author name
  version: string          // Version number
  timestamp: string        // ISO timestamp
  year: number            // Current year
}
```

### Feature-Specific Props

```typescript
{
  // React component
  componentType: 'class' | 'function'
  withHooks: boolean
  withState: boolean

  // Configuration
  includeESLint: boolean
  includePrettier: boolean
  includeTests: boolean

  // Dependencies
  dependencies: string[]
  devDependencies: string[]
}
```

## Advanced Techniques

### 1. Template Composition

Combine multiple templates:

```typescript
// Base component template
await template.generate({
  template: 'base/component.ts.ejs',
  target: 'src/components/Base.ts',
  props: baseProps
})

// Extended component using base
await template.generate({
  template: 'extended/component.ts.ejs',
  target: 'src/components/Extended.ts',
  props: { ...baseProps, extends: 'Base' }
})
```

### 2. Dynamic Template Selection

Choose templates based on user input:

```typescript
const framework = await prompt.select('Framework:', [
  'React',
  'Vue',
  'Angular'
])

const templatePath = `${framework.toLowerCase()}/component.ejs`
await template.generate({
  template: templatePath,
  target: `src/components/${name}.tsx`,
  props: { name }
})
```

### 3. Template Preprocessing

Modify props before generation:

```typescript
const props = {
  name,
  pascalName: strings.pascalCase(name),
  kebabName: strings.kebabCase(name),
  dependencies: dependencies.sort(),
  imports: generateImports(dependencies)
}

await template.generate({
  template: 'component.ts.ejs',
  target: `src/${props.kebabName}.ts`,
  props
})
```

### 4. Post-Generation Actions

Run actions after template generation:

```typescript
// Generate files
await template.generate({ /* ... */ })

// Format generated code
await system.run('npm run format')

// Run initial build
await system.run('npm run build')

// Initialize git
if (options.git) {
  await system.run('git init')
  await system.run('git add .')
  await system.run('git commit -m "Initial commit"')
}
```

### 5. Template Validation

Validate templates before generation:

```typescript
// Check if template exists
if (!filesystem.exists(`templates/${templatePath}`)) {
  print.error(`Template not found: ${templatePath}`)
  return
}

// Validate template syntax
const templateContent = await filesystem.read(`templates/${templatePath}`)
if (!validateEJS(templateContent)) {
  print.error('Invalid EJS syntax in template')
  return
}
```

## Best Practices

1. **Organize Templates**: Group related templates in directories
2. **Use Helpers**: Extract common logic into helper functions
3. **Validate Input**: Check user input before generation
4. **Provide Feedback**: Show progress with spinners
5. **Handle Errors**: Gracefully handle missing templates
6. **Document Variables**: Comment template variables
7. **Test Templates**: Generate samples to verify output

## Testing Generated Code

```bash
# Generate sample
./bin/cli new-app test-project --all

# Verify structure
cd test-project
npm install
npm test
npm run build
```

## Template Development Workflow

1. Create template file with `.ejs` extension
2. Add template variables with `<%= %>` syntax
3. Test template with sample props
4. Add conditional sections with `<% if %>` blocks
5. Validate generated output
6. Document template variables and options
