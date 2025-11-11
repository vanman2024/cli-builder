import { Command } from 'commander';
import inquirer from 'inquirer';
import chalk from 'chalk';

const program = new Command();

program
  .name('mycli')
  .description('Interactive CLI with Inquirer.js integration')
  .version('1.0.0');

// Interactive init command
program
  .command('init')
  .description('Initialize project interactively')
  .option('-y, --yes', 'skip prompts and use defaults', false)
  .action(async (options) => {
    if (options.yes) {
      console.log(chalk.blue('Using default configuration...'));
      await initProject({
        name: 'my-project',
        template: 'basic',
        features: [],
      });
      return;
    }

    // Interactive prompts
    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'name',
        message: 'Project name:',
        default: 'my-project',
        validate: (input) => {
          if (!input.trim()) {
            return 'Project name is required';
          }
          if (!/^[a-z0-9-]+$/.test(input)) {
            return 'Project name must contain only lowercase letters, numbers, and hyphens';
          }
          return true;
        },
      },
      {
        type: 'list',
        name: 'template',
        message: 'Choose a template:',
        choices: ['basic', 'advanced', 'enterprise'],
        default: 'basic',
      },
      {
        type: 'checkbox',
        name: 'features',
        message: 'Select features:',
        choices: [
          { name: 'TypeScript', value: 'typescript', checked: true },
          { name: 'ESLint', value: 'eslint', checked: true },
          { name: 'Prettier', value: 'prettier', checked: true },
          { name: 'Testing (Jest)', value: 'jest' },
          { name: 'CI/CD', value: 'cicd' },
          { name: 'Docker', value: 'docker' },
        ],
      },
      {
        type: 'confirm',
        name: 'install',
        message: 'Install dependencies now?',
        default: true,
      },
    ]);

    await initProject(answers);
  });

// Interactive deploy command
program
  .command('deploy')
  .description('Deploy with interactive configuration')
  .option('-e, --env <environment>', 'skip environment prompt')
  .action(async (options) => {
    const questions: any[] = [];

    // Conditionally add environment question
    if (!options.env) {
      questions.push({
        type: 'list',
        name: 'environment',
        message: 'Select deployment environment:',
        choices: ['dev', 'staging', 'prod'],
      });
    }

    questions.push(
      {
        type: 'list',
        name: 'strategy',
        message: 'Deployment strategy:',
        choices: ['rolling', 'blue-green', 'canary'],
        default: 'rolling',
      },
      {
        type: 'confirm',
        name: 'runTests',
        message: 'Run tests before deployment?',
        default: true,
      },
      {
        type: 'confirm',
        name: 'createBackup',
        message: 'Create backup before deployment?',
        default: true,
        when: (answers) => answers.environment === 'prod',
      },
      {
        type: 'password',
        name: 'token',
        message: 'Enter deployment token:',
        mask: '*',
        validate: (input) => (input.length > 0 ? true : 'Token is required'),
      }
    );

    const answers = await inquirer.prompt(questions);

    const deployConfig = {
      environment: options.env || answers.environment,
      ...answers,
    };

    console.log(chalk.blue('\nDeployment configuration:'));
    console.log(JSON.stringify(deployConfig, null, 2));

    const { confirm } = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'confirm',
        message: 'Proceed with deployment?',
        default: false,
      },
    ]);

    if (!confirm) {
      console.log(chalk.yellow('Deployment cancelled'));
      return;
    }

    await deploy(deployConfig);
  });

