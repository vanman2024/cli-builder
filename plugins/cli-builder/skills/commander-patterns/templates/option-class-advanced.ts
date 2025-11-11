import { Command, Option } from 'commander';
import chalk from 'chalk';

const program = new Command();

program
  .name('mycli')
  .description('Advanced Option class usage')
  .version('1.0.0');

program
  .command('deploy')
  .description('Deploy with advanced option patterns')

  // Option with choices
  .addOption(
    new Option('-e, --env <environment>', 'deployment environment')
      .choices(['dev', 'staging', 'prod'])
      .default('dev')
  )

  // Option with custom parser and validation
  .addOption(
    new Option('-p, --port <port>', 'server port')
      .argParser((value) => {
        const port = parseInt(value, 10);
        if (isNaN(port) || port < 1 || port > 65535) {
          throw new Error('Port must be between 1 and 65535');
        }
        return port;
      })
      .default(3000)
  )

  // Mandatory option
  .addOption(
    new Option('-t, --token <token>', 'API authentication token')
      .makeOptionMandatory()
      .env('API_TOKEN')
  )

  // Option from environment variable
  .addOption(
    new Option('-u, --api-url <url>', 'API base URL')
      .env('API_URL')
      .default('https://api.example.com')
  )

  // Conflicting options
  .addOption(
    new Option('--use-cache', 'enable caching')
      .conflicts('noCache')
  )
  .addOption(
    new Option('--no-cache', 'disable caching')
      .conflicts('useCache')
  )

  // Implies relationship
  .addOption(
    new Option('--ssl', 'enable SSL')
      .implies({ sslVerify: true })
  )
  .addOption(
    new Option('--ssl-verify', 'verify SSL certificates')
  )

  // Preset configurations
  .addOption(
    new Option('--preset <preset>', 'use preset configuration')
      .choices(['minimal', 'standard', 'complete'])
      .argParser((value) => {
        const presets = {
          minimal: { replicas: 1, timeout: 30 },
          standard: { replicas: 3, timeout: 60 },
          complete: { replicas: 5, timeout: 120 },
        };
        return presets[value as keyof typeof presets];
      })
  )

  // Hidden option (for debugging)
  .addOption(
    new Option('--debug', 'enable debug mode')
      .hideHelp()
  )

  // Custom option processing
  .addOption(
    new Option('-r, --replicas <count>', 'number of replicas')
      .argParser((value, previous) => {
        const count = parseInt(value, 10);
        if (count < 1) {
          throw new Error('Replicas must be at least 1');
        }
        return count;
      })
      .default(3)
  )

  .action((options) => {
    console.log(chalk.blue('Deployment configuration:'));
    console.log('Environment:', chalk.yellow(options.env));
    console.log('Port:', options.port);
    console.log('Token:', options.token ? chalk.green('***set***') : chalk.red('not set'));
    console.log('API URL:', options.apiUrl);
    console.log('Cache:', options.useCache ? 'enabled' : 'disabled');
    console.log('SSL:', options.ssl ? 'enabled' : 'disabled');
    console.log('SSL Verify:', options.sslVerify ? 'enabled' : 'disabled');

    if (options.preset) {
      console.log('Preset configuration:', options.preset);
    }

    console.log('Replicas:', options.replicas);

    if (options.debug) {
      console.log(chalk.gray('\nDebug mode enabled'));
      console.log(chalk.gray('All options:'), options);
    }

    console.log(chalk.green('\n✓ Deployment configuration validated'));
  });

// Command demonstrating option dependencies
program
  .command('backup')
  .description('Backup data with option dependencies')
  .addOption(
    new Option('-m, --method <method>', 'backup method')
      .choices(['full', 'incremental', 'differential'])
      .makeOptionMandatory()
  )
  .addOption(
    new Option('--base-backup <path>', 'base backup for incremental')
      .conflicts('full')
  )
  .addOption(
    new Option('--compression <level>', 'compression level')
      .choices(['none', 'low', 'medium', 'high'])
      .default('medium')
  )
  .action((options) => {
    if (options.method === 'incremental' && !options.baseBackup) {
      console.log(chalk.red('Error: --base-backup required for incremental backup'));
      process.exit(1);
    }

    console.log(chalk.blue(`Running ${options.method} backup...`));
    console.log('Compression:', options.compression);
    if (options.baseBackup) {
      console.log('Base backup:', options.baseBackup);
    }
    console.log(chalk.green('✓ Backup complete'));
  });

// Command with complex validation
program
  .command('scale')
  .description('Scale application with complex validation')
  .addOption(
    new Option('-r, --replicas <count>', 'number of replicas')
      .argParser((value) => {
        const count = parseInt(value, 10);
        if (isNaN(count)) {
          throw new Error('Replicas must be a number');
        }
        if (count < 1 || count > 100) {
          throw new Error('Replicas must be between 1 and 100');
        }
        return count;
      })
      .makeOptionMandatory()
  )
  .addOption(
    new Option('--cpu <value>', 'CPU limit (millicores)')
      .argParser((value) => {
        const cpu = parseInt(value, 10);
        if (cpu < 100 || cpu > 8000) {
          throw new Error('CPU must be between 100 and 8000 millicores');
        }
        return cpu;
      })
      .default(1000)
  )
  .addOption(
    new Option('--memory <value>', 'Memory limit (MB)')
      .argParser((value) => {
        const mem = parseInt(value, 10);
        if (mem < 128 || mem > 16384) {
          throw new Error('Memory must be between 128 and 16384 MB');
        }
        return mem;
      })
      .default(512)
  )
  .action((options) => {
    console.log(chalk.blue('Scaling application:'));
    console.log('Replicas:', chalk.yellow(options.replicas));
    console.log('CPU:', `${options.cpu}m`);
    console.log('Memory:', `${options.memory}MB`);

    const totalCpu = options.replicas * options.cpu;
    const totalMemory = options.replicas * options.memory;

    console.log(chalk.gray('\nTotal resources:'));
    console.log(chalk.gray(`CPU: ${totalCpu}m`));
    console.log(chalk.gray(`Memory: ${totalMemory}MB`));

    console.log(chalk.green('\n✓ Scaling complete'));
  });

program.parse();
