import logging
from command.basic_command import ChaosBladeCommand
from utils.k8s import get_pod_names


class SvcCpuFull(ChaosBladeCommand):

    def __init__(self, ip, pod_prefix, duration, interval, namespace):

        super(SvcCpuFull, self).__init__(duration, interval)
        self.ip = ip
        self.pod_prefix = pod_prefix
        self.namespace = namespace

    def __str__(self):
        return f'[svc-cpu-full] ip: {self.ip} pod_prefix: {self.pod_prefix} namespace: {self.namespace}'

    def init(self):
        pods = get_pod_names(self.namespace, self.pod_prefix)
        if len(pods) == 0:
            logging.error(f'Cannot find pod which name start with {self.pod_prefix}')
            raise Exception(f'Cannot find pod which name start with {self.pod_prefix}')
        pods = ','.join(pods)
        self.cmd = f'create k8s pod-cpu fullload ' \
                   f'--namespace {self.namespace} ' \
                   f'--names {pods} ' \
                   f'--kubeconfig ~/.kube/config'
