from typing import Dict
from .basic_command import BasicCommand
from .command_register import command_register


class CommandBuilder(object):

    @staticmethod
    def build(fault_info: Dict, target: str) -> BasicCommand:
        command_name = fault_info['fault_name']
        command = command_register[command_name]
        namespace = fault_info['namespace']
        duration = fault_info['duration']
        interval = fault_info['interval']
        time = fault_info['time'] if 'time' in fault_info else None
        interface = fault_info['interface'] if 'interface' in fault_info else None

        if command_name.startswith('api'):
            service, classname, methodname = target.strip().split()
            return

        if command_name.startswith(['pod-http', 'svc-http']):
            app, port = target.strip().split()
            return

        if command_name.startswith(['pod-pod-network', 'svc-svc-network']):
            src, dest = target.strip().split()
            return
