# Gluegun Plugin System Example

Demonstrates how to build an extensible CLI with plugin architecture.

## Structure

```
plugin-system/
├── src/
│   ├── cli.ts              # CLI with plugin loading
│   ├── commands/
│   │   └── plugin.ts       # Plugin management command
│   └── plugins/
│       ├── custom-plugin.ts    # Example plugin
│       └── validator-plugin.ts # Validation plugin
├── package.json
└── README.md
```

## Features

- Plugin discovery and loading
- Custom toolbox extensions via plugins
- Plugin-provided commands
- Plugin configuration management

## Installation

```bash
npm install
npm run build
```

## Usage

### Load Plugins

```bash
# CLI automatically loads plugins from:
# - ./plugins/
# - ./node_modules/mycli-*
```

### Use Plugin Commands

```bash
# Commands added by plugins
./bin/cli validate
./bin/cli custom-action
```

### Use Plugin Extensions

```typescript
// In any command
const { myPlugin } = toolbox
myPlugin.doSomething()
```

## Creating a Plugin

### Basic Plugin Structure

```typescript
module.exports = (toolbox) => {
  const { print } = toolbox

  // Add to toolbox
  toolbox.myPlugin = {
    version: '1.0.0',
    doSomething: () => {
      print.info('Plugin action executed')
    }
  }
}
```

### Plugin with Commands

```typescript
module.exports = (toolbox) => {
  const { runtime } = toolbox

  runtime.addPlugin({
    name: 'my-plugin',
    commands: [
      {
        name: 'my-command',
        run: async (toolbox) => {
          // Command implementation
        }
      }
    ]
  })
}
```

## Plugin Discovery

The CLI looks for plugins in:

1. **Local plugins directory**: `./plugins/*.js`
2. **Node modules**: `./node_modules/mycli-*`
3. **Scoped packages**: `@scope/mycli-*`

## Plugin Naming Convention

- Local plugins: Any `.js` or `.ts` file in `plugins/`
- NPM plugins: Must match pattern `mycli-*`
- Example: `mycli-validator`, `@myorg/mycli-helper`

## Key Patterns

### 1. Load Plugins from Directory

```typescript
cli.plugins('./plugins', { matching: '*.js' })
```

### 2. Load NPM Plugins

```typescript
cli.plugins('./node_modules', {
  matching: 'mycli-*',
  hidden: true
})
```

### 3. Add Toolbox Extension

```typescript
toolbox.validator = {
  validate: (data) => { /* ... */ }
}
```

### 4. Register Commands

```typescript
runtime.addPlugin({
  name: 'my-plugin',
  commands: [/* commands */]
})
```

## Example Plugins

### custom-plugin.ts

Adds custom utilities to toolbox.

```typescript
toolbox.custom = {
  formatDate: (date) => { /* ... */ },
  parseConfig: (file) => { /* ... */ }
}
```

### validator-plugin.ts

Adds validation command and utilities.

```typescript
toolbox.validator = {
  validateFile: (path) => { /* ... */ },
  validateSchema: (data) => { /* ... */ }
}
```

## Publishing Plugins

### 1. Create NPM Package

```json
{
  "name": "mycli-myplugin",
  "main": "dist/index.js",
  "keywords": ["mycli", "plugin"]
}
```

### 2. Export Plugin

```typescript
module.exports = (toolbox) => {
  // Plugin implementation
}
```

### 3. Publish

```bash
npm publish
```

### 4. Install and Use

```bash
npm install mycli-myplugin
# Automatically loaded by CLI
```

## Advanced Patterns

### Conditional Plugin Loading

```typescript
if (config.enablePlugin) {
  cli.plugins('./plugins/optional')
}
```

### Plugin Configuration

```typescript
toolbox.myPlugin = {
  config: await filesystem.read('.mypluginrc', 'json'),
  // Plugin methods
}
```

### Plugin Dependencies

```typescript
module.exports = (toolbox) => {
  // Check for required plugins
  if (!toolbox.otherPlugin) {
    throw new Error('Requires other-plugin')
  }
}
```

## Best Practices

1. **Namespace Extensions**: Use unique names for toolbox extensions
2. **Document APIs**: Provide clear documentation for plugin methods
3. **Handle Errors**: Validate inputs and handle failures gracefully
4. **Version Plugins**: Use semantic versioning
5. **Test Plugins**: Write tests for plugin functionality

## Testing Plugins

```typescript
import { build } from 'gluegun'

test('plugin loads correctly', async () => {
  const cli = build().src(__dirname).plugins('./plugins').create()
  const toolbox = await cli.run()

  expect(toolbox.myPlugin).toBeDefined()
})
```
