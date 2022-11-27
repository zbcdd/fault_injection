import logging
from abc import ABCMeta, abstractmethod, ABC
from utils.chaosblade import execute_cmd as chaosblade_cmd
from utils.chaosmesh import execute_cmd as chaosmesh_cmd


class BasicCommand(metaclass=ABCMeta):
    def __init__(self, duration: int, interval: int):
        self.duration = duration
        self.interval = interval

    @abstractmethod
    def init(self):
        """Init command.
        For ChaosBladeCommand, self.init() will be done at execute command stage.
        For ChaosMeshCommand, self.init() will be done at scheduler stage(when create the command).
        """
        raise NotImplementedError()

    @abstractmethod
    def execute(self):
        raise NotImplementedError()

    @abstractmethod
    def destroy(self):
        raise NotImplementedError()


class ChaosBladeCommand(BasicCommand, ABC):

    def __init__(self, duration: int, interval: int):
        super(ChaosBladeCommand, self).__init__(duration, interval)
        self.ip = None
        self.cmd = None
        self.res = None

    def __str__(self):
        return f'[chaosblade cmd] ip: {self.ip}, cmd: {self.cmd}, res: {self.res}'

    def execute(self):
        self.init()
        assert self.ip is not None
        assert self.cmd is not None
        self.res = chaosblade_cmd(self.ip, self.cmd)

    def destroy(self):
        if self.res and 'result' in self.res:
            chaosblade_cmd(self.ip, f"destroy {self.res['result']}")
        else:
            logging.error(f'Chaosblade cannot destroy command because of missing result uid.')


class ChaosMeshCommand(BasicCommand, ABC):

    def __init__(self, duration: int, interval: int):
        super(ChaosMeshCommand, self).__init__(duration, interval)
        self.k8s_yaml_path = None

    def __str__(self):
        return f'[chaosmesh cmd] k8s_yaml_path: {self.k8s_yaml_path}'

    def execute(self):
        assert self.k8s_yaml_path is not None
        chaosmesh_cmd(f'kubectl apply -f {self.k8s_yaml_path}')

    def destroy(self):
        assert self.k8s_yaml_path is not None
        chaosmesh_cmd(f'kubectl delete -f {self.k8s_yaml_path}')
