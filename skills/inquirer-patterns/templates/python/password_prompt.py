"""
Password Prompt Template

Use for: Sensitive input (credentials, tokens)
Features: Hidden input, confirmation, validation
"""

import questionary
import re
from questionary import ValidationError, Validator


class PasswordStrengthValidator(Validator):
    """Validator for password strength requirements"""

    def __init__(self, min_length=8, require_uppercase=True, require_lowercase=True,
                 require_digit=True, require_special=True):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special

    def validate(self, document):
        password = document.text
        issues = []

        if len(password) < self.min_length:
            issues.append(f"at least {self.min_length} characters")

        if self.require_uppercase and not re.search(r'[A-Z]', password):
            issues.append("an uppercase letter")

        if self.require_lowercase and not re.search(r'[a-z]', password):
            issues.append("a lowercase letter")

        if self.require_digit and not re.search(r'[0-9]', password):
            issues.append("a number")

        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            issues.append("a special character")

        if issues:
            raise ValidationError(
                message=f"Password must contain: {', '.join(issues)}",
                cursor_position=len(password)
            )


class APIKeyValidator(Validator):
    """Validator for API key format"""

    def validate(self, document):
        api_key = document.text

        if len(api_key) == 0:
            raise ValidationError(
                message="API key is required",
                cursor_position=0
            )

        if not (api_key.startswith('sk-') or api_key.startswith('pk-')):
            raise ValidationError(
                message='API key must start with "sk-" or "pk-"',
                cursor_position=len(api_key)
            )

        if len(api_key) < 32:
            raise ValidationError(
                message="API key appears to be too short",
                cursor_position=len(api_key)
            )


def calculate_password_strength(password):
    """Calculate password strength score"""
    strength = 0

    if len(password) >= 8:
        strength += 1
    if len(password) >= 12:
        strength += 1
    if re.search(r'[a-z]', password):
        strength += 1
    if re.search(r'[A-Z]', password):
        strength += 1
    if re.search(r'[0-9]', password):
        strength += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        strength += 1

    levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong']
    return levels[min(strength, len(levels) - 1)]


def password_prompt_example():
    """Example password prompts with validation"""

    print("\n🔒 Password Prompt Example\n")

    # Password with strength validation
    password = questionary.password(
        "Enter your password:",
        validate=PasswordStrengthValidator(min_length=8)
    ).ask()

    # Confirm password
    confirm_password = questionary.password(
        "Confirm your password:",
        validate=lambda text: text == password or "Passwords do not match"
    ).ask()

    print(f"\n✅ Password strength: {calculate_password_strength(password)}")

    # API key input
    api_key = questionary.password(
        "Enter your API key:",
        validate=APIKeyValidator()
    ).ask()

    print(f"✅ API key format: {api_key[:6]}...")

    # Optional encryption key
    encryption_key = questionary.password(
        "Enter encryption key (optional, press Enter to skip):",
        validate=lambda text: len(text) == 0 or len(text) >= 16 or "Encryption key must be at least 16 characters"
    ).ask()

    # Don't log actual passwords!
    answers = {
        'passwordSet': True,
        'passwordStrength': calculate_password_strength(password),
        'apiKeyPrefix': api_key[:6],
        'encryptionKeySet': len(encryption_key) > 0
    }

    print("\n✅ Credentials received (not displayed for security)")
    import json
    print(json.dumps(answers, indent=2))

    return answers


def secure_account_setup():
    """Example: Complete secure account setup"""

    print("\n🔐 Secure Account Setup\n")

    # Username
    username = questionary.text(
        "Username:",
        validate=lambda text: len(text) > 0 or "Username required"
    ).ask()

    # Strong password
    print("\n📝 Password requirements:")
    print("  • At least 12 characters")
    print("  • Uppercase and lowercase letters")
    print("  • Numbers")
    print("  • Special characters (!@#$%^&*)")
    print()

    password = questionary.password(
        "Password:",
        validate=PasswordStrengthValidator(
            min_length=12,
            require_uppercase=True,
            require_lowercase=True,
            require_digit=True,
            require_special=True
        )
    ).ask()

    # Confirm password
    confirm = questionary.password(
        "Confirm password:",
        validate=lambda text: text == password or "Passwords do not match"
    ).ask()

    # Optional: Remember credentials
    remember = questionary.confirm(
        "Remember credentials? (stored securely)",
        default=False
    ).ask()

    strength = calculate_password_strength(password)

    print(f"\n✅ Account created for: {username}")
    print(f"🔒 Password strength: {strength}")

    if remember:
        print("💾 Credentials will be stored securely")

    return {
        'username': username,
        'passwordStrength': strength,
        'remember': remember
    }


