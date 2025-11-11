# Basic Gluegun CLI Example

A simple example demonstrating core Gluegun CLI patterns.

## Structure

```
basic-cli/
├── src/
│   ├── cli.ts              # CLI entry point
│   ├── commands/
│   │   ├── hello.ts        # Simple command
│   │   └── generate.ts     # Template generator
│   └── extensions/
│       └── helpers.ts      # Custom toolbox extension
├── templates/
│   └── component.ts.ejs    # Example template
├── package.json
└── tsconfig.json
```

## Features

- Basic command structure
- Template generation
- Custom toolbox extensions
- TypeScript support

## Installation

```bash
npm install
npm run build
```

## Usage

```bash
# Run hello command
./bin/cli hello World

# Generate from template
./bin/cli generate MyComponent

# Show help
./bin/cli --help
```

## Commands

### hello

Simple greeting command demonstrating parameters.

```bash
./bin/cli hello [name]
```

### generate

Generate files from templates.

```bash
./bin/cli generate <name>
```

## Key Patterns

### 1. Command Structure

```typescript
const command: GluegunCommand = {
  name: 'hello',
  run: async (toolbox) => {
    const { print, parameters } = toolbox
    const name = parameters.first || 'World'
    print.success(`Hello, ${name}!`)
  }
}
```

### 2. Template Generation

```typescript
await template.generate({
  template: 'component.ts.ejs',
  target: `src/components/${name}.ts`,
  props: { name }
})
```

### 3. Custom Extensions

```typescript
toolbox.helpers = {
  formatName: (name: string) => {
    return name.charAt(0).toUpperCase() + name.slice(1)
  }
}
```

## Learning Path

1. Start with `src/cli.ts` - CLI initialization
2. Review `src/commands/hello.ts` - Simple command
3. Study `src/commands/generate.ts` - Template usage
4. Explore `templates/component.ts.ejs` - EJS templates
5. Check `src/extensions/helpers.ts` - Custom toolbox

## Next Steps

- Add more commands
- Create complex templates
- Implement plugin system
- Add interactive prompts
