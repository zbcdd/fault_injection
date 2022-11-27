import logging
import subprocess
from abc import ABCMeta, abstractmethod, ABC
from utils.chaosblade import execute_cmd as chaosblade_cmd
from utils.chaosmesh import execute_cmd as chaosmesh_cmd


class BasicCommand(metaclass=ABCMeta):

    @abstractmethod
    def init(self):
        raise NotImplementedError()

    @abstractmethod
    def execute(self):
        raise NotImplementedError()

    @abstractmethod
    def destroy(self):
        raise NotImplementedError()


class ChaosBladeCommand(BasicCommand, ABC):

    def __init__(self):
        self.ip = None
        self.cmd = None
        self.res = None

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

    def __init__(self):
        self.k8s_yaml_path = None

    def execute(self):
        assert self.k8s_yaml_path is not None
        chaosmesh_cmd(f'kubectl apply -f {self.k8s_yaml_path}')

    def destroy(self):
        assert self.k8s_yaml_path is not None
        chaosmesh_cmd(f'kubectl delete -f {self.k8s_yaml_path}')
