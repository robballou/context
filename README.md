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

For ZSH, you will also need to add the following to your `~/.zshrc`:

    # set to the install path for the context tool
    CONTEXT_HOME=[path]

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

## Plugins

The plugin interface allows you to create functionality around commands. Context ships with one plugin by
default called `vagrant_switch`. This let's you turn off/turn on vagrant VMs while you switch contexts. If
you have multiple contexts which have their own vagrant instances, this will make it easier to turn them off
and on while you switch.

To enable plugins, edit your configuration to include:

```json
{
  "__plugins": [
    "context.plugins.contrib.vagrant_switch"
  ]
}
```

Vagrant switch will prompt if you want to halt/start VMs as you switch.

### Custom plugins

You can create your own plugins:

```python
from context.plugins import Plugin

class MyPlugin(Plugin):
    def __init__(self, context_object):
        super(VagrantSwitch, self).__init__(context_object)
        context_object.subscribe('switch.pre', self.pre_switch)
        context_object.subscribe('switch', self.post_switch)
        self.context = context_object

    def pre_switch(self, event):
        self.message('pre switch')

    def post_switch(self, event):
        self.message('post switch')
```

## Commands

The following is a list of contributed commands.

Commands can have context-specific settings:

```json
{
  "my_project": {
    "git": "~/git/my_project",
    "vagrant": "$git/vagrant",
    "settings": {
      "drush": {
        "options": {
          "strict": 0
        }
      }
    }
  }
}
```

When a command is run, it will look in for settings in the current context. `options` is a special type of settings: these get converted to flags when running the command. So in the example above, the `drush` command will get a flag `--strict=0` added to the command.

### Bundler

The bundler command allows you to execute a command with Bundler within the `theme` directory for your context. Example:

    context bundler exec compass watch

### Clear

Clears the current context. Currently this actually just removes `~/.contexts_data`. This behavior will likely become smarter if new data gets stored in that file.

### Contexts

List out the available contexts. You can get the details of a specific context with:

    context contexts example

### Current

Outputs the current context. If there isn't a context selected, it will output: `None`.

### Django

**Alias:** d

Passes commands to the Django manage.py in the `web` folder of your context.

### Drush

**Alias:** dr

Passes commands to Drush in the `web` folder of your context.

The Drush command also has special handling for [Drush aliases](http://docs.drush.org/en/master/usage/). You can specify context-specific Drush aliases, including a default alias:

```json
{
  "my_project": {
    "git": "~/git/my_project",
    "vagrant": "$git/vagrant",
    "settings": {
      "drush": {
        "aliases": {
          "default": "example.dev",
          "prod": "example.prod"
        }
      }
    }
  }
}
```

The default alias will always be used unless another alias is specified, so only use it on projects where you will *always* use an alias.

    # this will run: drush @example.dev pml
    ct drush pml

    # this will run drush @example.prod pml
    ct drush:prod pml

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

* `branch` (switch branches, perform commands specified in settings)
* `edit` (launch the git folder in your `$EDITOR`)
* `finder` (launch the git folder in Finder)

The new `branch` command allows you to specify commands to run as you switch branches in git. You can set branch-specific commands and default commands that always run (the default commands run before the branch specific commands). All commands are centered on the git folder for the project. As an example, here's a configuration for a Drupal project to backup the database and load a new database while switching branches:

```json
"settings": {
  "git": {
    "branch": {
      "__defaults": {
        "precommands": [
          "drush @example.alias sql-dump --result-file=$branch.$date.sql",
        ],
        "postcommands": [
          "drush @example.alias sql-drop --yes",
          "pv $web/database.sql | drush @example.alias sqlc"
        ]
      }
    }
  }
}
```

When run with `ct git branch stage`, this will run:

* `pushd $git` (where `$git` is the configured git folder)
* `drush @example.alias sql-dump --result-file=$(git rev-parse --abbrev-ref HEAD).$(date +"%Y%m%d%H%M%S").sql` (notice that `$branch` is replaced with the current branch and `$date` with the current date)
* `git checkout stage` (default command run by the branch subcommand)
* `drush @example.alias sql-drop --yes`
* `pv $web/database.sql | drush @example.alias sqlc` (where `$web` is the configured web folder for the project)
* `popd` (leaves the $git folder)

All commands are chained together with `&&` so each much pass for the whole switch to work.

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
