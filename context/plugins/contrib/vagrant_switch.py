import subprocess
import re
import sys
from argparse import Namespace
from context.plugins import Plugin

class VagrantSwitch(Plugin):
    """
    Plugin to catch if a VM is running before switching contexts.

    CONFIGURATION

    The contexts need to have a "vm" key in the configuration file. This should be the
    name for vm as returned by VBoxManage. Also add "context.plugins.contrib.vagrant_switch" to
    your "__plugins" list in your config file.

    Observers: switch.pre
    """
    def __init__(self, context_object):
        super(VagrantSwitch, self).__init__(context_object)
        context_object.subscribe('switch.pre', self.switch)
        context_object.subscribe('switch', self.post_switch)
        self.context = context_object

    def answer_is_affirmative(self, answer):
        """Check if the user input is affirmative"""
        return answer.strip() in ['y', 'yes', 'Y', '1', '']

    def get_running_vms(self):
        """Get a list of running VMs"""
        output = subprocess.check_output("VBoxManage list runningvms", shell=True)
        reg = re.compile(b'"(?P<vm>[^"]+)"')
        vms = []
        for line in output.splitlines():
            match = reg.match(line)
            if match:
                vms.append(match.group('vm'))
        return [vm.decode('utf-8') for vm in vms]

    def switch(self, event):
        """
        Catch when a user is switching contexts and see if the VM for that
        context is running
        """

        # check vbox manage
        running_vms = self.get_running_vms()
        if not running_vms:
            return

        # if the context is being switched to the current context, skip
        if event.attributes['command_args'].subcommand and event.attributes['command_args'].subcommand[0] == event.context.current_context:
            return

        # try to see if the VM is running and turn it off
        try:
            if event.attributes['current_context'] and event.attributes['current_context']['vm'] in running_vms:
                sys.stderr.write("The VM for the context %s is running. Do you want to halt it? [Y/n] " % event.context.current_context)
                sys.stderr.flush()
                answer = sys.stdin.readline()
                if self.answer_is_affirmative(answer):
                    self.message("Halting VM")
                    event.context.run_command('vagrant', Namespace(subcommand=["down"]))
        except KeyError:
            pass

    def post_switch(self, event):
        """
        Catch when a user has switched contexts and see if the VM for the new
        context is running
        """

        # check vbox manage
        running_vms = self.get_running_vms()

        # try to see if the new VM is running and turn it on
        try:
            if event.attributes['current_context'] and event.attributes['current_context']['vm'] not in running_vms:
                sys.stderr.write("The VM for the context %s is not running. Do you want to start it? [Y/n] " % event.context.current_context)
                sys.stderr.flush()
                answer = sys.stdin.readline()
                if self.answer_is_affirmative(answer):
                    self.message("Starting VM")
                    event.context.run_command('vagrant', Namespace(subcommand=["up"]))
        except KeyError:
            pass
