# Commander.js Options and Arguments Demo

Comprehensive examples of option and argument patterns.

## Option Patterns

### 1. Boolean Flags

```typescript
program
  .command('build')
  .option('-w, --watch', 'watch for changes')
  .option('-m, --minify', 'minify output')
  .option('-v, --verbose', 'verbose logging')
  .action((options) => {
    console.log('Watch:', options.watch); // true or undefined
    console.log('Minify:', options.minify);
    console.log('Verbose:', options.verbose);
  });
```

Usage:
```bash
mycli build --watch --minify
```

### 2. Options with Required Values

```typescript
program
  .command('deploy')
  .option('-e, --env <environment>', 'deployment environment')
  .option('-r, --region <region>', 'AWS region')
  .action((options) => {
    console.log('Environment:', options.env);
    console.log('Region:', options.region);
  });
```

Usage:
```bash
mycli deploy --env production --region us-west-2
```

### 3. Options with Optional Values

```typescript
program
  .command('log')
  .option('-f, --file [path]', 'log file path')
  .action((options) => {
    if (options.file === true) {
      console.log('Using default log file');
    } else if (options.file) {
      console.log('Log file:', options.file);
    }
  });
```

Usage:
```bash
mycli log --file              # file = true
mycli log --file custom.log   # file = 'custom.log'
mycli log                     # file = undefined
```

### 4. Options with Defaults

```typescript
program
  .command('serve')
  .option('-p, --port <port>', 'port number', '3000')
  .option('-h, --host <host>', 'hostname', 'localhost')
  .action((options) => {
    console.log(`http://${options.host}:${options.port}`);
  });
```

Usage:
```bash
mycli serve                    # Uses defaults
mycli serve --port 8080       # Custom port
```

### 5. Negatable Options

```typescript
program
  .command('build')
  .option('--cache', 'enable cache')
  .option('--no-cache', 'disable cache')
  .option('--color', 'enable colors')
  .option('--no-color', 'disable colors')
  .action((options) => {
    console.log('Cache:', options.cache);    // undefined, true, or false
    console.log('Color:', options.color);
  });
```

Usage:
```bash
mycli build                # cache & color = undefined
mycli build --cache        # cache = true
mycli build --no-cache     # cache = false
mycli build --no-color     # color = false
```

### 6. Variadic Options

```typescript
program
  .command('tag')
  .option('-t, --tags <tags...>', 'multiple tags')
  .action((options) => {
    console.log('Tags:', options.tags);  // Array
  });
```

Usage:
```bash
mycli tag --tags v1.0 production stable
# Tags: ['v1.0', 'production', 'stable']
```

### 7. Options with Custom Parsers

```typescript
program
  .command('scale')
  .option('-r, --replicas <count>', 'replica count', parseInt)
  .option('-m, --memory <mb>', 'memory in MB', parseFloat)
  .option('-t, --timeout <sec>', 'timeout', (value) => {
    return parseInt(value) * 1000; // Convert to ms
  })
  .action((options) => {
    console.log('Replicas:', options.replicas);  // Number
    console.log('Memory:', options.memory);      // Number
    console.log('Timeout:', options.timeout);    // Number (ms)
  });
```

Usage:
```bash
mycli scale --replicas 5 --memory 512.5 --timeout 30
```

## Argument Patterns

### 1. Required Arguments

```typescript
program
  .command('deploy <environment>')
  .description('Deploy to environment')
  .action((environment) => {
    console.log('Deploying to:', environment);
  });
```

Usage:
```bash
mycli deploy production   # ✓ Works
mycli deploy             # ✗ Error: missing required argument
```

### 2. Optional Arguments

```typescript
program
  .command('create <name> [description]')
  .description('Create item')
  .action((name, description) => {
    console.log('Name:', name);
    console.log('Description:', description || 'No description');
  });
```

Usage:
```bash
mycli create "My Item"
mycli create "My Item" "A detailed description"
```

### 3. Variadic Arguments

```typescript
program
  .command('add <items...>')
  .description('Add multiple items')
  .action((items) => {
    console.log('Items:', items);  // Array
    items.forEach((item, i) => {
      console.log(`  ${i + 1}. ${item}`);
    });
  });
```

Usage:
```bash
mycli add item1 item2 item3
# Items: ['item1', 'item2', 'item3']
```

### 4. Mixed Required and Optional

```typescript
program
  .command('copy <source> <destination> [options]')
  .description('Copy files')
  .action((source, destination, options) => {
    console.log('Source:', source);
    console.log('Destination:', destination);
    console.log('Options:', options || 'none');
  });
```

### 5. Arguments with Descriptions

```typescript
program
  .command('deploy <environment>')
  .argument('<environment>', 'target environment (dev, staging, prod)')
  .argument('[region]', 'deployment region', 'us-east-1')
  .action((environment, region) => {
    console.log(`Deploying to ${environment} in ${region}`);
  });
