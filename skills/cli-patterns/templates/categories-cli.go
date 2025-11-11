package main

import (
	"fmt"
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

func main() {
	app := &cli.App{
		Name:  "myapp",
		Usage: "CLI tool with categorized commands",
		Commands: []*cli.Command{
			// Database category
			{
				Name:     "create-db",
				Category: "Database",
				Usage:    "Create a new database",
				Action: func(c *cli.Context) error {
					fmt.Println("Creating database...")
					return nil
				},
			},
			{
				Name:     "migrate",
				Category: "Database",
				Usage:    "Run database migrations",
				Action: func(c *cli.Context) error {
					fmt.Println("Running migrations...")
					return nil
				},
			},
			{
				Name:     "seed",
				Category: "Database",
				Usage:    "Seed database with test data",
				Action: func(c *cli.Context) error {
					fmt.Println("Seeding database...")
					return nil
				},
			},

			// Deploy category
			{
				Name:     "deploy",
				Category: "Deploy",
				Usage:    "Deploy application",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "env",
						Aliases:  []string{"e"},
						Usage:    "Target environment",
						Required: true,
					},
				},
				Action: func(c *cli.Context) error {
					env := c.String("env")
					fmt.Printf("Deploying to %s...\n", env)
					return nil
				},
			},
			{
				Name:     "rollback",
				Category: "Deploy",
				Usage:    "Rollback deployment",
				Action: func(c *cli.Context) error {
					fmt.Println("Rolling back...")
					return nil
				},
			},

			// Monitor category
			{
				Name:     "logs",
				Category: "Monitor",
				Usage:    "View application logs",
				Flags: []cli.Flag{
					&cli.BoolFlag{
						Name:    "follow",
						Aliases: []string{"f"},
						Usage:   "Follow log output",
					},
				},
				Action: func(c *cli.Context) error {
					follow := c.Bool("follow")
					fmt.Println("Fetching logs...")
					if follow {
						fmt.Println("Following logs (Ctrl+C to stop)...")
					}
					return nil
				},
			},
			{
				Name:     "status",
				Category: "Monitor",
				Usage:    "Check application status",
				Action: func(c *cli.Context) error {
					fmt.Println("Status: Running")
					return nil
				},
			},
			{
				Name:     "metrics",
				Category: "Monitor",
				Usage:    "View application metrics",
				Action: func(c *cli.Context) error {
					fmt.Println("Fetching metrics...")
					return nil
				},
			},

			// Config category
			{
				Name:     "show-config",
				Category: "Config",
				Usage:    "Show current configuration",
				Action: func(c *cli.Context) error {
					fmt.Println("Current configuration:")
					fmt.Println("  env: production")
					fmt.Println("  port: 8080")
					return nil
				},
			},
			{
				Name:     "set-config",
				Category: "Config",
				Usage:    "Set configuration value",
				Action: func(c *cli.Context) error {
					fmt.Println("Setting configuration...")
					return nil
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
