/**
 * Password Prompt Template
 *
 * Use for: Sensitive input (credentials, tokens)
 * Features: Hidden input, confirmation, validation
 */

import inquirer from 'inquirer';

async function passwordPromptExample() {
  const answers = await inquirer.prompt([
    {
      type: 'password',
      name: 'password',
      message: 'Enter your password:',
      mask: '*',
      validate: (input) => {
        if (input.length < 8) {
          return 'Password must be at least 8 characters';
        }
        if (!/[A-Z]/.test(input)) {
          return 'Password must contain at least one uppercase letter';
        }
        if (!/[a-z]/.test(input)) {
          return 'Password must contain at least one lowercase letter';
        }
        if (!/[0-9]/.test(input)) {
          return 'Password must contain at least one number';
        }
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(input)) {
          return 'Password must contain at least one special character';
        }
        return true;
      }
    },
    {
      type: 'password',
      name: 'confirmPassword',
      message: 'Confirm your password:',
      mask: '*',
      validate: (input, answers) => {
        if (input !== answers.password) {
          return 'Passwords do not match';
        }
        return true;
      }
    },
    {
      type: 'password',
      name: 'apiKey',
      message: 'Enter your API key:',
      mask: '•',
      validate: (input) => {
        if (input.length === 0) {
          return 'API key is required';
        }
        // Example: Validate API key format (e.g., sk-...)
        if (!input.startsWith('sk-') && !input.startsWith('pk-')) {
          return 'API key must start with "sk-" or "pk-"';
        }
        if (input.length < 32) {
          return 'API key appears to be too short';
        }
        return true;
      }
    },
    {
      type: 'password',
      name: 'oldPassword',
      message: 'Enter your old password (for password change):',
      mask: '*',
      when: (answers) => {
        // Only ask for old password if changing password
        return answers.password && answers.confirmPassword;
      },
      validate: (input) => {
        if (input.length === 0) {
          return 'Old password is required';
        }
        // In real app, you'd verify against stored password
        return true;
      }
    },
    {
      type: 'password',
      name: 'encryptionKey',
      message: 'Enter encryption key (optional):',
      mask: '#',
      validate: (input) => {
        if (input.length === 0) return true; // Optional
        if (input.length < 16) {
          return 'Encryption key must be at least 16 characters';
        }
        return true;
      }
    }
  ]);

  // Don't log actual passwords!
  console.log('\n✅ Credentials received (not displayed for security)');
  console.log('Password strength:', calculatePasswordStrength(answers.password));
  console.log('API key format:', answers.apiKey.substring(0, 6) + '...');

  // In real app, you'd:
  // - Hash the password before storing
  // - Encrypt the API key
  // - Store securely (not in plain text)

  return {
    passwordHash: hashPassword(answers.password),
    apiKeyEncrypted: encryptApiKey(answers.apiKey)
  };
}

// Helper function to calculate password strength
function calculatePasswordStrength(password) {
  let strength = 0;

  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;
  if (/[a-z]/.test(password)) strength++;
  if (/[A-Z]/.test(password)) strength++;
  if (/[0-9]/.test(password)) strength++;
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;

  const levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
  return levels[Math.min(strength, levels.length - 1)];
}

// Placeholder for password hashing (use bcrypt in production)
function hashPassword(password) {
  return `[HASHED:${password.length}_chars]`;
}

// Placeholder for API key encryption (use proper encryption in production)
function encryptApiKey(apiKey) {
  return `[ENCRYPTED:${apiKey.substring(0, 6)}...]`;
}

// Example: Secure credential storage
async function securePasswordExample() {
  console.log('\n🔐 Secure Password Setup\n');

  const credentials = await inquirer.prompt([
    {
      type: 'input',
      name: 'username',
      message: 'Username:',
      validate: (input) => input.length > 0 || 'Username required'
    },
    {
      type: 'password',
      name: 'password',
      message: 'Password:',
      mask: '*',
      validate: (input) => {
        const issues = [];
        if (input.length < 12) issues.push('at least 12 characters');
        if (!/[A-Z]/.test(input)) issues.push('an uppercase letter');
        if (!/[a-z]/.test(input)) issues.push('a lowercase letter');
        if (!/[0-9]/.test(input)) issues.push('a number');
        if (!/[!@#$%^&*]/.test(input)) issues.push('a special character (!@#$%^&*)');

        if (issues.length > 0) {
          return `Password must contain: ${issues.join(', ')}`;
        }
        return true;
      }
    },
    {
      type: 'password',
      name: 'confirm',
      message: 'Confirm password:',
      mask: '*',
      validate: (input, answers) => {
        return input === answers.password || 'Passwords do not match';
      }
    },
    {
      type: 'confirm',
      name: 'remember',
      message: 'Remember credentials? (stored securely)',
      default: false
    }
  ]);

  console.log(`\n✅ Account created for: ${credentials.username}`);
  console.log(`🔒 Password strength: ${calculatePasswordStrength(credentials.password)}`);

  return credentials;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  passwordPromptExample()
    .then(() => securePasswordExample())
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

export { passwordPromptExample, securePasswordExample };