def database_credentials_setup():
    """Example: Database connection credentials"""

    print("\n🗄️  Database Credentials Setup\n")

    # Database username
    db_user = questionary.text(
        "Database username:",
        default="postgres",
        validate=lambda text: len(text) > 0 or "Username required"
    ).ask()

    # Database password
    db_password = questionary.password(
        "Database password:",
        validate=lambda text: len(text) >= 8 or "Password must be at least 8 characters"
    ).ask()

    # Admin password (if needed)
    is_admin = questionary.confirm(
        "Create admin user?",
        default=False
    ).ask()

    admin_password = None
    if is_admin:
        admin_password = questionary.password(
            "Admin password:",
            validate=PasswordStrengthValidator(min_length=12)
        ).ask()

        admin_confirm = questionary.password(
            "Confirm admin password:",
            validate=lambda text: text == admin_password or "Passwords do not match"
        ).ask()

        print(f"\n✅ Admin password strength: {calculate_password_strength(admin_password)}")

    credentials = {
        'dbUser': db_user,
        'dbPasswordSet': True,
        'adminConfigured': is_admin
    }

    print("\n✅ Database credentials configured")
    import json
    print(json.dumps(credentials, indent=2))

    return credentials


def api_token_setup():
    """Example: API token and secret key setup"""

    print("\n🔑 API Token Setup\n")

    # API key
    api_key = questionary.password(
        "Enter API key:",
        validate=lambda text: len(text) > 0 or "API key required"
    ).ask()

    # Secret key
    secret_key = questionary.password(
        "Enter secret key:",
        validate=lambda text: len(text) >= 32 or "Secret key must be at least 32 characters"
    ).ask()

    # Webhook secret (optional)
    use_webhooks = questionary.confirm(
        "Configure webhook authentication?",
        default=False
    ).ask()

    webhook_secret = None
    if use_webhooks:
        webhook_secret = questionary.password(
            "Webhook secret:",
            validate=lambda text: len(text) >= 16 or "Webhook secret must be at least 16 characters"
        ).ask()

    # Environment
    environment = questionary.select(
        "Environment:",
        choices=['Development', 'Staging', 'Production']
    ).ask()

    config = {
        'apiKeySet': True,
        'secretKeySet': True,
        'webhookConfigured': use_webhooks,
        'environment': environment
    }

    print("\n✅ API credentials configured")
    print(f"Environment: {environment}")

    return config


def password_change_flow():
    """Example: Password change with old password verification"""

    print("\n🔄 Change Password\n")

    # Old password (in real app, verify against stored hash)
    old_password = questionary.password(
        "Enter current password:",
        validate=lambda text: len(text) > 0 or "Current password required"
    ).ask()

    # New password
    new_password = questionary.password(
        "Enter new password:",
        validate=PasswordStrengthValidator(min_length=8)
    ).ask()

    # Ensure new password is different
    if new_password == old_password:
        print("\n❌ New password must be different from current password")
        return password_change_flow()

    # Confirm new password
    confirm_password = questionary.password(
        "Confirm new password:",
        validate=lambda text: text == new_password or "Passwords do not match"
    ).ask()

    print(f"\n✅ Password changed successfully")
    print(f"🔒 New password strength: {calculate_password_strength(new_password)}")

    return {'passwordChanged': True}


def main():
    """Run password prompt examples"""
    try:
        print("=== Password Prompt Examples ===")

        # Example 1: Basic password prompts
        password_prompt_example()

        # Example 2: Secure account setup
        secure_account_setup()

        # Example 3: Database credentials
        database_credentials_setup()

        # Example 4: API token setup
        api_token_setup()

        # Example 5: Password change
        password_change_flow()

        print("\n✅ Password prompt examples complete!")

    except KeyboardInterrupt:
        print("\n\n❌ User interrupted prompt")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
