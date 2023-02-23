import logging
from command.basic_command import ChaosBladeCommand
from utils.k8s import get_pod_names, get_one_container_id_with_host_ip


class PodCpuFull(ChaosBladeCommand):

    def __init__(self, ip, pod_prefix, duration, interval, namespace):

        super(PodCpuFull, self).__init__(duration, interval)
        self.fault_type = 'pod-cpu-full'
        self.ip = ip
        self.pod_prefix = pod_prefix
        self.namespace = namespace

    def __str__(self):
        return f'[pod-cpu-full] ip: {self.ip} pod_prefix: {self.pod_prefix} namespace: {self.namespace}'

    def init(self):
        pods = get_pod_names(self.namespace, self.pod_prefix)
        if len(pods) == 0:
            logging.error(f'Cannot find pod which name start with {self.pod_prefix}')
            raise Exception(f'Cannot find pod which name start with {self.pod_prefix}')
        pod = pods[0]  # Only select the first pod.
        self.cmd = f'create k8s pod-cpu fullload ' \
                   f'--namespace {self.namespace} ' \
                   f'--names {pod} ' \
                   f'--kubeconfig ~/.kube/config'
        self.root_cause = pod


class PodMysqlDelay(ChaosBladeCommand):

    def __init__(self, pod_prefix, time, duration, interval, namespace):

        super(PodMysqlDelay, self).__init__(duration, interval)
        self.fault_type = 'pod-mysql-delay'
        self.pod_prefix = pod_prefix
        self.time = time
        self.namespace = namespace

    def __str__(self):
        return f'[pod-mysql-delay] pod_prefix: {self.pod_prefix} namespace: {self.namespace} time: {self.time}'

    def init(self):
        pod_name, container_id, host_ip = get_one_container_id_with_host_ip(self.namespace, self.pod_prefix)
        if not container_id:
            logging.error(f'Cannot find pod which name start with {self.pod_prefix}')
            raise Exception(f'Cannot find pod which name start with {self.pod_prefix}')

        self.ip = host_ip
        self.cmd = f'create cri mysql delay ' \
                   f'--container-id {container_id} ' \
                   f'--time {self.time} ' \
                   f'--pid 1 ' \
                   f'--chaosblade-release ~/chaosblade/chaosblade-1.5.0-linux-amd64.tar.gz'
        self.root_cause = ' '.join([pod_name, 'mysql-all'])


class PodTypedMysqlDelay(ChaosBladeCommand):

    def __init__(self, pod_prefix, sqltype, time, duration, interval, namespace):

        super(PodTypedMysqlDelay, self).__init__(duration, interval)
        self.fault_type = 'pod-typed-mysql-delay'
        self.pod_prefix = pod_prefix
        self.sqltype = sqltype
        self.time = time
        self.namespace = namespace

    def __str__(self):
        return f'[pod-typed-mysql-delay] pod_prefix: {self.pod_prefix} sqltype: {self.sqltype} namespace: {self.namespace} time: {self.time}'

    def init(self):
        pod_name, container_id, host_ip = get_one_container_id_with_host_ip(self.namespace, self.pod_prefix)
        if not container_id:
            logging.error(f'Cannot find pod which name start with {self.pod_prefix}')
            raise Exception(f'Cannot find pod which name start with {self.pod_prefix}')

        self.ip = host_ip
        self.cmd = f'create cri mysql delay ' \
                   f'--container-id {container_id} ' \
                   f'--sqltype {self.sqltype} ' \
                   f'--time {self.time} ' \
                   f'--pid 1 ' \
                   f'--chaosblade-release ~/chaosblade/chaosblade-1.5.0-linux-amd64.tar.gz'
        self.root_cause = ' '.join([pod_name, f'mysql-{self.sqltype}'])


class PodRabbitmqDelay(ChaosBladeCommand):

    def __init__(self, pod_prefix, time, duration, interval, namespace):

        super(PodRabbitmqDelay, self).__init__(duration, interval)
        self.fault_type = 'pod-rabbitmq-delay'
        self.pod_prefix = pod_prefix
        self.time = time
        self.namespace = namespace

    def __str__(self):
        return f'[pod-rabbitmq-delay] pod_prefix: {self.pod_prefix} namespace: {self.namespace} time: {self.time}'

    def init(self):
        pod_name, container_id, host_ip = get_one_container_id_with_host_ip(self.namespace, self.pod_prefix)
        if not container_id:
            logging.error(f'Cannot find pod which name start with {self.pod_prefix}')
            raise Exception(f'Cannot find pod which name start with {self.pod_prefix}')

        self.ip = host_ip
        self.cmd = f'create cri rabbitmq delay --producer ' \
                   f'--container-id {container_id} ' \
                   f'--time {self.time} ' \
                   f'--pid 1 ' \
                   f'--chaosblade-release ~/chaosblade/chaosblade-1.5.0-linux-amd64.tar.gz'
        self.root_cause = ' '.join([pod_name, 'rabbitmq-producer'])
