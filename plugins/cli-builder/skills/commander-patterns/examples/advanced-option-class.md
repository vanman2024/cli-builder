# Advanced Option Class Usage

Comprehensive examples of the Option class for advanced option handling.

## Basic Option Class

```typescript
import { Command, Option } from 'commander';

const program = new Command();

program
  .command('deploy')
  .addOption(
    new Option('-e, --env <environment>', 'target environment')
      .choices(['dev', 'staging', 'prod'])
      .default('dev')
  )
  .action((options) => {
    console.log('Environment:', options.env);
  });

program.parse();
```

## Option with Choices

```typescript
import { Command, Option } from 'commander';

program
  .command('log')
  .addOption(
    new Option('-l, --level <level>', 'log level')
      .choices(['debug', 'info', 'warn', 'error'])
      .default('info')
  )
  .addOption(
    new Option('-f, --format <format>', 'output format')
      .choices(['json', 'yaml', 'table'])
      .default('table')
  )
  .action((options) => {
    console.log(`Logging at ${options.level} level in ${options.format} format`);
  });
```

Usage:
```bash
mycli log --level debug --format json
mycli log --level invalid    # Error: invalid choice
```

## Mandatory Options

```typescript
import { Command, Option } from 'commander';

program
  .command('deploy')
  .addOption(
    new Option('-t, --token <token>', 'API token')
      .makeOptionMandatory()
  )
  .addOption(
    new Option('-e, --env <environment>', 'environment')
      .choices(['dev', 'staging', 'prod'])
      .makeOptionMandatory()
  )
  .action((options) => {
    console.log('Deploying with token:', options.token);
    console.log('Environment:', options.env);
  });
```

Usage:
```bash
mycli deploy    # Error: required option missing
mycli deploy --token abc --env prod    # ✓ Works
```

## Options from Environment Variables

```typescript
import { Command, Option } from 'commander';

program
  .command('deploy')
  .addOption(
    new Option('-t, --token <token>', 'API token')
      .env('API_TOKEN')
      .makeOptionMandatory()
  )
  .addOption(
    new Option('-u, --api-url <url>', 'API URL')
      .env('API_URL')
      .default('https://api.example.com')
  )
  .action((options) => {
    console.log('Token:', options.token);
    console.log('API URL:', options.apiUrl);
  });
```

Usage:
```bash
export API_TOKEN=abc123
export API_URL=https://custom-api.com

mycli deploy    # Uses environment variables
mycli deploy --token xyz    # CLI arg overrides env var
```

## Custom Argument Parsers

```typescript
import { Command, Option } from 'commander';

program
  .command('scale')
  .addOption(
    new Option('-r, --replicas <count>', 'number of replicas')
      .argParser((value) => {
        const count = parseInt(value, 10);
        if (isNaN(count) || count < 1 || count > 100) {
          throw new Error('Replicas must be between 1 and 100');
        }
        return count;
      })
      .default(3)
  )
  .addOption(
    new Option('-m, --memory <size>', 'memory limit')
      .argParser((value) => {
        // Parse sizes like "512M", "2G"
        const match = value.match(/^(\d+)([MG])$/i);
        if (!match) {
          throw new Error('Invalid memory format (use 512M or 2G)');
        }
        const [, num, unit] = match;
        const mb = parseInt(num) * (unit.toUpperCase() === 'G' ? 1024 : 1);
        return mb;
      })
      .default(512)
  )
  .action((options) => {
    console.log('Replicas:', options.replicas);
    console.log('Memory:', options.memory, 'MB');
  });
```

Usage:
```bash
mycli scale --replicas 5 --memory 2G
# Replicas: 5
# Memory: 2048 MB
```

## Conflicting Options

```typescript
import { Command, Option } from 'commander';

program
  .command('build')
  .addOption(
    new Option('--cache', 'enable caching')
      .conflicts('noCache')
  )
  .addOption(
    new Option('--no-cache', 'disable caching')
      .conflicts('cache')
  )
  .addOption(
    new Option('--watch', 'watch mode')
      .conflicts('production')
  )
  .addOption(
    new Option('--production', 'production build')
      .conflicts('watch')
  )
  .action((options) => {
    console.log('Cache:', options.cache);
    console.log('Watch:', options.watch);
    console.log('Production:', options.production);
  });
```

