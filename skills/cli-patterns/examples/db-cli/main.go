package main

import (
	"fmt"
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

func main() {
	app := &cli.App{
		Name:  "dbctl",
		Usage: "Database management CLI tool",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:     "connection",
				Aliases:  []string{"conn"},
				Usage:    "Database connection string",
				EnvVars:  []string{"DATABASE_URL"},
				Required: true,
			},
			&cli.BoolFlag{
				Name:    "verbose",
				Aliases: []string{"v"},
				Usage:   "Enable verbose output",
			},
		},

		Before: func(c *cli.Context) error {
			conn := c.String("connection")
			verbose := c.Bool("verbose")

			if verbose {
				fmt.Println("🔗 Validating database connection...")
			}

			// Validate connection string
			if conn == "" {
				return fmt.Errorf("database connection string required")
			}

			if verbose {
				fmt.Println("✅ Connection string validated")
			}

			return nil
		},

		After: func(c *cli.Context) error {
			if c.Bool("verbose") {
				fmt.Println("🔚 Closing database connections...")
			}
			return nil
		},

		Commands: []*cli.Command{
			// Schema category
			{
				Name:     "migrate",
				Category: "Schema",
				Usage:    "Run database migrations",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:    "direction",
						Aliases: []string{"d"},
						Usage:   "Migration direction (up/down)",
						Value:   "up",
					},
					&cli.IntFlag{
						Name:  "steps",
						Usage: "Number of steps to migrate",
						Value: 0,
					},
				},
				Action: func(c *cli.Context) error {
					direction := c.String("direction")
					steps := c.Int("steps")

					fmt.Printf("Running migrations %s", direction)
					if steps > 0 {
						fmt.Printf(" (%d steps)", steps)
					}
					fmt.Println()

					return nil
				},
			},
			{
				Name:     "rollback",
				Category: "Schema",
				Usage:    "Rollback last migration",
				Action: func(c *cli.Context) error {
					fmt.Println("Rolling back last migration...")
					return nil
				},
			},

			// Data category
			{
				Name:     "seed",
				Category: "Data",
				Usage:    "Seed database with test data",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:    "file",
						Aliases: []string{"f"},
						Usage:   "Seed file path",
						Value:   "seeds/default.sql",
					},
				},
				Action: func(c *cli.Context) error {
					file := c.String("file")
					fmt.Printf("Seeding database from: %s\n", file)
					return nil
				},
			},
			{
				Name:     "backup",
				Category: "Data",
				Usage:    "Backup database",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "output",
						Aliases:  []string{"o"},
						Usage:    "Backup output path",
						Required: true,
					},
				},
				Action: func(c *cli.Context) error {
					output := c.String("output")
					fmt.Printf("Backing up database to: %s\n", output)
					return nil
				},
			},
			{
				Name:     "restore",
				Category: "Data",
				Usage:    "Restore database from backup",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "input",
						Aliases:  []string{"i"},
						Usage:    "Backup file path",
						Required: true,
					},
				},
				Action: func(c *cli.Context) error {
					input := c.String("input")
					fmt.Printf("Restoring database from: %s\n", input)
					return nil
				},
			},

			// Admin category
			{
				Name:     "status",
				Category: "Admin",
				Usage:    "Check database status",
				Action: func(c *cli.Context) error {
					fmt.Println("Database Status:")
					fmt.Println("  Connection: Active")
					fmt.Println("  Tables: 15")
					fmt.Println("  Size: 245 MB")
					return nil
				},
			},
			{
				Name:     "vacuum",
				Category: "Admin",
				Usage:    "Optimize database",
				Action: func(c *cli.Context) error {
					fmt.Println("Optimizing database...")
					return nil
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
