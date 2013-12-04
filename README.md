# Context Switcher

Switch project contexts easily, from anywhere. Example usage:

    $ context current
    None
    $ context switch my_project
    $ context current
    my_project

    # change to git directory
    $ context git

    # change to vagrant directory
    $ context vagrant

    # start vagrant
    $ context vagrant start

    # stop vagrant
    $ context vagrant stop

    # remove the "current" context
    $ context clear

## Install

Clone this repo where you store your git files:

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

## Configuration options

* git
* web
* www
* vagrant

## Commands

### Git

Defaults to changing to the git directory.

You can also now pass arguments to git that will run in that folder. For example, `context git merge dev` will run:

    pushd [git directory] && git merge dev && popd

### Vagrant

Defaults to changing to the vagrant directory.

#### Subcommands

* `down` or `halt` (turn off vagrant)
* `up` (turn on vagrant)
* `ssh` (ssh into vagrant)

### Web

Goes to the defined `web` folder.

### Www

Goes to the defined website in your browser.