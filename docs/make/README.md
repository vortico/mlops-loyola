# Make and Automation

## What is Make?

[Make](https://www.gnu.org/software/make/) is a build automation tool that automatically builds executable programs and libraries from source code by reading files called Makefiles. While it was originally created for compiling programs, it's now widely used as a general-purpose automation tool in software development.

## Why Use Make?

Make offers several advantages for project automation:
1. **Standardization**: Common commands are documented and standardized
2. **Simplicity**: Complex operations are reduced to simple commands
3. **Documentation**: Self-documenting through help commands
4. **Dependency Management**: Can handle task dependencies efficiently

## Our Makefile Commands

Our project uses Make to simplify common development tasks. Here are the available commands:

### Code Quality Commands
- `make black` - Format code using black
- `make isort` - Sort Python imports
- `make pyright` - Run static type checking
- `make ruff` - Run the ruff linter
- `make lint` - Run all linting tools
- `make lint-fix` - Auto-fix linting issues where possible

### Installation Commands
- `make install` - Install main project dependencies
- `make install-dev` - Install development dependencies

### Testing Commands
- `make test` - Run the test suite

### Deployment Commands
- `make serve-model` - Serve the ML model with a web interface

## How to Use Make

1. **View Available Commands**
   ```bash
   make help
   ```
   This will show all available commands with their descriptions.

2. **Run a Command**
   ```bash
   make <command-name>
   ```
   For example: `make lint` to run all linters

## Behind the Scenes

Our Makefile uses several key features:

- **@** prefix: Suppresses command echo in the terminal
- **Scripts Directory**: Commands are implemented in separate scripts for maintainability
- **Help System**: Auto-generates help text from command comments
- **PHONY Targets**: Declares targets that don't create files

## Best Practices

When working on this project:
1. Always run `make lint` before committing code
2. Use `make lint-fix` to automatically fix common issues
3. Ensure tests pass with `make test` before pushing changes
4. Install dependencies using the appropriate make command

This automation helps maintain consistency across the development team and simplifies common tasks into memorable commands.
