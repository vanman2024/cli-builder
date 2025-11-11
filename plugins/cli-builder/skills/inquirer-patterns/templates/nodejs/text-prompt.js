/**
 * Text Input Prompt Template
 *
 * Use for: Names, emails, URLs, paths, free-form text
 * Features: Validation, default values, transform
 */

import inquirer from 'inquirer';

async function textPromptExample() {
  const answers = await inquirer.prompt([
    {
      type: 'input',
      name: 'username',
      message: 'Enter your username:',
      default: '',
      validate: (input) => {
        if (input.length === 0) {
          return 'Username is required';
        }
        if (input.length < 3) {
          return 'Username must be at least 3 characters';
        }
        if (!/^[a-zA-Z0-9_-]+$/.test(input)) {
          return 'Username can only contain letters, numbers, hyphens, and underscores';
        }
        return true;
      },
      transformer: (input) => {
        return input.toLowerCase();
      }
    },
    {
      type: 'input',
      name: 'email',
      message: 'Enter your email:',
      validate: (input) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(input) || 'Invalid email address';
      }
    },
    {
      type: 'input',
      name: 'website',
      message: 'Enter your website (optional):',
      default: '',
      validate: (input) => {
        if (input.length === 0) return true; // Optional field
        const urlRegex = /^https?:\/\/.+/;
        return urlRegex.test(input) || 'Must be a valid URL (http:// or https://)';
      }
    },
    {
      type: 'input',
      name: 'age',
      message: 'Enter your age:',
      validate: (input) => {
        const age = parseInt(input);
        if (isNaN(age)) {
          return 'Please enter a valid number';
        }
        if (age < 18) {
          return 'You must be at least 18 years old';
        }
        if (age > 120) {
          return 'Please enter a realistic age';
        }
        return true;
      },
      filter: (input) => parseInt(input)
    },
    {
      type: 'input',
      name: 'bio',
      message: 'Enter a short bio:',
      validate: (input) => {
        if (input.length > 200) {
          return 'Bio must be 200 characters or less';
        }
        return true;
      }
    }
  ]);

  console.log('\n✅ Answers received:');
  console.log(JSON.stringify(answers, null, 2));

  return answers;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  textPromptExample()
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

export { textPromptExample };
