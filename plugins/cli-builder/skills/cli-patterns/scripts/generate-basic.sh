#!/bin/bash
# Generate basic CLI structure with urfave/cli

set -euo pipefail

APP_NAME="${1:-myapp}"

echo "Generating basic CLI: $APP_NAME"

# Create project structure
mkdir -p "$APP_NAME"
cd "$APP_NAME"

# Initialize Go module
go mod init "$APP_NAME" 2>/dev/null || true

# Install urfave/cli
echo "Installing urfave/cli v2..."
go get github.com/urfave/cli/v2@latest

# Create main.go
cat > main.go <<'EOF'
package main

import (
	"fmt"
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

func main() {
	app := &cli.App{
		Name:    "APP_NAME_PLACEHOLDER",
		Usage:   "A simple CLI tool",
		Version: "0.1.0",
		Flags: []cli.Flag{
			&cli.BoolFlag{
				Name:    "verbose",
				Aliases: []string{"v"},
				Usage:   "Enable verbose output",
				EnvVars: []string{"VERBOSE"},
			},
			&cli.StringFlag{
				Name:    "config",
				Aliases: []string{"c"},
				Usage:   "Path to config file",
				EnvVars: []string{"CONFIG_PATH"},
			},
		},
		Action: func(c *cli.Context) error {
			verbose := c.Bool("verbose")
			config := c.String("config")

			if verbose {
				fmt.Println("Verbose mode enabled")
			}

			if config != "" {
				fmt.Printf("Using config: %s\n", config)
			}

			fmt.Println("Hello from APP_NAME_PLACEHOLDER!")
			return nil
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
EOF

# Replace placeholder
sed -i "s/APP_NAME_PLACEHOLDER/$APP_NAME/g" main.go

# Create README
cat > README.md <<EOF
# $APP_NAME

A CLI tool built with urfave/cli.

## Installation

\`\`\`bash
go install
\`\`\`

## Usage

\`\`\`bash
$APP_NAME --help
$APP_NAME --verbose
$APP_NAME --config config.yaml
\`\`\`

## Environment Variables

- \`VERBOSE\`: Enable verbose output
- \`CONFIG_PATH\`: Path to config file
EOF

# Build
echo "Building..."
go build -o "$APP_NAME" .

echo "✅ Basic CLI generated successfully!"
echo "Run: ./$APP_NAME --help"
