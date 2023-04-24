import logging
from typing import Dict
from .basic_command import BasicCommand
from .chaos_blade.api import ApiDelay, ApiException
from .chaos_blade.pod_pod import PodPodNetworkDelay, PodPodNetworkDrop
from .chaos_blade.svc_svc import SvcSvcNetworkDelay, SvcSvcNetworkDrop
from .chaos_blade.pod import PodCpuFull, PodMysqlDelay, PodTypedMysqlDelay, PodRabbitmqDelay
from .chaos_blade.svc import SvcCpuFull
from .chaos_blade.jvm import JvmCpuFull
from .chaos_mesh.pod import PodHttpRequestDelay, PodHttpRequestAbort
from .chaos_mesh.svc import SvcHttpRequestDelay, SvcHttpRequestAbort


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
        idx = fault_info['idx']
        if command_name.startswith('api'):
            service, classname, methodname = target.strip().split()
            if command_name == 'api-delay':
                return ApiDelay(service, classname, methodname, time, duration, interval, namespace, idx)
            if command_name == 'api-exception':
                return ApiException(service, classname, methodname, duration, interval, namespace)

        if command_name.startswith(('pod-http', 'svc-http')):
            app, port = target.strip().split()
            if command_name == 'pod-http-request-delay':
                return PodHttpRequestDelay(tmp_dir, app, port, time, duration, interval, namespace)
            if command_name == 'pod-http-request-abort':
                return PodHttpRequestAbort(tmp_dir, app, port, duration, interval, namespace)
            if command_name == 'svc-http-request-delay':
                return SvcHttpRequestDelay(tmp_dir, app, port, time, duration, interval, namespace)
            if command_name == 'svc-http-request-abort':
                return SvcHttpRequestAbort(tmp_dir, app, port, duration, interval, namespace)

        if command_name.startswith(('pod-pod-network', 'svc-svc-network')):
            src, dest = target.strip().split()
            if command_name == 'pod-pod-network-delay':
                return PodPodNetworkDelay(k8s_master_ip, src, dest, interface, time, duration, interval, namespace)
            if command_name == 'pod-pod-network-drop':
                return PodPodNetworkDrop(k8s_master_ip, src, dest, interface, duration, interval, namespace)
            if command_name == 'svc-svc-network-delay':
                return SvcSvcNetworkDelay(k8s_master_ip, src, dest, interface, time, duration, interval, namespace)
            if command_name == 'svc-svc-network-drop':
                return SvcSvcNetworkDrop(k8s_master_ip, src, dest, interface, duration, interval, namespace)

        if command_name in ('pod-mysql-delay', 'jvm-cpu-full', 'pod-cpu-full', 'svc-cpu-full', 'pod-rabbitmq-delay'):
            pod_prefix = target.strip()
            if command_name == 'pod-mysql-delay':
                return PodMysqlDelay(pod_prefix, time, duration, interval, namespace, idx)
            if command_name == 'jvm-cpu-full':
                return JvmCpuFull(pod_prefix, duration, interval, namespace)
            if command_name == 'pod-cpu-full':
                return PodCpuFull(k8s_master_ip, pod_prefix, duration, interval, namespace)
            if command_name == 'svc-cpu-full':
                return SvcCpuFull(k8s_master_ip, pod_prefix, duration, interval, namespace)
            if command_name == 'pod-rabbitmq-delay':
                return PodRabbitmqDelay(pod_prefix, time, duration, interval, namespace, idx)

        if command_name == 'pod-typed-mysql-delay':
            pod_prefix, sqltype = target.strip().split()
            return PodTypedMysqlDelay(pod_prefix, sqltype, time, duration, interval, namespace, idx)

        logging.error(f'Cannot recognize command name: {command_name}')
        raise Exception(f'Cannot recognize command name: {command_name}')
