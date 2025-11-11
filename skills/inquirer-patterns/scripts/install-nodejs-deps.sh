#!/bin/bash

# install-nodejs-deps.sh
# Install Node.js dependencies for inquirer patterns

set -e

echo "📦 Installing Node.js dependencies for inquirer patterns..."
echo

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    echo "Please install Node.js and npm first"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 14 ]; then
    echo "⚠️  Warning: Node.js 14 or higher is recommended"
    echo "Current version: $(node --version)"
fi

# Create package.json if it doesn't exist
if [ ! -f "package.json" ]; then
    echo "📝 Creating package.json..."
    cat > package.json << 'EOF'
{
  "name": "inquirer-patterns-examples",
  "version": "1.0.0",
  "description": "Interactive prompt patterns for CLI tools",
  "type": "module",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": ["inquirer", "cli", "prompts", "interactive"],
  "author": "",
  "license": "MIT"
}
EOF
    echo "✅ package.json created"
fi

# Install core dependencies
echo "📥 Installing inquirer..."
npm install inquirer@^9.0.0

echo "📥 Installing inquirer-autocomplete-prompt..."
npm install inquirer-autocomplete-prompt@^3.0.0

# Optional: Install chalk for colored output
echo "📥 Installing chalk (optional, for colored output)..."
npm install chalk@^5.0.0

echo
echo "✅ All Node.js dependencies installed successfully!"
echo
echo "📚 Installed packages:"
echo "  - inquirer@^9.0.0"
echo "  - inquirer-autocomplete-prompt@^3.0.0"
echo "  - chalk@^5.0.0"
echo
echo "🚀 You can now run the examples:"
echo "  node templates/nodejs/text-prompt.js"
echo "  node templates/nodejs/list-prompt.js"
echo "  node templates/nodejs/checkbox-prompt.js"
echo "  node templates/nodejs/password-prompt.js"
echo "  node templates/nodejs/autocomplete-prompt.js"
echo "  node templates/nodejs/conditional-prompt.js"
echo "  node templates/nodejs/comprehensive-example.js"
echo
