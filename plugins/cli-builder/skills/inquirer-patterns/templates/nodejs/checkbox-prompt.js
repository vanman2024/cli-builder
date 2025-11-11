/**
 * Checkbox Prompt Template
 *
 * Use for: Multiple selections from options
 * Features: Space to toggle, Enter to confirm
 */

import inquirer from 'inquirer';

async function checkboxPromptExample() {
  const answers = await inquirer.prompt([
    {
      type: 'checkbox',
      name: 'features',
      message: 'Select features to include:',
      choices: [
        'Authentication',
        'Authorization',
        'Database Integration',
        'API Documentation',
        'Testing Suite',
        'CI/CD Pipeline',
        'Monitoring',
        'Logging'
      ],
      validate: (choices) => {
        if (choices.length === 0) {
          return 'You must select at least one feature';
        }
        return true;
      }
    },
    {
      type: 'checkbox',
      name: 'tools',
      message: 'Select development tools:',
      choices: [
        { name: 'ESLint (Linting)', value: 'eslint', checked: true },
        { name: 'Prettier (Formatting)', value: 'prettier', checked: true },
        { name: 'Jest (Testing)', value: 'jest' },
        { name: 'Husky (Git Hooks)', value: 'husky' },
        { name: 'TypeDoc (Documentation)', value: 'typedoc' },
        { name: 'Webpack (Bundling)', value: 'webpack' }
      ]
    },
    {
      type: 'checkbox',
      name: 'plugins',
      message: 'Select plugins to install:',
      choices: [
        new inquirer.Separator('=== Essential ==='),
        { name: 'dotenv - Environment variables', value: 'dotenv', checked: true },
        { name: 'axios - HTTP client', value: 'axios', checked: true },
        new inquirer.Separator('=== Utilities ==='),
        { name: 'lodash - Utility functions', value: 'lodash' },
        { name: 'dayjs - Date manipulation', value: 'dayjs' },
        { name: 'uuid - Unique IDs', value: 'uuid' },
        new inquirer.Separator('=== Validation ==='),
        { name: 'joi - Schema validation', value: 'joi' },
        { name: 'zod - TypeScript-first validation', value: 'zod' },
        new inquirer.Separator('=== Advanced ==='),
        { name: 'bull - Job queues', value: 'bull' },
        { name: 'socket.io - WebSockets', value: 'socket.io' }
      ],
      pageSize: 15,
      validate: (choices) => {
        if (choices.length > 10) {
          return 'Please select no more than 10 plugins to avoid bloat';
        }
        return true;
      }
    },
    {
      type: 'checkbox',
      name: 'permissions',
      message: 'Grant the following permissions:',
      choices: [
        { name: '📁 Read files', value: 'read', checked: true },
        { name: '✏️  Write files', value: 'write' },
        { name: '🗑️  Delete files', value: 'delete' },
        { name: '🌐 Network access', value: 'network', checked: true },
        { name: '🖥️  System commands', value: 'system' },
        { name: '🔒 Keychain access', value: 'keychain' }
      ],
      validate: (choices) => {
        if (choices.includes('delete') && !choices.includes('write')) {
          return 'Delete permission requires write permission';
        }
        return true;
      }
    },
    {
      type: 'checkbox',
      name: 'environments',
      message: 'Select deployment environments:',
      choices: [
        { name: 'Development', value: 'dev', checked: true },
        { name: 'Staging', value: 'staging' },
        { name: 'Production', value: 'prod' },
        { name: 'Testing', value: 'test', checked: true }
      ],
      validate: (choices) => {
        if (!choices.includes('dev')) {
          return 'Development environment is required';
        }
        if (choices.includes('prod') && !choices.includes('staging')) {
          return 'Staging environment is recommended before production';
        }
        return true;
      }
    }
  ]);

  console.log('\n✅ Selected options:');
  console.log(JSON.stringify(answers, null, 2));

  // Example: Process selections
  console.log('\n📦 Installing selected features...');
  answers.features.forEach(feature => {
    console.log(`  - ${feature}`);
  });

  return answers;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  checkboxPromptExample()
    .then(() => process.exit(0))
    .catch((error) => {
      if (error.isTtyError) {
        console.error('❌ Prompt could not be rendered in this environment');
      } else {
        console.error('❌ User interrupted prompt');
      }
      process.exit(1);
    });
}

export { checkboxPromptExample };
