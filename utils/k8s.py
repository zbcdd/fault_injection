import kubernetes
from kubernetes import client
from typing import Tuple, List


def get_one_container_id_with_host_ip(namespace: str, service_name: str) -> Tuple[str, str, str]:
    pods = client.CoreV1Api().list_namespaced_pod(namespace)
    for pod in pods.items:
        if pod.metadata.name.startswith(service_name):
            pod_name = pod.metadata.name
            container_id = pod.status.container_statuses[0].container_id.split('//')[-1]
            host_ip = pod.status.host_ip
            return pod_name, container_id, host_ip
    return '', '', ''


def get_one_src_name_dest_ip(namespace: str, src: str, dest: str) -> Tuple[str, str, str]:
    pods = client.CoreV1Api().list_namespaced_pod(namespace)
    src_pod_name, dest_pod_name, dest_pod_ip = '', '', ''
    for pod in pods.items:
        if not src_pod_name and pod.metadata.name.startswith(src):
            src_pod_name = pod.metadata.name
        if not dest_pod_ip and pod.metadata.name.startswith(dest):
            dest_pod_name = pod.metadata.name
            dest_pod_ip = pod.status.pod_ip
        if src_pod_name and dest_pod_name and dest_pod_ip:
            break
    return src_pod_name, dest_pod_name, dest_pod_ip


def get_all_src_names_dest_ips(namespace: str, src: str, dest: str) -> Tuple[List[str], List[str], List[str]]:
    pods = client.CoreV1Api().list_namespaced_pod(namespace)
    src_pod_names, dest_pod_names, dest_pod_ips = [], [], []
    for pod in pods.items:
        if pod.metadata.name.startswith(src):
            src_pod_names.append(pod.metadata.name)
        if pod.metadata.name.startswith(dest):
            dest_pod_names.append(pod.metadata.name)
            dest_pod_ips.append(pod.status.pod_ip)
    return src_pod_names, dest_pod_names, dest_pod_ips


def get_pod_names(namespace: str, pod_prefix: str) -> List[str]:
    pods = client.CoreV1Api().list_namespaced_pod(namespace)
    res = [pod.metadata.name for pod in pods.items if pod.metadata.name.startswith(pod_prefix)]
    return res
