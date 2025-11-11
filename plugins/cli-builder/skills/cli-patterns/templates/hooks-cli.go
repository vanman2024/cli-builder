package main

import (
	"fmt"
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

func main() {
	app := &cli.App{
		Name:  "hooks-demo",
		Usage: "Demonstration of Before/After hooks",

		// Global Before hook - runs before any command
		Before: func(c *cli.Context) error {
			fmt.Println("🚀 [GLOBAL BEFORE] Initializing application...")
			fmt.Println("   - Loading configuration")
			fmt.Println("   - Setting up connections")
			return nil
		},

		// Global After hook - runs after any command
		After: func(c *cli.Context) error {
			fmt.Println("✅ [GLOBAL AFTER] Cleaning up...")
			fmt.Println("   - Closing connections")
			fmt.Println("   - Saving state")
			return nil
		},

		Commands: []*cli.Command{
			{
				Name:  "process",
				Usage: "Process data with hooks",

				// Command-specific Before hook
				Before: func(c *cli.Context) error {
					fmt.Println("  [COMMAND BEFORE] Preparing to process...")
					fmt.Println("    - Validating input")
					return nil
				},

				// Command action
				Action: func(c *cli.Context) error {
					fmt.Println("    [ACTION] Processing data...")
					return nil
				},

				// Command-specific After hook
				After: func(c *cli.Context) error {
					fmt.Println("  [COMMAND AFTER] Processing complete!")
					return nil
				},
			},

			{
				Name:  "validate",
				Usage: "Validate configuration",

				Before: func(c *cli.Context) error {
					fmt.Println("  [COMMAND BEFORE] Starting validation...")
					return nil
				},

				Action: func(c *cli.Context) error {
					fmt.Println("    [ACTION] Validating...")
					return nil
				},

				After: func(c *cli.Context) error {
					fmt.Println("  [COMMAND AFTER] Validation complete!")
					return nil
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}

// Example output when running "hooks-demo process":
// 🚀 [GLOBAL BEFORE] Initializing application...
//    - Loading configuration
//    - Setting up connections
//   [COMMAND BEFORE] Preparing to process...
//     - Validating input
//     [ACTION] Processing data...
//   [COMMAND AFTER] Processing complete!
// ✅ [GLOBAL AFTER] Cleaning up...
//    - Closing connections
//    - Saving state
