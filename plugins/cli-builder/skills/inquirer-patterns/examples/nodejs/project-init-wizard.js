/**
 * Example: Complete Project Initialization Wizard
 *
 * Demonstrates combining multiple prompt types to create
 * a comprehensive CLI tool for project setup
 */

import inquirer from 'inquirer';

async function projectInitWizard() {
  console.log('\n╔════════════════════════════════════════╗');
  console.log('║  🚀 Project Initialization Wizard 🚀  ║');
  console.log('╚════════════════════════════════════════╝\n');

  const config = await inquirer.prompt([
    // Project basics
    {
      type: 'input',
      name: 'name',
      message: 'Project name:',
      validate: (input) => {
        if (!/^[a-z0-9-]+$/.test(input)) {
          return 'Use lowercase letters, numbers, and hyphens only';
        }
        return true;
      }
    },
    {
      type: 'input',
      name: 'description',
      message: 'Description:',
      validate: (input) => input.length > 0 || 'Description required'
    },
    {
      type: 'list',
      name: 'language',
      message: 'Programming language:',
      choices: ['TypeScript', 'JavaScript', 'Python', 'Go', 'Rust']
    },
    {
      type: 'list',
      name: 'framework',
      message: 'Framework:',
      choices: (answers) => {
        const frameworks = {
          TypeScript: ['Next.js', 'Nest.js', 'Express', 'Fastify'],
          JavaScript: ['React', 'Vue', 'Express', 'Koa'],
          Python: ['FastAPI', 'Django', 'Flask'],
          Go: ['Gin', 'Echo', 'Fiber'],
          Rust: ['Actix', 'Rocket', 'Axum']
        };
        return frameworks[answers.language] || ['None'];
      }
    },
    {
      type: 'checkbox',
      name: 'features',
      message: 'Select features:',
      choices: [
        { name: 'Database', value: 'database', checked: true },
        { name: 'Authentication', value: 'auth' },
        { name: 'API Documentation', value: 'docs' },
        { name: 'Testing', value: 'testing', checked: true },
        { name: 'Logging', value: 'logging', checked: true }
      ]
    },
    {
      type: 'confirm',
      name: 'useDocker',
      message: 'Use Docker?',
      default: true
    },
    {
      type: 'confirm',
      name: 'setupCI',
      message: 'Setup CI/CD?',
      default: true
    }
  ]);

  console.log('\n✅ Configuration complete!\n');
  console.log(JSON.stringify(config, null, 2));

  return config;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  projectInitWizard()
    .then(() => process.exit(0))
    .catch(console.error);
}

export { projectInitWizard };
