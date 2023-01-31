from command.basic_command import ChaosBladeCommand
from utils.k8s import get_one_src_name_dest_ip


class PodPodNetworkDelay(ChaosBladeCommand):
    def __init__(self, ip, src, dest, interface, time, duration, interval, namespace):
        """Chaosblade k8s pod-network delay

        For example:
            create k8s pod-network delay
            --namespace default
            --names ts-admin-travel-service-d5c4d76b4-ffr8x
            --interface eth0
            --destination-ip 10.244.195.203
            --time 500
            --kubeconfig ~/.kube/config

        :param ip: blade server ip (port: 9526). e.g., 10.176.122.154
        :param src: src service name used to obtain pod name. e.g., ts-seat-service
        :param dest: dest service name used to obatin pod ip. e.g., ts-order-service
        :param interface: network interface. e.g., eth0
        :param time: delay time (ms). e.g., 500
        :param duration: duration of the fault injection (s). e.g., 300
        :param interval: interval between current and next fault injections (s). e.g., 300
        :param namespace: k8s deployment namespace. e.g., default
        """
        super(PodPodNetworkDelay, self).__init__(duration, interval)
        self.fault_type = 'pod-pod-network-delay'
        self.ip = ip
        self.src = src
        self.dest = dest
        self.interface = interface
        self.time = time
        self.namespace = namespace

    def __str__(self):
        return f'[pod-pod-network-delay] ip: {self.ip} src: {self.src} dest: {self.dest} ' \
               f'interface: {self.interface} time: {self.time} namespace: {self.namespace}'

    def init(self):
        src_pod_name, dest_pod_name, dest_pod_ip = get_one_src_name_dest_ip(self.namespace, self.src, self.dest)
        self.cmd = f'create k8s pod-network delay ' \
                   f'--namespace {self.namespace} ' \
                   f'--names {src_pod_name} ' \
                   f'--interface {self.interface} ' \
                   f'--destination-ip {dest_pod_ip} ' \
                   f'--time {self.time} ' \
                   f'--kubeconfig ~/.kube/config'
        self.root_cause = ' '.join(src_pod_name, dest_pod_name)


class PodPodNetworkDrop(ChaosBladeCommand):

    def __init__(self, ip, src, dest, interface, duration, interval, namespace):
        """Chaosblade k8s container-network drop

        For example:
            create k8s container-network drop
            --namespace default
            --names ts-preserve-service-56548b8fd4-qh5ns
            --container-names ts-preserve-service
            --destination-ip 10.244.169.129
            --network-traffic out
            --use-sidecar-container-network
            --kubeconfig ~/.kube/config

        :param ip: blade server ip (port: 9526). e.g., 10.176.122.154
        :param src: src service name used to obtain pod name. e.g., ts-seat-service
        :param dest: dest service name used to obatin pod ip. e.g., ts-order-service
        :param interface: network interface. e.g., eth0
        :param duration: duration of the fault injection (s). e.g., 300
        :param interval: interval between current and next fault injections (s). e.g., 300
        :param namespace: k8s deployment namespace. e.g., default
        """
        super(PodPodNetworkDrop, self).__init__(duration, interval)
        self.fault_type = 'pod-pod-network-drop'
        self.ip = ip
        self.src = src
        self.dest = dest
        self.interface = interface
        self.namespace = namespace

    def __str__(self):
        return f'[pod-pod-network-drop] ip: {self.ip} src: {self.src} dest: {self.dest} ' \
               f'interface: {self.interface} namespace: {self.namespace}'

    def init(self):
        src_pod_name, dest_pod_name, dest_pod_ip = get_one_src_name_dest_ip(self.namespace, self.src, self.dest)
        self.cmd = f'create k8s container-network drop ' \
                   f'--namespace {self.namespace} ' \
                   f'--names {src_pod_name} ' \
                   f'--container-names {self.src} ' \
                   f'--destination-ip {dest_pod_ip} ' \
                   f'--network-traffic out ' \
                   f'--use-sidecar-container-network ' \
                   f'--kubeconfig ~/.kube/config'
        self.root_cause = ' '.join(src_pod_name, dest_pod_name)
