/**
 * Comprehensive CLI Example
 *
 * Complete project initialization wizard combining all prompt types:
 * - Text input with validation
 * - List selections
 * - Checkbox selections
 * - Password input
 * - Autocomplete (optional)
 * - Conditional logic
 */

import inquirer from 'inquirer';

async function projectInitWizard() {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           🚀 Project Initialization Wizard 🚀             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
  `);

  const config = await inquirer.prompt([
    // === PROJECT BASICS ===
    {
      type: 'input',
      name: 'projectName',
      message: '📦 Project name:',
      validate: (input) => {
        if (input.length === 0) return 'Project name is required';
        if (!/^[a-z0-9-_]+$/.test(input)) {
          return 'Use lowercase letters, numbers, hyphens, and underscores only';
        }
        if (input.length < 3) return 'Project name must be at least 3 characters';
        return true;
      },
      transformer: (input) => input.toLowerCase()
    },
    {
      type: 'input',
      name: 'description',
      message: '📝 Project description:',
      validate: (input) => input.length > 0 || 'Description is required'
    },
    {
      type: 'input',
      name: 'version',
      message: '🏷️  Initial version:',
      default: '0.1.0',
      validate: (input) => {
        return /^\d+\.\d+\.\d+$/.test(input) || 'Use semantic versioning (e.g., 0.1.0)';
      }
    },
    {
      type: 'input',
      name: 'author',
      message: '👤 Author name:',
      default: process.env.USER || ''
    },
    {
      type: 'input',
      name: 'email',
      message: '📧 Author email:',
      validate: (input) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(input) || 'Invalid email address';
      }
    },
    {
      type: 'list',
      name: 'license',
      message: '📜 License:',
      choices: ['MIT', 'Apache-2.0', 'GPL-3.0', 'BSD-3-Clause', 'ISC', 'Unlicensed'],
      default: 'MIT'
    },

    // === TECHNOLOGY STACK ===
    {
      type: 'list',
      name: 'projectType',
      message: '🛠️  Project type:',
      choices: [
        'Web Application',
        'CLI Tool',
        'API/Backend',
        'Library/Package',
        'Desktop Application',
        'Mobile Application'
      ]
    },
    {
      type: 'list',
      name: 'language',
      message: '💻 Programming language:',
      choices: [
        { name: 'TypeScript (Recommended)', value: 'typescript', short: 'TS' },
        { name: 'JavaScript', value: 'javascript', short: 'JS' },
        { name: 'Python', value: 'python', short: 'Py' },
        { name: 'Go', value: 'go', short: 'Go' },
        { name: 'Rust', value: 'rust', short: 'Rust' }
      ]
    },
    {
      type: 'list',
      name: 'framework',
      message: '🎨 Framework/Runtime:',
      choices: (answers) => {
        const frameworks = {
          typescript: ['Next.js', 'Remix', 'Nest.js', 'Express', 'Fastify', 'Node.js'],
          javascript: ['React', 'Vue', 'Svelte', 'Express', 'Fastify', 'Node.js'],
          python: ['FastAPI', 'Django', 'Flask', 'Tornado', 'Sanic'],
          go: ['Gin', 'Echo', 'Fiber', 'Standard library'],
          rust: ['Actix', 'Rocket', 'Axum', 'Warp']
        };
        return frameworks[answers.language] || ['None'];
      }
    },

    // === FEATURES & TOOLS ===
    {
      type: 'checkbox',
      name: 'features',
      message: '✨ Select features:',
      choices: (answers) => {
        const baseFeatures = [
          { name: 'Environment variables (.env)', value: 'env', checked: true },
          { name: 'Configuration management', value: 'config', checked: true },
          { name: 'Logging', value: 'logging', checked: true },
          { name: 'Error handling', value: 'error-handling', checked: true }
        ];

        if (answers.projectType === 'Web Application' || answers.projectType === 'API/Backend') {
          baseFeatures.push(
            { name: 'Authentication', value: 'auth' },
            { name: 'Database integration', value: 'database' },
            { name: 'API documentation', value: 'api-docs' },
            { name: 'CORS handling', value: 'cors' }
          );
        }

        if (answers.projectType === 'CLI Tool') {
          baseFeatures.push(
            { name: 'Command-line arguments parser', value: 'cli-parser', checked: true },
            { name: 'Interactive prompts', value: 'prompts', checked: true },
            { name: 'Progress bars', value: 'progress' }
          );
        }

        return baseFeatures;
      },
      validate: (choices) => choices.length > 0 || 'Select at least one feature'
    },
    {
      type: 'checkbox',
      name: 'devTools',
      message: '🔧 Development tools:',
      choices: (answers) => {
        const tools = [];

        if (['typescript', 'javascript'].includes(answers.language)) {
          tools.push(
            { name: 'ESLint - Linting', value: 'eslint', checked: true },
            { name: 'Prettier - Code formatting', value: 'prettier', checked: true },
            { name: 'Husky - Git hooks', value: 'husky' },
            { name: 'Jest - Testing framework', value: 'jest', checked: true },
            { name: 'TypeDoc/JSDoc - Documentation', value: 'docs' }
          );
        } else if (answers.language === 'python') {
          tools.push(
            { name: 'Black - Code formatting', value: 'black', checked: true },
            { name: 'Flake8 - Linting', value: 'flake8', checked: true },
            { name: 'mypy - Type checking', value: 'mypy' },
            { name: 'pytest - Testing framework', value: 'pytest', checked: true },
            { name: 'Sphinx - Documentation', value: 'sphinx' }
          );
        }

        return tools;
      },
      default: ['eslint', 'prettier', 'jest']
    },

    // === DATABASE CONFIGURATION ===
    {
      type: 'confirm',
      name: 'useDatabase',
      message: '🗄️  Use database?',
      default: (answers) => {
        return answers.features.includes('database') ||
               ['Web Application', 'API/Backend'].includes(answers.projectType);
      },
      when: (answers) => ['Web Application', 'API/Backend', 'CLI Tool'].includes(answers.projectType)
    },
    {
      type: 'list',
      name: 'databaseType',
      message: '📊 Database type:',
      choices: [
        { name: '🐘 PostgreSQL (Relational)', value: 'postgresql' },
        { name: '🐬 MySQL (Relational)', value: 'mysql' },
        { name: '🍃 MongoDB (Document)', value: 'mongodb' },
        { name: '⚡ Redis (Key-Value)', value: 'redis' },
        { name: '📁 SQLite (Embedded)', value: 'sqlite' },
        { name: '🔥 Supabase (PostgreSQL + APIs)', value: 'supabase' }
      ],
      when: (answers) => answers.useDatabase
    },
    {
      type: 'list',
      name: 'databaseORM',
      message: '🔗 ORM/Database client:',
      choices: (answers) => {
        const orms = {
          typescript: {
            postgresql: ['Prisma', 'TypeORM', 'Kysely', 'Drizzle'],
            mysql: ['Prisma', 'TypeORM', 'Kysely', 'Drizzle'],
            mongodb: ['Mongoose', 'Prisma', 'TypeORM'],
            sqlite: ['Prisma', 'TypeORM', 'Better-SQLite3'],
            supabase: ['Supabase Client', 'Prisma']
          },
          python: {
            postgresql: ['SQLAlchemy', 'Django ORM', 'Tortoise ORM'],
            mysql: ['SQLAlchemy', 'Django ORM', 'Tortoise ORM'],
            mongodb: ['Motor', 'PyMongo', 'MongoEngine'],
            sqlite: ['SQLAlchemy', 'Django ORM']
          }
        };

        const lang = answers.language;
        const db = answers.databaseType;
        return orms[lang]?.[db] || ['None'];
      },
      when: (answers) => answers.useDatabase && answers.databaseType !== 'redis'
    },

    // === TESTING CONFIGURATION ===
    {
      type: 'confirm',
      name: 'setupTesting',
      message: '🧪 Setup testing?',
      default: true
    },
    {
      type: 'checkbox',
      name: 'testTypes',
      message: '🔬 Test types:',
      choices: [
        { name: 'Unit tests', value: 'unit', checked: true },
        { name: 'Integration tests', value: 'integration', checked: true },
        { name: 'E2E tests', value: 'e2e' },
        { name: 'Performance tests', value: 'performance' }
      ],
      when: (answers) => answers.setupTesting
    },

    // === CI/CD CONFIGURATION ===
    {
      type: 'confirm',
      name: 'setupCICD',
      message: '⚙️  Setup CI/CD?',
      default: true
    },
    {
      type: 'list',
      name: 'cicdProvider',
      message: '🔄 CI/CD provider:',
      choices: ['GitHub Actions', 'GitLab CI', 'CircleCI', 'Jenkins', 'None'],
      when: (answers) => answers.setupCICD
    },

    // === DEPLOYMENT CONFIGURATION ===
    {
      type: 'confirm',
      name: 'setupDeployment',
      message: '🚀 Setup deployment?',
      default: (answers) => answers.projectType !== 'Library/Package'
    },
    {
      type: 'list',
      name: 'deploymentPlatform',
      message: '☁️  Deployment platform:',
      choices: (answers) => {
        if (answers.projectType === 'Web Application') {
          return ['Vercel', 'Netlify', 'AWS', 'Google Cloud', 'Azure', 'Self-hosted'];
        } else if (answers.projectType === 'API/Backend') {
          return ['AWS', 'Google Cloud', 'Azure', 'DigitalOcean', 'Heroku', 'Self-hosted'];
        } else if (answers.projectType === 'CLI Tool') {
          return ['npm', 'PyPI', 'Homebrew', 'Binary releases', 'Docker'];
        }
        return ['AWS', 'Google Cloud', 'Azure', 'Self-hosted'];
      },
      when: (answers) => answers.setupDeployment
    },
    {
      type: 'confirm',
      name: 'useDocker',
      message: '🐳 Use Docker?',
      default: true,
      when: (answers) => {
        return answers.setupDeployment &&
               !['Vercel', 'Netlify'].includes(answers.deploymentPlatform);
      }
    },

    // === MONITORING & OBSERVABILITY ===
    {
      type: 'confirm',
      name: 'setupMonitoring',
      message: '📊 Setup monitoring & observability?',
      default: (answers) => answers.projectType !== 'Library/Package'
    },
    {
      type: 'checkbox',
      name: 'monitoringTools',
      message: '📈 Monitoring tools:',
      choices: [
        { name: 'Sentry - Error tracking', value: 'sentry' },
        { name: 'DataDog - Full observability', value: 'datadog' },
        { name: 'Prometheus - Metrics', value: 'prometheus' },
        { name: 'Grafana - Dashboards', value: 'grafana' },
        { name: 'New Relic - APM', value: 'newrelic' }
      ],
      when: (answers) => answers.setupMonitoring
    },

    // === DOCUMENTATION ===
    {
      type: 'confirm',
      name: 'generateDocs',
      message: '📚 Generate documentation?',
      default: true
    },
    {
      type: 'checkbox',
      name: 'docTypes',
      message: '📖 Documentation types:',
      choices: [
        { name: 'README.md', value: 'readme', checked: true },
        { name: 'API documentation', value: 'api', checked: true },
        { name: 'Contributing guidelines', value: 'contributing' },
        { name: 'Code of conduct', value: 'coc' },
        { name: 'Changelog', value: 'changelog', checked: true }
      ],
      when: (answers) => answers.generateDocs
    },

    // === SECURITY ===
    {
      type: 'confirm',
      name: 'securitySetup',
      message: '🔒 Setup security features?',
      default: true,
      when: (answers) => ['Web Application', 'API/Backend'].includes(answers.projectType)
    },
    {
      type: 'checkbox',
      name: 'securityFeatures',
      message: '🛡️  Security features:',
      choices: [
        { name: 'Dependency scanning', value: 'dep-scan', checked: true },
        { name: 'Secret scanning', value: 'secret-scan', checked: true },
        { name: 'HTTPS enforcement', value: 'https' },
        { name: 'Rate limiting', value: 'rate-limit' },
        { name: 'Input validation', value: 'validation', checked: true },
        { name: 'Security headers', value: 'headers' }
      ],
      when: (answers) => answers.securitySetup
    },

    // === FINAL CONFIRMATION ===
    {
      type: 'confirm',
      name: 'confirm',
      message: '✅ Initialize project with these settings?',
      default: true
    }
  ]);

  if (!config.confirm) {
    console.log('\n❌ Project initialization cancelled.\n');
    return null;
  }

  // Display configuration summary
  console.log('\n' + '═'.repeat(60));
  console.log('📋 PROJECT CONFIGURATION SUMMARY');
  console.log('═'.repeat(60) + '\n');

  console.log(`📦 Project: ${config.projectName} v${config.version}`);
  console.log(`📝 Description: ${config.description}`);
  console.log(`👤 Author: ${config.author} <${config.email}>`);
  console.log(`📜 License: ${config.license}\n`);

  console.log(`💻 Language: ${config.language}`);
  console.log(`🎨 Framework: ${config.framework}`);
  console.log(`🛠️  Type: ${config.projectType}\n`);

  if (config.useDatabase) {
    console.log(`🗄️  Database: ${config.databaseType}`);
    if (config.databaseORM) {
      console.log(`🔗 ORM: ${config.databaseORM}\n`);
    }
  }

  if (config.features.length > 0) {
    console.log(`✨ Features: ${config.features.join(', ')}`);
  }

  if (config.devTools.length > 0) {
    console.log(`🔧 Dev Tools: ${config.devTools.join(', ')}\n`);
  }

  if (config.setupDeployment) {
    console.log(`🚀 Deployment: ${config.deploymentPlatform}`);
    if (config.useDocker) console.log(`🐳 Docker: Enabled`);
  }

  if (config.setupCICD) {
    console.log(`⚙️  CI/CD: ${config.cicdProvider}`);
  }

  console.log('\n' + '═'.repeat(60) + '\n');

  console.log('🎉 Configuration complete! Initializing project...\n');

  // Here you would actually create the project files
  // This is just a demonstration

  return config;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  projectInitWizard()
    .then((config) => {
      if (config) {
        console.log('✅ Project initialized successfully!\n');
        console.log('Next steps:');
        console.log(`  1. cd ${config.projectName}`);
        console.log('  2. Install dependencies');
        console.log('  3. Start development');
      }
      process.exit(0);
    })
    .catch((error) => {
      if (error.isTtyError) {
        console.error('❌ Prompt could not be rendered in this environment');
      } else {
        console.error('❌ User interrupted prompt');
      }
      process.exit(1);
    });
}

export { projectInitWizard };
