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
		Usage:   "A simple CLI application",
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

			// Your application logic here
			fmt.Println("Hello, World!")

			return nil
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