// Interactive config command
program
  .command('config')
  .description('Configure application interactively')
  .action(async () => {
    const mainMenu = await inquirer.prompt([
      {
        type: 'list',
        name: 'action',
        message: 'What would you like to do?',
        choices: [
          { name: 'View configuration', value: 'view' },
          { name: 'Edit configuration', value: 'edit' },
          { name: 'Reset to defaults', value: 'reset' },
          { name: 'Exit', value: 'exit' },
        ],
      },
    ]);

    switch (mainMenu.action) {
      case 'view':
        console.log(chalk.blue('\nCurrent configuration:'));
        console.log(JSON.stringify(getConfig(), null, 2));
        break;

      case 'edit':
        const config = await inquirer.prompt([
          {
            type: 'input',
            name: 'apiUrl',
            message: 'API URL:',
            default: getConfig().apiUrl,
          },
          {
            type: 'number',
            name: 'timeout',
            message: 'Request timeout (ms):',
            default: getConfig().timeout,
          },
          {
            type: 'list',
            name: 'logLevel',
            message: 'Log level:',
            choices: ['debug', 'info', 'warn', 'error'],
            default: getConfig().logLevel,
          },
        ]);
        saveConfig(config);
        console.log(chalk.green('✓ Configuration saved'));
        break;

      case 'reset':
        const { confirmReset } = await inquirer.prompt([
          {
            type: 'confirm',
            name: 'confirmReset',
            message: 'Reset to default configuration?',
            default: false,
          },
        ]);
        if (confirmReset) {
          resetConfig();
          console.log(chalk.green('✓ Configuration reset'));
        }
        break;

      case 'exit':
        console.log(chalk.gray('Goodbye!'));
        break;
    }
  });

// Multi-step wizard
program
  .command('wizard')
  .description('Run setup wizard')
  .action(async () => {
    console.log(chalk.blue('🧙 Welcome to the setup wizard\n'));

    // Step 1: Basic info
    console.log(chalk.bold('Step 1: Basic Information'));
    const step1 = await inquirer.prompt([
      {
        type: 'input',
        name: 'projectName',
        message: 'Project name:',
      },
      {
        type: 'input',
        name: 'description',
        message: 'Description:',
      },
    ]);

    // Step 2: Technology stack
    console.log(chalk.bold('\nStep 2: Technology Stack'));
    const step2 = await inquirer.prompt([
      {
        type: 'list',
        name: 'language',
        message: 'Primary language:',
        choices: ['TypeScript', 'JavaScript', 'Python', 'Go', 'Rust'],
      },
      {
        type: 'checkbox',
        name: 'frameworks',
        message: 'Select frameworks:',
        choices: (answers) => {
          const frameworksByLanguage: Record<string, string[]> = {
            TypeScript: ['Next.js', 'Express', 'NestJS'],
            JavaScript: ['React', 'Vue', 'Express'],
            Python: ['FastAPI', 'Django', 'Flask'],
            Go: ['Gin', 'Echo', 'Fiber'],
            Rust: ['Actix', 'Rocket', 'Axum'],
          };
          return frameworksByLanguage[answers.language] || [];
        },
      },
    ]);

    // Step 3: Infrastructure
    console.log(chalk.bold('\nStep 3: Infrastructure'));
    const step3 = await inquirer.prompt([
      {
        type: 'list',
        name: 'database',
        message: 'Database:',
        choices: ['PostgreSQL', 'MySQL', 'MongoDB', 'SQLite', 'None'],
      },
      {
        type: 'checkbox',
        name: 'services',
        message: 'Additional services:',
        choices: ['Redis', 'ElasticSearch', 'RabbitMQ', 'S3'],
      },
    ]);

    // Summary
    const config = { ...step1, ...step2, ...step3 };

    console.log(chalk.bold('\n📋 Configuration Summary:'));
    console.log(JSON.stringify(config, null, 2));

    const { confirm } = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'confirm',
        message: 'Create project with this configuration?',
        default: true,
      },
    ]);

    if (confirm) {
      console.log(chalk.green('\n✓ Project created successfully!'));
    } else {
      console.log(chalk.yellow('\n✗ Project creation cancelled'));
    }
  });

// Helper functions
async function initProject(config: any) {
  console.log(chalk.blue('\nInitializing project...'));
  console.log('Name:', config.name);
  console.log('Template:', config.template);
  console.log('Features:', config.features.join(', '));
  console.log(chalk.green('\n✓ Project initialized!'));
}

async function deploy(config: any) {
  console.log(chalk.blue('\nDeploying...'));
  console.log(JSON.stringify(config, null, 2));
  console.log(chalk.green('\n✓ Deployment complete!'));
}

function getConfig() {
  return {
    apiUrl: 'https://api.example.com',
    timeout: 5000,
    logLevel: 'info',
  };
}

function saveConfig(config: any) {
  console.log('Saving config:', config);
}

function resetConfig() {
  console.log('Resetting config to defaults');
}

program.parse();
