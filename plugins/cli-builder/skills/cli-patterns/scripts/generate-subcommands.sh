#!/bin/bash
# Generate CLI with subcommands structure

set -euo pipefail

APP_NAME="${1:-myapp}"

echo "Generating CLI with subcommands: $APP_NAME"

# Create project structure
mkdir -p "$APP_NAME/commands"
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
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

func main() {
	app := &cli.App{
		Name:    "APP_NAME_PLACEHOLDER",
		Usage:   "A multi-command CLI tool",
		Version: "0.1.0",
		Commands: []*cli.Command{
			{
				Name:    "start",
				Aliases: []string{"s"},
				Usage:   "Start the service",
				Flags: []cli.Flag{
					&cli.IntFlag{
						Name:    "port",
						Aliases: []string{"p"},
						Value:   8080,
						Usage:   "Port to listen on",
					},
				},
				Action: func(c *cli.Context) error {
					return startCommand(c)
				},
			},
			{
				Name:    "stop",
				Usage:   "Stop the service",
				Action:  stopCommand,
			},
			{
				Name:    "status",
				Usage:   "Check service status",
				Action:  statusCommand,
			},
			{
				Name:    "config",
				Usage:   "Configuration management",
				Subcommands: []*cli.Command{
					{
						Name:   "show",
						Usage:  "Show current configuration",
						Action: configShowCommand,
					},
					{
						Name:   "set",
						Usage:  "Set configuration value",
						Action: configSetCommand,
					},
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
EOF

# Create commands.go
cat > commands.go <<'EOF'
package main

import (
	"fmt"

	"github.com/urfave/cli/v2"
)

func startCommand(c *cli.Context) error {
	port := c.Int("port")
	fmt.Printf("Starting service on port %d...\n", port)
	return nil
}

func stopCommand(c *cli.Context) error {
	fmt.Println("Stopping service...")
	return nil
}

func statusCommand(c *cli.Context) error {
	fmt.Println("Service status: running")
	return nil
}

func configShowCommand(c *cli.Context) error {
	fmt.Println("Current configuration:")
	fmt.Println("  port: 8080")
	fmt.Println("  host: localhost")
	return nil
}

func configSetCommand(c *cli.Context) error {
	key := c.Args().Get(0)
	value := c.Args().Get(1)

	if key == "" || value == "" {
		return fmt.Errorf("usage: config set <key> <value>")
	}

	fmt.Printf("Setting %s = %s\n", key, value)
	return nil
}
EOF

# Replace placeholder
sed -i "s/APP_NAME_PLACEHOLDER/$APP_NAME/g" main.go

# Create README
cat > README.md <<EOF
# $APP_NAME

A CLI tool with subcommands built with urfave/cli.

## Installation

\`\`\`bash
go install
\`\`\`

## Usage

\`\`\`bash
# Start service
$APP_NAME start --port 8080
$APP_NAME s -p 3000

# Stop service
$APP_NAME stop

# Check status
$APP_NAME status

# Configuration
$APP_NAME config show
$APP_NAME config set host 0.0.0.0
\`\`\`
EOF

# Build
echo "Building..."
go build -o "$APP_NAME" .

echo "✅ CLI with subcommands generated successfully!"
echo "Run: ./$APP_NAME --help"
