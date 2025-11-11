/**
 * Autocomplete Prompt Template
 *
 * Use for: Large option lists with search
 * Features: Type-ahead, fuzzy matching, suggestions
 *
 * Note: Requires inquirer-autocomplete-prompt plugin
 * Install: npm install inquirer-autocomplete-prompt
 */

import inquirer from 'inquirer';
import inquirerAutocomplete from 'inquirer-autocomplete-prompt';

// Register the autocomplete prompt type
inquirer.registerPrompt('autocomplete', inquirerAutocomplete);

// Example: Countries list for autocomplete
const countries = [
  'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola',
  'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
  'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus',
  'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia',
  'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi',
  'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Chad',
  'Chile', 'China', 'Colombia', 'Comoros', 'Congo',
  'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic',
  'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic',
  'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Ethiopia',
  'Fiji', 'Finland', 'France', 'Gabon', 'Gambia',
  'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada',
  'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras',
  'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
  'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica',
  'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait',
  'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia',
  'Libya', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi',
  'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mexico',
  'Moldova', 'Monaco', 'Mongolia', 'Morocco', 'Mozambique',
  'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand',
  'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman',
  'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines',
  'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia',
  'Rwanda', 'Saudi Arabia', 'Senegal', 'Serbia', 'Singapore',
  'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'South Korea',
  'Spain', 'Sri Lanka', 'Sudan', 'Sweden', 'Switzerland',
  'Syria', 'Taiwan', 'Tanzania', 'Thailand', 'Togo',
  'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'United Arab Emirates',
  'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan',
  'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'
];

// Example: NPM packages for autocomplete
const popularPackages = [
  'express', 'react', 'vue', 'angular', 'next', 'nuxt',
  'axios', 'lodash', 'moment', 'dayjs', 'uuid', 'dotenv',
  'typescript', 'eslint', 'prettier', 'jest', 'mocha', 'chai',
  'webpack', 'vite', 'rollup', 'babel', 'esbuild',
  'socket.io', 'redis', 'mongodb', 'mongoose', 'sequelize',
  'prisma', 'typeorm', 'knex', 'pg', 'mysql2',
  'bcrypt', 'jsonwebtoken', 'passport', 'helmet', 'cors',
  'multer', 'sharp', 'puppeteer', 'playwright', 'cheerio'
];

// Fuzzy search function
function fuzzySearch(input, choices) {
  if (!input) return choices;

  const searchTerm = input.toLowerCase();
  return choices.filter(choice => {
    const item = typeof choice === 'string' ? choice : choice.name;
    return item.toLowerCase().includes(searchTerm);
  });
}

async function autocompletePromptExample() {
  const answers = await inquirer.prompt([
    {
      type: 'autocomplete',
      name: 'country',
      message: 'Select your country:',
      source: (answersSoFar, input) => {
        return Promise.resolve(fuzzySearch(input, countries));
      },
      pageSize: 10
    },
    {
      type: 'autocomplete',
      name: 'package',
      message: 'Search for an npm package:',
      source: (answersSoFar, input) => {
        const filtered = fuzzySearch(input, popularPackages);
        return Promise.resolve(filtered);
      },
      pageSize: 8,
      validate: (input) => {
        return input.length > 0 || 'Please select a package';
      }
    },
    {
      type: 'autocomplete',
      name: 'city',
      message: 'Select city:',
      source: async (answersSoFar, input) => {
        // Example: Cities based on selected country
        const citiesByCountry = {
          'United States': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
          'United Kingdom': ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Liverpool'],
          'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
          'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'],
          'Germany': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne']
        };

        const cities = citiesByCountry[answersSoFar.country] || ['Capital City', 'Major City'];
        return fuzzySearch(input, cities);
      },
      when: (answers) => ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany'].includes(answers.country)
    }
  ]);

  console.log('\n✅ Selections:');
  console.log(JSON.stringify(answers, null, 2));

  return answers;
}