Usage:
```bash
mycli build --cache    # ✓ Works
mycli build --no-cache    # ✓ Works
mycli build --cache --no-cache    # ✗ Error: conflicting options
mycli build --watch --production    # ✗ Error: conflicting options
```

## Option Implies

```typescript
import { Command, Option } from 'commander';

program
  .command('server')
  .addOption(
    new Option('--ssl', 'enable SSL')
      .implies({ sslCert: './cert.pem', sslKey: './key.pem' })
  )
  .addOption(
    new Option('--ssl-cert <path>', 'SSL certificate path')
  )
  .addOption(
    new Option('--ssl-key <path>', 'SSL key path')
  )
  .addOption(
    new Option('--secure', 'secure mode')
      .implies({ ssl: true, httpsOnly: true })
  )
  .addOption(
    new Option('--https-only', 'enforce HTTPS')
  )
  .action((options) => {
    console.log('SSL:', options.ssl);
    console.log('SSL Cert:', options.sslCert);
    console.log('SSL Key:', options.sslKey);
    console.log('HTTPS Only:', options.httpsOnly);
  });
```

Usage:
```bash
mycli server --ssl
# SSL: true
# SSL Cert: ./cert.pem
# SSL Key: ./key.pem

mycli server --secure
# SSL: true
# HTTPS Only: true
```

## Preset Configurations

```typescript
import { Command, Option } from 'commander';

program
  .command('deploy')
  .addOption(
    new Option('--preset <preset>', 'use preset configuration')
      .choices(['minimal', 'standard', 'enterprise'])
      .argParser((value) => {
        const presets = {
          minimal: {
            replicas: 1,
            memory: '256M',
            cpu: '0.25',
            autoScaling: false,
          },
          standard: {
            replicas: 3,
            memory: '512M',
            cpu: '0.5',
            autoScaling: true,
          },
          enterprise: {
            replicas: 10,
            memory: '2G',
            cpu: '2',
            autoScaling: true,
            loadBalancer: true,
            monitoring: true,
          },
        };
        return presets[value as keyof typeof presets];
      })
  )
  .action((options) => {
    if (options.preset) {
      console.log('Using preset configuration:');
      console.log(JSON.stringify(options.preset, null, 2));
    }
  });
```

Usage:
```bash
mycli deploy --preset enterprise
# Using preset configuration:
# {
#   "replicas": 10,
#   "memory": "2G",
#   "cpu": "2",
#   "autoScaling": true,
#   "loadBalancer": true,
#   "monitoring": true
# }
```

## Hidden Options (Debug/Internal)

```typescript
import { Command, Option } from 'commander';

program
  .command('build')
  .option('-p, --production', 'production build')
  .addOption(
    new Option('--debug', 'enable debug mode')
      .hideHelp()
  )
  .addOption(
    new Option('--internal-api', 'use internal API')
      .hideHelp()
      .default(false)
  )
  .action((options) => {
    if (options.debug) {
      console.log('Debug mode enabled');
      console.log('All options:', options);
    }
  });
```

## Complex Validation

```typescript
import { Command, Option } from 'commander';

program
  .command('backup')
  .addOption(
    new Option('-s, --schedule <cron>', 'backup schedule (cron format)')
      .argParser((value) => {
        // Validate cron expression
        const cronRegex = /^(\*|([0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])|\*\/([0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])) (\*|([0-9]|1[0-9]|2[0-3])|\*\/([0-9]|1[0-9]|2[0-3])) (\*|([1-9]|1[0-9]|2[0-9]|3[0-1])|\*\/([1-9]|1[0-9]|2[0-9]|3[0-1])) (\*|([1-9]|1[0-2])|\*\/([1-9]|1[0-2])) (\*|([0-6])|\*\/([0-6]))$/;

        if (!cronRegex.test(value)) {
          throw new Error('Invalid cron expression');
        }
        return value;
      })
  )
  .addOption(
    new Option('-r, --retention <days>', 'backup retention in days')
      .argParser((value) => {
        const days = parseInt(value, 10);
        if (isNaN(days) || days < 1 || days > 365) {
          throw new Error('Retention must be between 1 and 365 days');
        }
        return days;
      })
      .default(30)
  )
  .action((options) => {
    console.log('Schedule:', options.schedule);
    console.log('Retention:', options.retention, 'days');
  });
```

