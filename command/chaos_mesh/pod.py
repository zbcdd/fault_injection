import os
import yaml
from string import Template
from utils.file import dump_yaml
from command import ChaosMeshCommand


class PodHttpRequestDelay(ChaosMeshCommand):
    def __init__(self, tmp_dir, app, port, time, duration, interval, namespace):
        """ Chaos-mesh HTTPChaos request delay
        chaos-mesh yaml: ./templates/http_request_delay.yaml
        :param tmp_dir: temp dir to generate middle files. e.g, ./command/chaos_mesh/tmp/
        :param app: label selector, key is 'app'. e.g, ts-verification-code-service
        :param port: service port. e.g, 15678
        :param time: delay time (ms). e.g., 500
        :param duration: duration of the fault injection (s). e.g., 300
        :param interval: interval between current and next fault injections (s). e.g., 300
        :param namespace: k8s deployment namespace. e.g., default
        """
        super(PodHttpRequestDelay, self).__init__(duration, interval)
        self.tmp_dir = tmp_dir
        self.app = app
        self.port = port
        self.time = time
        self.namespace = namespace

    def init(self):
        name = f'pod-http-request-delay.{self.app}'
        self.k8s_yaml_path = os.path.join(self.tmp_dir, f'{name}.yaml')
        values = {
            'name': name,
            'namespace': self.namespace,
            'app': self.app,
            'mode': 'one',
            'port': self.port,
            'delay': f'{self.time}ms',
            'duration': f'{self.duration}s'
        }
        with open('./templates/http_request_delay.yaml', 'r', encoding='utf-8') as f:
            res = Template(f.read()).substitute(values)
            dump_yaml(yaml.safe_load(stream=res), self.k8s_yaml_path)


class PodHttpRequestAbort(ChaosMeshCommand):
    def __init__(self, tmp_dir, app, port, duration, interval, namespace):
        """ Chaos-mesh HTTPChaos request abort
        chaos-mesh yaml: ./templates/http_request_abort.yaml
        :param tmp_dir: temp dir to generate middle files. e.g, ./command/chaos_mesh/tmp/
        :param app: label selector, key is 'app'. e.g, ts-verification-code-service
        :param port: service port. e.g, 15678
        :param duration: duration of the fault injection (s). e.g., 300
        :param interval: interval between current and next fault injections (s). e.g., 300
        :param namespace: k8s deployment namespace. e.g., default
        """
        super(PodHttpRequestAbort, self).__init__(duration, interval)
        self.tmp_dir = tmp_dir
        self.app = app
        self.port = port
        self.namespace = namespace

    def init(self):
        name = f'pod-http-request-abort.{self.app}'
        self.k8s_yaml_path = os.path.join(self.tmp_dir, f'{name}.yaml')
        values = {
            'name': name,
            'namespace': self.namespace,
            'app': self.app,
            'mode': 'one',
            'port': self.port,
            'duration': f'{self.duration}s'
        }
        with open('./templates/http_request_abort.yaml', 'r', encoding='utf-8') as f:
            res = Template(f.read()).substitute(values)
            dump_yaml(yaml.safe_load(stream=res), self.k8s_yaml_path)
