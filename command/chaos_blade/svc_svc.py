from command.basic_command import ChaosBladeCommand
from utils.k8s import get_all_src_names_dest_ips


class SvcSvcNetworkDelay(ChaosBladeCommand):
    def __init__(self, ip, src, dest, interface, time, duration, interval, namespace):
        """Chaosblade k8s pod-network delay

        For example:
            create k8s pod-network delay
            --namespace default
            --names ts-admin-route-service-77cd6cf987-c4nm7,ts-admin-route-service-77cd6cf987-jr88g
            --interface eth0
            --destination-ip 10.244.107.213,10.244.107.232
            --time 500
            --kubeconfig ~/.kube/config

        :param ip: blade server ip (port: 9526). e.g., 10.176.122.154
        :param src: src service name used to obtain pod names. e.g., ts-admin-route-service
        :param dest: dest service name used to obatin pod ips. e.g., ts-station-service
        :param interface: network interface. e.g., eth0
        :param time: delay time (ms). e.g., 500
        :param duration: duration of the fault injection (s). e.g., 300
        :param interval: interval between current and next fault injections (s). e.g., 300
        :param namespace: k8s deployment namespace. e.g., default
        """
        super(SvcSvcNetworkDelay, self).__init__(duration, interval)
        self.ip = ip
        self.src = src
        self.dest = dest
        self.interface = interface
        self.time = time
        self.namespace = namespace

    def __str__(self):
        return f'[svc-svc-network-delay] ip: {self.ip} src: {self.src} dest: {self.dest} ' \
               f'interface: {self.interface} time: {self.time} namespace: {self.namespace}'

    def init(self):
        src_pod_names, dest_pod_ips = get_all_src_names_dest_ips(self.namespace, self.src, self.dest)
        self.cmd = f"create k8s pod-network delay " \
                   f"--namespace {self.namespace} " \
                   f"--names {','.join(src_pod_names)} " \
                   f"--interface {self.interface} " \
                   f"--destination-ip {','.join(dest_pod_ips)} " \
                   f"--time {self.time} " \
                   f"--kubeconfig ~/.kube/config"


class SvcSvcNetworkDrop(ChaosBladeCommand):

    def __init__(self, ip, src, dest, interface, duration, interval, namespace):
        """Chaosblade k8s container-network drop

        For example:
            create k8s container-network drop
            --namespace default
            --names ts-travel2-service-686c895647-s2jcx,ts-travel2-service-686c895647-tgd5d
            --container-names ts-travel2-service
            --destination-ip 10.244.169.152,10.244.195.193
            --network-traffic out
            --use-sidecar-container-network
            --kubeconfig ~/.kube/config

        :param ip: blade server ip (port: 9526). e.g., 10.176.122.154
        :param src: src service name used to obtain pod names. e.g., ts-travel2-service
        :param dest: dest service name used to obatin pod ips. e.g., ts-basic-service
        :param interface: network interface. e.g., eth0
        :param duration: duration of the fault injection (s). e.g., 300
        :param interval: interval between current and next fault injections (s). e.g., 300
        :param namespace: k8s deployment namespace. e.g., default
        """
        super(SvcSvcNetworkDrop, self).__init__(duration, interval)
        self.ip = ip
        self.src = src
        self.dest = dest
        self.interface = interface
        self.namespace = namespace

    def __str__(self):
        return f'[svc-svc-network-drop] ip: {self.ip} src: {self.src} dest: {self.dest} ' \
               f'interface: {self.interface} namespace: {self.namespace}'

    def init(self):
        src_pod_names, dest_pod_ips = get_all_src_names_dest_ips(self.namespace, self.src, self.dest)
        self.cmd = f"create k8s container-network drop " \
                   f"--namespace {self.namespace} " \
                   f"--names {','.join(src_pod_names)} " \
                   f"--container-names {self.src} " \
                   f"--destination-ip {','.join(dest_pod_ips)} " \
                   f"--network-traffic out " \
                   f"--use-sidecar-container-network " \
                   f"--kubeconfig ~/.kube/config"
