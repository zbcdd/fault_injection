from command.command_register import command_register
from command import ChaosBladeCommand
from utils.k8s import get_one_container_id_with_host_ip


@command_register('api-delay')
class ApiDelay(ChaosBladeCommand):

    def __init__(self, service, classname, methodname, time, duration, interval, namespace):
        """Chaosblade cri jvm delay

        For example:
            create cri jvm delay
            --chaosblade-release ~/chaosblade/chaosblade-1.5.0-linux-amd64.tar.gz
            --classname verifycode.controller.VerifyCodeController
            --methodname imageCode
            --container-id 3a9e08bb4c56b17190a1a8454825fabbf82a1a73b26557208d42848301c43491
            --pid 1
            --time 500

        :param service: service name used to obtain container-id. e.g., ts-verification-code-service
        :param classname: classname. e.g., verifycode.controller.VerifyCodeController
        :param methodname: methodname. e.g., imageCode
        :param time: jvm delay time (ms). e.g., 500
        :param duration: duration of the fault injection (s). e.g., 300
        :param interval: interval between current and next fault injections (s). e.g., 300
        :param namespace: k8s deployment namespace. e.g., default
        """
        super(ApiDelay, self).__init__(duration, interval)
        self.service = service
        self.classname = classname
        self.methodname = methodname
        self.time = time
        self.namespace = namespace

    def init(self):
        container_id, host_ip = get_one_container_id_with_host_ip(self.namespace, self.service)
        self.ip = host_ip
        self.cmd = f'create cri jvm delay \
                    --chaosblade-release ~/chaosblade/chaosblade-1.5.0-linux-amd64.tar.gz \
                    --classname {self.classname} \
                    --methodname {self.methodname} \
                    --container-id {container_id} \
                    --pid 1 \
                    --time {self.time}'


@command_register('api-exception')
class ApiException(ChaosBladeCommand):

    def __init__(self, service, classname, methodname, duration, interval, namespace):
        """Chaosblade cri jvm throwCustomException

        For example:
            create cri jvm throwCustomException
            --chaosblade-release ~/chaosblade/chaosblade-1.5.0-linux-amd64.tar.gz
            --classname verifycode.controller.VerifyCodeController
            --methodname imageCode
            --container-id 3a9e08bb4c56b17190a1a8454825fabbf82a1a73b26557208d42848301c43491
            --pid 1
            --exception java.lang.Exception

        :param service: service name used to obtain container-id. e.g., ts-verification-code-service
        :param classname: classname. e.g., verifycode.controller.VerifyCodeController
        :param methodname: methodname. e.g., imageCode
        :param duration: duration of the fault injection (s). e.g., 300
        :param interval: interval between current and next fault injections (s). e.g., 300
        :param namespace: k8s deployment namespace. e.g., default
        """
        super(ApiException, self).__init__(duration, interval)
        self.service = service
        self.classname = classname
        self.methodname = methodname
        self.namespace = namespace

    def init(self):
        container_id, host_ip = get_one_container_id_with_host_ip(self.namespace, self.service)
        self.ip = host_ip
        self.cmd = f'create cri jvm throwCustomException \
                    --chaosblade-release ~/chaosblade/chaosblade-1.5.0-linux-amd64.tar.gz \
                    --classname {self.classname} \
                    --methodname {self.methodname} \
                    --container-id {container_id} \
                    --pid 1 \
                    --exception java.lang.Exception'
