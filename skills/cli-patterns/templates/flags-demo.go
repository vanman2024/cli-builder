package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/urfave/cli/v2"
)

func main() {
	app := &cli.App{
		Name:  "flags-demo",
		Usage: "Demonstration of all flag types in urfave/cli",
		Flags: []cli.Flag{
			// String flag
			&cli.StringFlag{
				Name:    "name",
				Aliases: []string{"n"},
				Value:   "World",
				Usage:   "Name to greet",
				EnvVars: []string{"GREETING_NAME"},
			},

			// Int flag
			&cli.IntFlag{
				Name:    "count",
				Aliases: []string{"c"},
				Value:   1,
				Usage:   "Number of times to repeat",
				EnvVars: []string{"REPEAT_COUNT"},
			},

			// Bool flag
			&cli.BoolFlag{
				Name:    "verbose",
				Aliases: []string{"v"},
				Usage:   "Enable verbose output",
				EnvVars: []string{"VERBOSE"},
			},

			// Int64 flag
			&cli.Int64Flag{
				Name:  "size",
				Value: 1024,
				Usage: "Size in bytes",
			},

			// Uint flag
			&cli.UintFlag{
				Name:  "port",
				Value: 8080,
				Usage: "Port number",
			},

			// Float64 flag
			&cli.Float64Flag{
				Name:  "timeout",
				Value: 30.0,
				Usage: "Timeout in seconds",
			},

			// Duration flag
			&cli.DurationFlag{
				Name:  "wait",
				Value: 10 * time.Second,
				Usage: "Wait duration",
			},

			// StringSlice flag (multiple values)
			&cli.StringSliceFlag{
				Name:    "tag",
				Aliases: []string{"t"},
				Usage:   "Tags (can be specified multiple times)",
			},

			// IntSlice flag (multiple int values)
			&cli.IntSliceFlag{
				Name:  "priority",
				Usage: "Priority values",
			},

			// Required flag
			&cli.StringFlag{
				Name:     "token",
				Usage:    "API token (required)",
				Required: true,
				EnvVars:  []string{"API_TOKEN"},
			},

			// Flag with default from env
			&cli.StringFlag{
				Name:    "env",
				Aliases: []string{"e"},
				Value:   "development",
				Usage:   "Environment name",
				EnvVars: []string{"ENV", "ENVIRONMENT"},
			},

			// Hidden flag (not shown in help)
			&cli.StringFlag{
				Name:   "secret",
				Usage:  "Secret value",
				Hidden: true,
			},
		},
		Action: func(c *cli.Context) error {
			// String flag
			name := c.String("name")
			fmt.Printf("Name: %s\n", name)

			// Int flag
			count := c.Int("count")
			fmt.Printf("Count: %d\n", count)

			// Bool flag
			verbose := c.Bool("verbose")
			if verbose {
				fmt.Println("Verbose mode: enabled")
			}

			// Int64 flag
			size := c.Int64("size")
			fmt.Printf("Size: %d bytes\n", size)

			// Uint flag
			port := c.Uint("port")
			fmt.Printf("Port: %d\n", port)

			// Float64 flag
			timeout := c.Float64("timeout")
			fmt.Printf("Timeout: %.2f seconds\n", timeout)

			// Duration flag
			wait := c.Duration("wait")
			fmt.Printf("Wait: %s\n", wait)

			// StringSlice flag
			tags := c.StringSlice("tag")
			if len(tags) > 0 {
				fmt.Printf("Tags: %v\n", tags)
			}

			// IntSlice flag
			priorities := c.IntSlice("priority")
			if len(priorities) > 0 {
				fmt.Printf("Priorities: %v\n", priorities)
			}

			// Required flag
			token := c.String("token")
			fmt.Printf("Token: %s\n", token)

			// Environment flag
			env := c.String("env")
			fmt.Printf("Environment: %s\n", env)

			// Greeting logic
			fmt.Println("\n---")
			for i := 0; i < count; i++ {
				fmt.Printf("Hello, %s!\n", name)
			}

			return nil
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
