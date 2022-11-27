import logging
from typing import Dict
from .basic_command import BasicCommand
from chaos_blade.api import ApiDelay, ApiException
from chaos_blade.pod_pod import PodPodNetworkDelay, PodPodNetworkDrop
from chaos_blade.svc_svc import SvcSvcNetworkDelay, SvcSvcNetworkDrop
from chaos_mesh.pod import PodHttpRequestDelay, PodHttpRequestAbort
from chaos_mesh.svc import SvcHttpRequestDelay, SvcHttpRequestAbort


class CommandBuilder(object):

    @staticmethod
    def build(fault_info: Dict, target: str) -> BasicCommand:
        command_name = fault_info['fault_name']
        namespace = fault_info['namespace']
        duration = fault_info['duration']
        interval = fault_info['interval']
        time = fault_info['time'] if 'time' in fault_info else None
        interface = fault_info['interface'] if 'interface' in fault_info else None
        tmp_dir = fault_info['chaosmesh_tmp_dir']
        k8s_master_ip = fault_info['k8s_master_ip']
        if command_name.startswith('api'):
            service, classname, methodname = target.strip().split()
            if command_name == 'api-delay':
                return ApiDelay(service, classname, methodname, time, duration, interval, namespace)
            if command_name == 'api-exception':
                return ApiException(service, classname, methodname, duration, interval, namespace)

        if command_name.startswith(['pod-http', 'svc-http']):
            app, port = target.strip().split()
            if command_name == 'pod-http-request-delay':
                return PodHttpRequestDelay(tmp_dir, app, port, time, duration, interval, namespace)
            if command_name == 'pod-http-request-abort':
                return PodHttpRequestAbort(tmp_dir, app, port, duration, interval, namespace)
            if command_name == 'svc-http-request-delay':
                return SvcHttpRequestDelay(tmp_dir, app, port, time, duration, interval, namespace)
            if command_name == 'svc-http-request-abort':
                return SvcHttpRequestAbort(tmp_dir, app, port, duration, interval, namespace)

        if command_name.startswith(['pod-pod-network', 'svc-svc-network']):
            src, dest = target.strip().split()
            if command_name == 'pod-pod-network-delay':
                return PodPodNetworkDelay(k8s_master_ip, src, dest, interface, time, duration, interval, namespace)
            if command_name == 'pod-pod-network-drop':
                return PodPodNetworkDrop(k8s_master_ip, src, dest, interface, duration, interval, namespace)
            if command_name == 'svc-svc-network-delay':
                return SvcSvcNetworkDelay(k8s_master_ip, src, dest, interface, time, duration, interval, namespace)
            if command_name == 'svc-svc-network-drop':
                return SvcSvcNetworkDrop(k8s_master_ip, src, dest, interface, duration, interval, namespace)

        logging.error(f'Cannot recognize command name: {command_name}')
        raise Exception(f'Cannot recognize command name: {command_name}')