Usage:
```bash
mycli backup --schedule "0 2 * * *" --retention 90
# Schedule: 0 2 * * *
# Retention: 90 days
```

## Cumulative Options

```typescript
import { Command, Option } from 'commander';

program
  .command('log')
  .addOption(
    new Option('-v, --verbose', 'increase verbosity')
      .argParser((value, previous) => {
        return previous + 1;
      })
      .default(0)
  )
  .action((options) => {
    console.log('Verbosity level:', options.verbose);
    // 0 = normal
    // 1 = verbose (-v)
    // 2 = very verbose (-vv)
    // 3 = debug (-vvv)
  });
```

Usage:
```bash
mycli log         # verbosity: 0
mycli log -v      # verbosity: 1
mycli log -vv     # verbosity: 2
mycli log -vvv    # verbosity: 3
```

## Complete Example

```typescript
#!/usr/bin/env node
import { Command, Option } from 'commander';
import chalk from 'chalk';

const program = new Command();

program
  .name('deploy-cli')
  .version('1.0.0');

program
  .command('deploy')
  .description('Deploy application with advanced options')

  // Required with choices
  .addOption(
    new Option('-e, --env <environment>', 'deployment environment')
      .choices(['dev', 'staging', 'prod'])
      .makeOptionMandatory()
  )

  // Environment variable with validation
  .addOption(
    new Option('-t, --token <token>', 'API token')
      .env('DEPLOY_TOKEN')
      .makeOptionMandatory()
      .argParser((value) => {
        if (value.length < 32) {
          throw new Error('Token must be at least 32 characters');
        }
        return value;
      })
  )

  // Custom parser with unit conversion
  .addOption(
    new Option('-m, --memory <size>', 'memory allocation')
      .argParser((value) => {
        const match = value.match(/^(\d+)([MG])$/i);
        if (!match) {
          throw new Error('Memory must be in format: 512M or 2G');
        }
        const [, num, unit] = match;
        return parseInt(num) * (unit.toUpperCase() === 'G' ? 1024 : 1);
      })
      .default(512)
  )

  // Conflicting options
  .addOption(
    new Option('--fast', 'fast deployment (skip tests)')
      .conflicts('safe')
  )
  .addOption(
    new Option('--safe', 'safe deployment (full tests)')
      .conflicts('fast')
      .default(true)
  )

  // Implies relationship
  .addOption(
    new Option('--production-mode', 'enable production optimizations')
      .implies({ env: 'prod', safe: true, monitoring: true })
  )
  .addOption(
    new Option('--monitoring', 'enable monitoring')
  )

  // Hidden debug option
  .addOption(
    new Option('--debug', 'debug mode')
      .hideHelp()
  )

  .action((options) => {
    console.log(chalk.blue('Deployment Configuration:'));
    console.log('Environment:', chalk.yellow(options.env));
    console.log('Token:', options.token ? chalk.green('***set***') : chalk.red('missing'));
    console.log('Memory:', `${options.memory}MB`);
    console.log('Mode:', options.fast ? 'fast' : 'safe');
    console.log('Production Mode:', options.productionMode || false);
    console.log('Monitoring:', options.monitoring || false);

    if (options.debug) {
      console.log(chalk.gray('\nDebug - All options:'));
      console.log(chalk.gray(JSON.stringify(options, null, 2)));
    }

    console.log(chalk.green('\n✓ Deployment started'));
  });

program.parse();
```

Usage:
```bash
export DEPLOY_TOKEN=abc123xyz789abc123xyz789abc12345

# Basic deployment
deploy-cli deploy --env staging

# Custom memory
deploy-cli deploy --env prod --memory 4G

# Fast mode
deploy-cli deploy --env dev --fast

# Production mode (implies multiple settings)
deploy-cli deploy --production-mode

# Debug
deploy-cli deploy --env dev --debug
```
