# Basic Commander.js Usage

Simple examples demonstrating core Commander.js features.

## Example 1: Simple CLI with Commands

```typescript
import { Command } from 'commander';

const program = new Command();

program
  .name('mycli')
  .description('My CLI tool')
  .version('1.0.0');

// Command without options
program
  .command('init')
  .description('Initialize project')
  .action(() => {
    console.log('Initializing project...');
  });

// Command with options
program
  .command('build')
  .description('Build project')
  .option('-w, --watch', 'watch mode')
  .action((options) => {
    console.log('Building...');
    if (options.watch) {
      console.log('Watch mode enabled');
    }
  });

program.parse();
```

**Usage:**
```bash
mycli init
mycli build
mycli build --watch
mycli --help
mycli --version
```

## Example 2: Command with Arguments

```typescript
import { Command } from 'commander';

const program = new Command();

program
  .name('mycli')
  .version('1.0.0');

program
  .command('greet <name>')
  .description('Greet someone')
  .action((name) => {
    console.log(`Hello, ${name}!`);
  });

program
  .command('add <a> <b>')
  .description('Add two numbers')
  .action((a, b) => {
    const sum = parseInt(a) + parseInt(b);
    console.log(`${a} + ${b} = ${sum}`);
  });

program.parse();
```

**Usage:**
```bash
mycli greet Alice
# Output: Hello, Alice!

mycli add 5 3
# Output: 5 + 3 = 8
```

## Example 3: Options with Different Types

```typescript
import { Command } from 'commander';

const program = new Command();

program
  .name('mycli')
  .version('1.0.0');

program
  .command('serve')
  .description('Start development server')
  // Boolean flag
  .option('-o, --open', 'open browser', false)
  // Option with value
  .option('-p, --port <port>', 'port number', '3000')
  // Option with default
  .option('-h, --host <host>', 'hostname', 'localhost')
  // Negatable option
  .option('--no-color', 'disable colors')
  .action((options) => {
    console.log(`Server running at http://${options.host}:${options.port}`);
    console.log('Open browser:', options.open);
    console.log('Colors:', options.color);
  });

program.parse();
```

**Usage:**
```bash
mycli serve
# Uses defaults

mycli serve --port 8080
# Uses custom port

mycli serve --open --no-color
# Opens browser and disables colors
```

## Example 4: Global Options

```typescript
import { Command } from 'commander';

const program = new Command();

program
  .name('mycli')
  .version('1.0.0')
  // Global options
  .option('-v, --verbose', 'verbose output')
  .option('-c, --config <path>', 'config file path');

program
  .command('deploy')
  .action((options, command) => {
    const globalOpts = command.parent?.opts();
    console.log('Deploying...');
    if (globalOpts?.verbose) {
      console.log('Verbose mode enabled');
      console.log('Config:', globalOpts.config);
    }
  });

program.parse();
```

**Usage:**
```bash
mycli deploy
# Normal output

mycli --verbose deploy
# Verbose output

mycli --verbose --config ./config.json deploy
# Verbose with custom config
```

## Example 5: Multiple Commands

```typescript
import { Command } from 'commander';
import chalk from 'chalk';

const program = new Command();

program.name('mycli').version('1.0.0');

program
  .command('init')
  .description('Initialize new project')
  .action(() => {
    console.log(chalk.green('✓ Project initialized'));
  });

program
  .command('build')
  .description('Build project')
  .action(() => {
    console.log(chalk.blue('Building...'));
    console.log(chalk.green('✓ Build complete'));
  });

program
  .command('test')
  .description('Run tests')
  .action(() => {
    console.log(chalk.blue('Running tests...'));
    console.log(chalk.green('✓ All tests passed'));
  });

program
  .command('deploy')
  .description('Deploy to production')
  .action(() => {
    console.log(chalk.yellow('Deploying...'));
    console.log(chalk.green('✓ Deployed'));
  });

program.parse();
```

**Usage:**
```bash
mycli init
mycli build
mycli test
mycli deploy
mycli --help  # Shows all commands
```

## Running the Examples

### Setup

1. Create a new project:
```bash
mkdir my-cli
cd my-cli
npm init -y
```

2. Install dependencies:
```bash
npm install commander chalk
npm install -D typescript @types/node tsx
```

3. Configure TypeScript:
```bash
npx tsc --init --target ES2022 --module ESNext
```

4. Create `src/index.ts` with any example above

5. Run with tsx:
```bash
npx tsx src/index.ts --help
```

### Building for Production

```bash
# Build TypeScript
npx tsc

# Run compiled version
node dist/index.js
```

### Making it Executable

Add to `package.json`:
```json
{
  "bin": {
    "mycli": "./dist/index.js"
  }
}
```

Add shebang to top of source file:
```typescript
#!/usr/bin/env node
import { Command } from 'commander';
// ... rest of code
```

Install globally for testing:
```bash
npm link
mycli --help
```