// Example: Framework/Library search
async function frameworkSearchExample() {
  const frameworks = [
    { name: 'React - UI library by Facebook', value: 'react' },
    { name: 'Vue.js - Progressive JavaScript framework', value: 'vue' },
    { name: 'Angular - Platform for building web apps', value: 'angular' },
    { name: 'Svelte - Cybernetically enhanced web apps', value: 'svelte' },
    { name: 'Next.js - React framework with SSR', value: 'next' },
    { name: 'Nuxt.js - Vue.js framework with SSR', value: 'nuxt' },
    { name: 'Remix - Full stack web framework', value: 'remix' },
    { name: 'SvelteKit - Svelte framework', value: 'sveltekit' },
    { name: 'Express - Fast Node.js web framework', value: 'express' },
    { name: 'Fastify - Fast and low overhead web framework', value: 'fastify' },
    { name: 'NestJS - Progressive Node.js framework', value: 'nestjs' },
    { name: 'Koa - Expressive middleware for Node.js', value: 'koa' }
  ];

  const answer = await inquirer.prompt([
    {
      type: 'autocomplete',
      name: 'framework',
      message: 'Search for a framework:',
      source: (answersSoFar, input) => {
        const filtered = fuzzySearch(input, frameworks);
        return Promise.resolve(filtered);
      },
      pageSize: 10
    }
  ]);

  console.log(`\n✅ Selected: ${answer.framework}`);
  return answer;
}

// Example: Command search with categories
async function commandSearchExample() {
  const commands = [
    { name: '📦 install - Install dependencies', value: 'install' },
    { name: '🚀 start - Start development server', value: 'start' },
    { name: '🏗️  build - Build for production', value: 'build' },
    { name: '🧪 test - Run tests', value: 'test' },
    { name: '🔍 lint - Check code quality', value: 'lint' },
    { name: '✨ format - Format code', value: 'format' },
    { name: '📝 generate - Generate files', value: 'generate' },
    { name: '🔄 update - Update dependencies', value: 'update' },
    { name: '🧹 clean - Clean build artifacts', value: 'clean' },
    { name: '🚢 deploy - Deploy application', value: 'deploy' },
    { name: '📊 analyze - Analyze bundle size', value: 'analyze' },
    { name: '🐛 debug - Start debugger', value: 'debug' }
  ];

  const answer = await inquirer.prompt([
    {
      type: 'autocomplete',
      name: 'command',
      message: 'Search for a command:',
      source: (answersSoFar, input) => {
        return Promise.resolve(fuzzySearch(input, commands));
      },
      pageSize: 12
    }
  ]);

  console.log(`\n✅ Running: ${answer.command}`);
  return answer;
}

// Example: Dynamic API search (simulated)
async function apiSearchExample() {
  console.log('\n🔍 API Endpoint Search\n');

  const answer = await inquirer.prompt([
    {
      type: 'autocomplete',
      name: 'endpoint',
      message: 'Search API endpoints:',
      source: async (answersSoFar, input) => {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 100));

        const endpoints = [
          { name: 'GET /users - List all users', value: '/users' },
          { name: 'GET /users/:id - Get user by ID', value: '/users/:id' },
          { name: 'POST /users - Create new user', value: '/users' },
          { name: 'PUT /users/:id - Update user', value: '/users/:id' },
          { name: 'DELETE /users/:id - Delete user', value: '/users/:id' },
          { name: 'GET /posts - List all posts', value: '/posts' },
          { name: 'GET /posts/:id - Get post by ID', value: '/posts/:id' },
          { name: 'POST /posts - Create new post', value: '/posts' },
          { name: 'GET /comments - List comments', value: '/comments' },
          { name: 'POST /auth/login - User login', value: '/auth/login' },
          { name: 'POST /auth/register - User registration', value: '/auth/register' },
          { name: 'POST /auth/logout - User logout', value: '/auth/logout' }
        ];

        return fuzzySearch(input, endpoints);
      },
      pageSize: 10
    }
  ]);

  console.log(`\n✅ Selected endpoint: ${answer.endpoint}`);
  return answer;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  (async () => {
    console.log('=== Autocomplete Examples ===\n');

    console.log('1. Country & Package Selection');
    await autocompletePromptExample();

    console.log('\n2. Framework Search');
    await frameworkSearchExample();

    console.log('\n3. Command Search');
    await commandSearchExample();

    console.log('\n4. API Endpoint Search');
    await apiSearchExample();

    process.exit(0);
  })().catch((error) => {
    if (error.isTtyError) {
      console.error('❌ Prompt could not be rendered in this environment');
    } else {
      console.error('❌ User interrupted prompt');
    }
    process.exit(1);
  });
}

export { autocompletePromptExample, frameworkSearchExample, commandSearchExample, apiSearchExample };
