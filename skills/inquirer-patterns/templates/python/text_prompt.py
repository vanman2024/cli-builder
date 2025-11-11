"""
Text Input Prompt Template

Use for: Names, emails, URLs, paths, free-form text
Features: Validation, default values, transform
"""

import questionary
import re
from questionary import ValidationError, Validator


class UsernameValidator(Validator):
    """Validate username format"""

    def validate(self, document):
        text = document.text
        if len(text) == 0:
            raise ValidationError(
                message='Username is required',
                cursor_position=len(text)
            )
        if len(text) < 3:
            raise ValidationError(
                message='Username must be at least 3 characters',
                cursor_position=len(text)
            )
        if not re.match(r'^[a-zA-Z0-9_-]+$', text):
            raise ValidationError(
                message='Username can only contain letters, numbers, hyphens, and underscores',
                cursor_position=len(text)
            )


class EmailValidator(Validator):
    """Validate email format"""

    def validate(self, document):
        text = document.text
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, text):
            raise ValidationError(
                message='Invalid email address',
                cursor_position=len(text)
            )


class URLValidator(Validator):
    """Validate URL format"""

    def validate(self, document):
        text = document.text
        if len(text) == 0:
            return  # Optional field
        url_regex = r'^https?://.+'
        if not re.match(url_regex, text):
            raise ValidationError(
                message='Must be a valid URL (http:// or https://)',
                cursor_position=len(text)
            )


class AgeValidator(Validator):
    """Validate age range"""

    def validate(self, document):
        text = document.text
        try:
            age = int(text)
            if age < 18:
                raise ValidationError(
                    message='You must be at least 18 years old',
                    cursor_position=len(text)
                )
            if age > 120:
                raise ValidationError(
                    message='Please enter a realistic age',
                    cursor_position=len(text)
                )
        except ValueError:
            raise ValidationError(
                message='Please enter a valid number',
                cursor_position=len(text)
            )


class BioValidator(Validator):
    """Validate bio length"""

    def validate(self, document):
        text = document.text
        if len(text) > 200:
            raise ValidationError(
                message='Bio must be 200 characters or less',
                cursor_position=len(text)
            )


def text_prompt_example():
    """Example text input prompts with validation"""

    print("\n📝 Text Input Example\n")

    # Username input
    username = questionary.text(
        "Enter your username:",
        validate=UsernameValidator
    ).ask()

    # Email input
    email = questionary.text(
        "Enter your email:",
        validate=EmailValidator
    ).ask()

    # Website input (optional)
    website = questionary.text(
        "Enter your website (optional):",
        default="",
        validate=URLValidator
    ).ask()

    # Age input with conversion
    age_str = questionary.text(
        "Enter your age:",
        validate=AgeValidator
    ).ask()
    age = int(age_str)

    # Bio input
    bio = questionary.text(
        "Enter a short bio:",
        validate=BioValidator,
        multiline=False
    ).ask()

    answers = {
        'username': username.lower(),
        'email': email,
        'website': website,
        'age': age,
        'bio': bio
    }

    print("\n✅ Answers received:")
    import json
    print(json.dumps(answers, indent=2))

    return answers


# Alternative: Using lambda validators
def lambda_validator_example():
    """Example using lambda validators for simpler cases"""

    print("\n📝 Lambda Validator Example\n")

    # Simple required field
    name = questionary.text(
        "Name:",
        validate=lambda text: len(text) > 0 or "Name is required"
    ).ask()

    # Email validation
    email = questionary.text(
        "Email:",
        validate=lambda text: bool(re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', text)) or "Invalid email"
    ).ask()

    # Numeric validation
    port = questionary.text(
        "Port number:",
        default="8000",
        validate=lambda text: text.isdigit() and 1 <= int(text) <= 65535 or "Invalid port (1-65535)"
    ).ask()

    # Path validation
    path = questionary.text(
        "Project path:",
        default="./my-project",
        validate=lambda text: len(text) > 0 or "Path is required"
    ).ask()

    answers = {
        'name': name,
        'email': email,
        'port': int(port),
        'path': path
    }

    print("\n✅ Answers received:")
    import json
    print(json.dumps(answers, indent=2))

    return answers


def main():
    """Run text prompt examples"""
    try:
        print("=== Text Prompt Examples ===")

        # Example 1: Class-based validators
        text_prompt_example()

        # Example 2: Lambda validators
        lambda_validator_example()

        print("\n✅ Text prompt examples complete!")

    except KeyboardInterrupt:
        print("\n\n❌ User interrupted prompt")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