```

### 6. Arguments with Custom Parsers

```typescript
program
  .command('wait <seconds>')
  .argument('<seconds>', 'seconds to wait', parseFloat)
  .action(async (seconds) => {
    console.log(`Waiting ${seconds} seconds...`);
    await new Promise((resolve) => setTimeout(resolve, seconds * 1000));
    console.log('Done!');
  });
```

Usage:
```bash
mycli wait 2.5    # Waits 2.5 seconds
```

### 7. Arguments with Validation

```typescript
program
  .command('set-port <port>')
  .argument('<port>', 'port number', (value) => {
    const port = parseInt(value, 10);
    if (isNaN(port)) {
      throw new Error('Port must be a number');
    }
    if (port < 1 || port > 65535) {
      throw new Error('Port must be between 1 and 65535');
    }
    return port;
  })
  .action((port) => {
    console.log('Port set to:', port);
  });
```

## Combined Patterns

### Arguments + Options

```typescript
program
  .command('deploy <environment>')
  .argument('<environment>', 'deployment environment')
  .option('-f, --force', 'force deployment')
  .option('-d, --dry-run', 'simulate deployment')
  .option('-t, --tag <tag>', 'deployment tag', 'latest')
  .action((environment, options) => {
    console.log('Environment:', environment);
    console.log('Force:', options.force);
    console.log('Dry run:', options.dryRun);
    console.log('Tag:', options.tag);
  });
```

Usage:
```bash
mycli deploy production --force --tag v1.2.3
```

### Variadic Arguments + Options

```typescript
program
  .command('compile <files...>')
  .argument('<files...>', 'files to compile')
  .option('-o, --output <dir>', 'output directory', './dist')
  .option('-m, --minify', 'minify output')
  .action((files, options) => {
    console.log('Files:', files);
    console.log('Output:', options.output);
    console.log('Minify:', options.minify);
  });
```

Usage:
```bash
mycli compile src/a.ts src/b.ts --output build --minify
```

### Multiple Option Types

```typescript
program
  .command('start')
  .option('-p, --port <port>', 'port', '3000')
  .option('-h, --host <host>', 'host', 'localhost')
  .option('-o, --open', 'open browser')
  .option('--no-color', 'disable colors')
  .option('-e, --env <vars...>', 'environment variables')
  .action((options) => {
    console.log('Server:', `http://${options.host}:${options.port}`);
    console.log('Open:', options.open);
    console.log('Color:', options.color);
    console.log('Env:', options.env);
  });
```

Usage:
```bash
mycli start --port 8080 --open --env NODE_ENV=production DEBUG=true
```

## Complete Example

```typescript
#!/usr/bin/env node
import { Command } from 'commander';
import chalk from 'chalk';

const program = new Command();

program.name('deploy-cli').version('1.0.0');

program
  .command('deploy <environment> [region]')
  .description('Deploy application')
  .argument('<environment>', 'target environment (dev, staging, prod)')
  .argument('[region]', 'deployment region', 'us-east-1')
  .option('-f, --force', 'skip confirmations', false)
  .option('-d, --dry-run', 'simulate deployment', false)
  .option('-t, --tag <tag>', 'deployment tag', 'latest')
  .option('-r, --replicas <count>', 'replica count', parseInt, 3)
  .option('--env <vars...>', 'environment variables')
  .option('--no-rollback', 'disable auto-rollback')
  .action((environment, region, options) => {
    console.log(chalk.blue('Deployment Configuration:'));
    console.log('Environment:', chalk.yellow(environment));
    console.log('Region:', region);
    console.log('Tag:', options.tag);
    console.log('Replicas:', options.replicas);
    console.log('Force:', options.force);
    console.log('Dry run:', options.dryRun);
    console.log('Rollback:', options.rollback);

    if (options.env) {
      console.log('Environment variables:');
      options.env.forEach((v) => console.log(`  ${v}`));
    }

    if (options.dryRun) {
      console.log(chalk.yellow('\n🔍 Dry run - no actual deployment'));
      return;
    }

    console.log(chalk.green('\n✓ Deployment complete!'));
  });

program.parse();
```

Usage examples:
```bash
# Basic
deploy-cli deploy production

# With region
deploy-cli deploy staging us-west-2

# With options
deploy-cli deploy prod --force --replicas 5

# With environment variables
deploy-cli deploy prod --env NODE_ENV=production API_KEY=xyz

# Dry run
deploy-cli deploy prod --dry-run --no-rollback

# All together
deploy-cli deploy production us-west-2 \
  --force \
  --tag v2.0.0 \
  --replicas 10 \
  --env NODE_ENV=production DEBUG=false \
  --no-rollback
```
