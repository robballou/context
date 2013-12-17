# Context Switcher

Switch project contexts easily, from anywhere. Example usage:

    # check the current context
    $ context current
    None

    # switch contexts
    $ context switch my_project
    $ context current
    my_project

    # change to git directory
    $ context git

    # launch the web folder in your editor
    $ context web edit

    # change to vagrant directory
    $ context vagrant

    # start vagrant
    $ context vagrant start

    # stop vagrant
    $ context vagrant stop

    # remove the "current" context
    $ context clear

Basically this is a commandline tool that allows you to use the same commands in different folders or on different assets.

## Install

This library requires Python 2.7. Clone this repo where you store your git files:

    cd ~/git
    git clone [path]

Add this alias to your aliases and source the aliases file:

    alias context=". [path]/context.sh"

Create a JSON document with your configuration:

    echo '{}' > ~/.contexts

Configure some contexts:

    # ~/.contexts
    {
        "my_project": {
            "git": "~/git/my_project",
            "vagrant": "~/git/my_project/vagrant"
        }
    }

## Context Configuration options

* git: string
* links: dict
* theme: string
* web: string
* www: string
* vagrant: string

## Loading Custom Commands

You can add custom commands with a "__commands" entry:

    # ~/.contexts
    {
        "__commands": [
            "example_module.example_command"
        ],
        "my_project": {
            "git": "~/git/my_project",
            "vagrant": "~/git/my_project/vagrant"
        }
    }

The example above will add the example command to the list of available context commands. Command classes should inherit the `Command` class (or a derivative when they exist). The `Command` class has two main methods:

1. **`run`:** This method is called for any subcommand. You can add this to handle specific subcommands or to even handle the default.
2. **`default`:** Useful when your command does not have any subcommands, the default command is called when no subcommands are issued.

A very simple example:

    from context_commands import Command

    class Current(Command):
        """Display the current context"""
        def default(self, context, args, contexts):
            self.error_message(contexts.current_context)

## Commands

### Bundler

The bundler command allows you to execute a command with Bundler within the `theme` directory for your context. Example:

    context bundler exec compass watch

### Clear

Clears the current context. Currently this actually just removes `~/.contexts_data`. This behavior will likely become smarter if new data gets stored in that file.

### Contexts

List out the available contexts

### Current

Outputs the current context. If there isn't a context selected, it will output: `None`.

### Git

**Alias:** g

Defaults to changing to the git directory.

You can also now pass arguments to git that will run in that folder. For example, `context git merge dev` will run:

    pushd [git directory]; git merge dev; popd

#### Subcommands

* `edit` (launch the git folder in your `$EDITOR`)

### Links

**Alias:** l

Allows you to save links and open them: `context links link_name`

A better example, if you have this in your context configuration:

    "links": {
        "dev": "http://dev.example.com"
    }

You can run: `context links dev` to open that in a browser.

### Switch

Switches contexts used by this command. The command remembers this by storing this in `~/.contexts_data` as JSON data.

### Vagrant

**Alias:** v

Defaults to changing to the vagrant directory.

#### Subcommands

* `down` or `halt` (turn off vagrant)
* `up` (turn on vagrant)
* `ssh` (ssh into vagrant)

### Web

**Alias:** w

Goes to the defined `web` folder.

#### Subcommands

* `edit` (launch the web folder in your `$EDITOR`)
* `theme` (goto the theme folder)

### Www

Goes to the defined website in your browser.
