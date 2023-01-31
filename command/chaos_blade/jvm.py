import logging
from command.basic_command import ChaosBladeCommand
from utils.k8s import get_one_container_id_with_host_ip


class JvmCpuFull(ChaosBladeCommand):

    def __init__(self, pod_prefix, duration, interval, namespace):

        super(JvmCpuFull, self).__init__(duration, interval)
        self.fault_type = 'jvm-cpu-full'
        self.pod_prefix = pod_prefix
        self.namespace = namespace

    def __str__(self):
        return f'[jvm-cpu-full] pod_prefix: {self.pod_prefix} namespace: {self.namespace}'

    def init(self):
        pod_name, container_id, host_ip = get_one_container_id_with_host_ip(self.namespace, self.pod_prefix)
        if not container_id:
            logging.error(f'Cannot find pod which name start with {self.pod_prefix}')
            raise Exception(f'Cannot find pod which name start with {self.pod_prefix}')

        self.ip = host_ip
        self.cmd = f'create cri jvm cpufullload ' \
                   f'--container-id {container_id} ' \
                   f'--pid 1 ' \
                   f'--chaosblade-release ~/chaosblade/chaosblade-1.5.0-linux-amd64.tar.gz'
        self.root_cause = pod_name
