import { Command, Option } from 'commander';
import chalk from 'chalk';

const program = new Command();

program
  .name('mycli')
  .description('CLI with various option types')
  .version('1.0.0');

program
  .command('deploy')
  .description('Deploy application')
  // Boolean flag
  .option('-v, --verbose', 'verbose output', false)
  // Option with required value
  .option('-p, --port <port>', 'port number', '3000')
  // Option with optional value
  .option('-c, --config [path]', 'config file path')
  // Negatable option
  .option('--no-build', 'skip build step')
  // Multiple choice option using Option class
  .addOption(
    new Option('-e, --env <environment>', 'target environment')
      .choices(['dev', 'staging', 'prod'])
      .default('dev')
  )
  // Option with custom parser
  .addOption(
    new Option('-r, --replicas <count>', 'number of replicas')
      .argParser(parseInt)
      .default(3)
  )
  // Mandatory option
  .addOption(
    new Option('-t, --token <token>', 'API token')
      .makeOptionMandatory()
      .env('API_TOKEN')
  )
  // Variadic option
  .option('--tags <tags...>', 'deployment tags')
  .action((options) => {
    console.log(chalk.blue('Deploying with options:'));
    console.log('Verbose:', options.verbose);
    console.log('Port:', options.port);
    console.log('Config:', options.config);
    console.log('Build:', options.build);
    console.log('Environment:', options.env);
    console.log('Replicas:', options.replicas);
    console.log('Token:', options.token ? '***' : 'not set');
    console.log('Tags:', options.tags);

    if (options.verbose) {
      console.log(chalk.gray('Verbose mode enabled'));
    }

    console.log(chalk.green('✓ Deployment complete'));
  });

program.parse();
