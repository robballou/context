# Context Switcher

Switch project contexts easily, from anywhere. Example usage:

```bash
# check the current context
context current
None

# switch contexts
context switch my_project
context current
my_project

# change to git directory
context git

# launch the web folder in your editor
context web edit

# launch the web folder in Finder
context web finder

# change to vagrant directory
context vagrant

# start vagrant
context vagrant start

# stop vagrant
context vagrant stop

# remove the "current" context
context clear
```

Basically this is a command line tool that allows you to use the same commands in different folders or on different assets. It doesn't require you to be in a specific location to run commands that may require you be setup in a specific location (like vagrant, compass, etc.). Switching contexts lets you change to a different set of definitions.

For the time being, the code here will be in transition as I use the module and find better ways of doing things!

## Install

This library requires Python 2.7. Clone this repo where you store your git files:

    cd ~/git
    git clone [path]

Add this alias to your aliases and source the aliases file (tip: change the alias to something useful for you, examples: `c`, `ctxt`, etc):

    alias context=". [path]/context.sh"

Create a JSON document with your configuration:

    echo '{}' > ~/.contexts

Configure some contexts:

```json
{
    "my_project": {
        "git": "~/git/my_project",
        "vagrant": "~/git/my_project/vagrant"
    }
}
```

## Context Configuration options

* git: string
* links: dict
* theme: string
* web: string
* www: string
* vagrant: string

## Loading Custom Commands

You can add custom commands with a `__commands` entry:

```json
{
    "__commands": [
        "example_module.example_command"
    ],
    "my_project": {
        "git": "~/git/my_project",
        "vagrant": "~/git/my_project/vagrant"
    }
}
```

The example above will add the example command to the list of available context commands. Command classes should inherit the `Command` class (or a derivative when they exist). The `Command` class has two main methods:

1. **`run`:** This method is called for any subcommand. You can add this to handle specific subcommands or to even handle the default.
2. **`default`:** Useful when your command does not have any subcommands, the default command is called when no subcommands are issued.

A very simple example:

```python
from context.commands import Command

class Current(Command):
    """Display the current context"""
    def default(self, context, args, contexts):
        self.error_message(contexts.current_context)
```

To execute commands on the shell, print them out to the `stdout`. If you want to print informational data, print that out to `stderr` (`self.error_message` above is just a method that writes to `stderr` for you).

## Context variables

You can use variables within context definitions. The variables take a PHP-style approach:

```json
{
    "my_project": {
        "git": "~/git/my_project",
        "vagrant": "$git/vagrant"
    }
}
```

The `my_project.vagrant` setting will become: `~/git/my_project/vagrant`

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

### Django

Passes commands to the Django manage.py in the `web` folder of your context.

### Edit

Opens the contexts file in the `$EDITOR`.

### Git

**Alias:** g

Defaults to changing to the git directory.

You can also now pass arguments to git that will run in that folder. For example, `context git merge dev` will run:

```bash
pushd [git directory]; git merge dev; popd
```

#### Subcommands

* `edit` (launch the git folder in your `$EDITOR`)
* `finder` (launch the git folder in Finder)

### Links

**Alias:** l

Allows you to save links and open them: `context links link_name`

A better example, if you have this in your context configuration:

```json
"links": {
    "dev": "http://dev.example.com",
    "theme": "file:///Users/example/git/project/themefolder"
}
```

You can run: `context links dev` to open that link. This command uses `open` to handle opening the links. So if `open` knows how to handle a link, it will do that for you. For example, web links will open in a browser, folders in Finder, etc.

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
* `finder` (launch the web folder in Finder)
* `theme` (goto the theme folder)
* `theme finder` (goto the theme folder in Finder)

### Www

Goes to the defined website in your browser.
