/**
 * List Selection Prompt Template
 *
 * Use for: Single choice from predefined options
 * Features: Arrow key navigation, search filtering
 */

import inquirer from 'inquirer';

async function listPromptExample() {
  const answers = await inquirer.prompt([
    {
      type: 'list',
      name: 'framework',
      message: 'Choose your preferred framework:',
      choices: [
        'React',
        'Vue',
        'Angular',
        'Svelte',
        'Next.js',
        'Nuxt.js'
      ],
      default: 'React'
    },
    {
      type: 'list',
      name: 'language',
      message: 'Choose programming language:',
      choices: [
        { name: 'JavaScript', value: 'js' },
        { name: 'TypeScript', value: 'ts' },
        { name: 'Python', value: 'py' },
        { name: 'Ruby', value: 'rb' },
        { name: 'Go', value: 'go' }
      ],
      default: 'ts'
    },
    {
      type: 'list',
      name: 'packageManager',
      message: 'Choose package manager:',
      choices: [
        { name: 'npm (Node Package Manager)', value: 'npm', short: 'npm' },
        { name: 'yarn (Fast, reliable package manager)', value: 'yarn', short: 'yarn' },
        { name: 'pnpm (Fast, disk space efficient)', value: 'pnpm', short: 'pnpm' },
        { name: 'bun (All-in-one toolkit)', value: 'bun', short: 'bun' }
      ]
    },
    {
      type: 'list',
      name: 'environment',
      message: 'Select deployment environment:',
      choices: [
        new inquirer.Separator('--- Cloud Platforms ---'),
        'AWS',
        'Google Cloud',
        'Azure',
        new inquirer.Separator('--- Serverless ---'),
        'Vercel',
        'Netlify',
        'Cloudflare Workers',
        new inquirer.Separator('--- Self-hosted ---'),
        'Docker',
        'Kubernetes'
      ]
    },
    {
      type: 'list',
      name: 'database',
      message: 'Choose database:',
      choices: [
        { name: '🐘 PostgreSQL (Relational)', value: 'postgresql' },
        { name: '🐬 MySQL (Relational)', value: 'mysql' },
        { name: '🍃 MongoDB (Document)', value: 'mongodb' },
        { name: '⚡ Redis (Key-Value)', value: 'redis' },
        { name: '📊 SQLite (Embedded)', value: 'sqlite' },
        { name: '🔥 Supabase (PostgreSQL + APIs)', value: 'supabase' }
      ],
      pageSize: 10
    }
  ]);

  console.log('\n✅ Selections:');
  console.log(JSON.stringify(answers, null, 2));

  return answers;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  listPromptExample()
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

export { listPromptExample };
