#!/usr/bin/env node
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

yargs(hideBin(process.argv))
  .command('deploy <service>', 'deploy a service', (yargs) => {
    yargs
      .positional('service', {
        describe: 'Service name to deploy',
        type: 'string'
      })
      .option('environment', {
        alias: 'env',
        describe: 'Deployment environment',
        choices: ['development', 'staging', 'production'],
        demandOption: true
      })
      .option('version', {
        alias: 'v',
        describe: 'Version to deploy',
        type: 'string',
        coerce: (arg) => {
          if (!/^\d+\.\d+\.\d+$/.test(arg)) {
            throw new Error('Version must be in format X.Y.Z');
          }
          return arg;
        }
      })
      .option('replicas', {
        alias: 'r',
        describe: 'Number of replicas',
        type: 'number',
        default: 1
      })
      .option('force', {
        alias: 'f',
        describe: 'Force deployment without confirmation',
        type: 'boolean',
        default: false
      })
      .check((argv) => {
        if (argv.replicas > 10 && argv.environment === 'development') {
          throw new Error('Cannot deploy more than 10 replicas in development');
        }
        if (argv.environment === 'production' && !argv.version) {
          throw new Error('Version is required for production deployments');
        }
        return true;
      });
  }, (argv) => {
    console.log(`Deploying ${argv.service} v${argv.version || 'latest'}`);
    console.log(`Environment: ${argv.environment}`);
    console.log(`Replicas: ${argv.replicas}`);

    if (!argv.force) {
      console.log('Use --force to proceed without confirmation');
    }
  })
  .command('rollback <service>', 'rollback a service', (yargs) => {
    yargs
      .positional('service', {
        describe: 'Service name to rollback',
        type: 'string'
      })
      .option('environment', {
        alias: 'env',
        describe: 'Deployment environment',
        choices: ['development', 'staging', 'production'],
        demandOption: true
      })
      .option('version', {
        alias: 'v',
        describe: 'Version to rollback to',
        type: 'string'
      });
  }, (argv) => {
    console.log(`Rolling back ${argv.service} in ${argv.environment}`);
    if (argv.version) {
      console.log(`Target version: ${argv.version}`);
    }
  })
  .middleware((argv) => {
    // Logging middleware
    if (argv.verbose) {
      console.log('[DEBUG] Arguments:', argv);
    }
  })
  .option('verbose', {
    describe: 'Enable verbose logging',
    type: 'boolean',
    global: true  // Available to all commands
  })
  .demandCommand(1, 'You need at least one command')
  .strict()
  .help()
  .alias('help', 'h')
  .version()
  .alias('version', 'V')
  .parse();
