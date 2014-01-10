import subprocess
import re
import sys
from argparse import Namespace
from context.plugins import Plugin

class VagrantSwitch(Plugin):
    def __init__(self, context_object):
        super(VagrantSwitch, self).__init__(context_object)
        context_object.subscribe('switch.pre', self.switch)

    def get_running_vms(self):
        output = subprocess.check_output("VBoxManage list runningvms", shell=True)
        reg = re.compile(r'"(?P<vm>[^"]+)"')
        vms = []
        for line in output.splitlines():
            match = reg.match(line)
            if match:
                vms.append(match.group('vm'))
        return vms

    # def pre_switch(self, event):
    #     self.pre_context_name = event.context.current_context
    #     self.pre_context_settings = None
    #     if self.pre_context_name:
    #         self.pre_context_settings = event.context.get(event.context.current_context)

    def switch(self, event):
        # check vbox manage
        # VBoxManage list runningvms
        running_vms = self.get_running_vms()

        # if the context is being switched to the current context, skip
        if event.attributes['command_args'].subcommand and event.attributes['command_args'].subcommand[0] == event.context.current_context:
            return

        # try to see if the VM is running and turn it off
        try:
            if event.attributes['current_context']['vm'] in running_vms:
                sys.stderr.write("The VM for the context %s is running. Do you want to halt it? [Y/n] " % event.context.current_context)
                answer = sys.stdin.readline()
                answer = answer.strip()
                # answer = raw_input("The VM for the context %s is running. Do you want to halt it? [Y/n]" % event.context.current_context)
                if answer in ['y', 'yes', 'Y', '1', '']:
                    self.message("Halting VM")
                    event.context.run_command('vagrant', Namespace(subcommand=["down"]))
        except KeyError:
            pass
