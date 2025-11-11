#!/usr/bin/env node
/**
 * Example: yargs with nested subcommands
 *
 * Usage:
 *   node subcommands-example.js user create --name John --email john@example.com
 *   node subcommands-example.js user list --limit 10
 *   node subcommands-example.js user delete 123
 */

const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

yargs(hideBin(process.argv))
  .command('user', 'manage users', (yargs) => {
    return yargs
      .command('create', 'create a new user', (yargs) => {
        yargs
          .option('name', {
            describe: 'User name',
            type: 'string',
            demandOption: true
          })
          .option('email', {
            describe: 'User email',
            type: 'string',
            demandOption: true
          })
          .option('role', {
            describe: 'User role',
            choices: ['admin', 'user', 'guest'],
            default: 'user'
          });
      }, (argv) => {
        console.log(`Creating user: ${argv.name} (${argv.email}) with role ${argv.role}`);
      })
      .command('list', 'list all users', (yargs) => {
        yargs
          .option('limit', {
            alias: 'l',
            describe: 'Limit number of results',
            type: 'number',
            default: 10
          })
          .option('offset', {
            alias: 'o',
            describe: 'Offset for pagination',
            type: 'number',
            default: 0
          });
      }, (argv) => {
        console.log(`Listing users (limit: ${argv.limit}, offset: ${argv.offset})`);
      })
      .command('delete <id>', 'delete a user', (yargs) => {
        yargs.positional('id', {
          describe: 'User ID',
          type: 'number'
        });
      }, (argv) => {
        console.log(`Deleting user ID: ${argv.id}`);
      })
      .demandCommand(1, 'You need to specify a user subcommand');
  })
  .command('project', 'manage projects', (yargs) => {
    return yargs
      .command('create <name>', 'create a new project', (yargs) => {
        yargs
          .positional('name', {
            describe: 'Project name',
            type: 'string'
          })
          .option('template', {
            alias: 't',
            describe: 'Project template',
            choices: ['basic', 'advanced'],
            default: 'basic'
          });
      }, (argv) => {
        console.log(`Creating project: ${argv.name} with template ${argv.template}`);
      })
      .command('list', 'list all projects', {}, (argv) => {
        console.log('Listing all projects');
      })
      .demandCommand(1, 'You need to specify a project subcommand');
  })
  .demandCommand(1, 'You need at least one command')
  .strict()
  .help()
  .parse();
