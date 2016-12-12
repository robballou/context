import subprocess
import re
import sys
from argparse import Namespace
from context.plugins import Plugin

class DockerSwitch(Plugin):
    """
    Plugin to catch if a VM is running before switching contexts.

    CONFIGURATION

    The contexts need to have a "vm" key in the configuration file. This should be the
    name for vm as returned by VBoxManage. Also add "context.plugins.contrib.docker_switch" to
    your "__plugins" list in your config file.

    Observers: switch.pre
    """
    def __init__(self, context_object):
        super(DockerSwitch, self).__init__(context_object)
        context_object.subscribe('switch.pre', self.switch)
        context_object.subscribe('switch', self.post_switch)
        self.context = context_object

    def answer_is_affirmative(self, answer):
        """Check if the user input is affirmative"""
        return answer.strip() in ['y', 'yes', 'Y', '1', '']

    def are_containers_running(self, context):
        """Check if there are containers for this context running"""
        # we don't care if they are running when running drocker, it will
        # handle it for us...
        if 'containers' not in context and context['docker'] == 'drocker':
            return True

        if 'containers' in context:
            running_containers = self.get_running_containers()
            for container in context['containers']:
                if container in running_containers:
                    return True

        return False

    def get_running_containers(self, context=None):
        """Get a list of running containers"""
        output = subprocess.check_output("docker ps", shell=True)
        reg = re.compile(b'^.+\s(\S+)$')
        containers = []
        first_line = True
        for line in output.splitlines():
            if first_line:
                first_line = False
                continue
            match = reg.match(line)
            if match:
                containers.append(match.group(1))
        return [container.decode('utf-8') for container in containers]

    def switch(self, event):
        """
        Catch when a user is switching contexts and see if the VM for that
        context is running
        """
        # if the context is being switched to the current context, skip
        if event.attributes['command_args'].subcommand and event.attributes['command_args'].subcommand[0] == event.context.current_context:
            return

        # try to see if the VM is running and turn it off
        try:
            if event.attributes['current_context'] and self.are_containers_running(event.attributes['current_context']):
                sys.stderr.write("The containers for the context %s are running. Do you want to halt it? [Y/n] " % event.context.current_context)
                sys.stderr.flush()
                answer = sys.stdin.readline()
                if self.answer_is_affirmative(answer):
                    self.message("Halting containers")
                    event.context.run_command('docker', Namespace(subcommand=['down']))
        except KeyError:
            pass

    def post_switch(self, event):
        """
        Catch when a user has switched contexts and see if the VM for the new
        context is running
        """
        # check vbox manage
        running_containers = self.get_running_containers(event.attributes['current_context'])

        # try to see if the new VM is running and turn it on
        try:
            if event.attributes['current_context'] and 'docker' in event.attributes['current_context']:
                if not self.are_containers_running(event.attributes['current_context']):
                    sys.stderr.write("The containers for the context %s are not running. Do you want to start it? [Y/n] " % event.context.current_context)
                    sys.stderr.flush()
                    answer = sys.stdin.readline()
                    if self.answer_is_affirmative(answer):
                        self.message("Starting containers")
                        event.context.run_command('docker', Namespace(subcommand=['up', '-d']))
        except KeyError:
            pass
