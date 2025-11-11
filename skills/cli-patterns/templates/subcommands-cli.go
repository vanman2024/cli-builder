package main

import (
	"fmt"
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

func main() {
	app := &cli.App{
		Name:    "myapp",
		Usage:   "A CLI tool with subcommands",
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
						EnvVars: []string{"PORT"},
					},
					&cli.StringFlag{
						Name:    "host",
						Value:   "localhost",
						Usage:   "Host to bind to",
						EnvVars: []string{"HOST"},
					},
				},
				Action: func(c *cli.Context) error {
					port := c.Int("port")
					host := c.String("host")
					fmt.Printf("Starting service on %s:%d\n", host, port)
					return nil
				},
			},
			{
				Name:  "stop",
				Usage: "Stop the service",
				Action: func(c *cli.Context) error {
					fmt.Println("Stopping service...")
					return nil
				},
			},
			{
				Name:  "restart",
				Usage: "Restart the service",
				Action: func(c *cli.Context) error {
					fmt.Println("Restarting service...")
					return nil
				},
			},
			{
				Name:  "status",
				Usage: "Check service status",
				Action: func(c *cli.Context) error {
					fmt.Println("Service is running")
					return nil
				},
			},
			{
				Name:  "config",
				Usage: "Configuration management",
				Subcommands: []*cli.Command{
					{
						Name:  "show",
						Usage: "Show current configuration",
						Action: func(c *cli.Context) error {
							fmt.Println("Current configuration:")
							fmt.Println("  port: 8080")
							fmt.Println("  host: localhost")
							return nil
						},
					},
					{
						Name:      "set",
						Usage:     "Set configuration value",
						ArgsUsage: "<key> <value>",
						Action: func(c *cli.Context) error {
							if c.NArg() < 2 {
								return fmt.Errorf("usage: config set <key> <value>")
							}
							key := c.Args().Get(0)
							value := c.Args().Get(1)
							fmt.Printf("Setting %s = %s\n", key, value)
							return nil
						},
					},
					{
						Name:      "get",
						Usage:     "Get configuration value",
						ArgsUsage: "<key>",
						Action: func(c *cli.Context) error {
							if c.NArg() < 1 {
								return fmt.Errorf("usage: config get <key>")
							}
							key := c.Args().Get(0)
							fmt.Printf("%s = <value>\n", key)
							return nil
						},
					},
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
