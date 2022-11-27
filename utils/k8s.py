import kubernetes
from kubernetes import client
from typing import Tuple


def get_one_container_id_with_host_ip(namespace: str, service_name: str) -> Tuple[str, str]:
    pods = client.CoreV1Api().list_namespaced_pod(namespace)
    for pod in pods.items:
        if pod.metadata.name.startswith(service_name):
            container_id = pod.status.container_statuses[0].container_id.split('//')[-1]
            host_ip = pod.status.host_ip
            return container_id, host_ip
    return '', ''


if __name__ == '__main__':
    kubernetes.config.load_kube_config('../config/k8s/kube_config_154')
    get_one_container_id_with_host_ip('default', 'ts-verification-code-service')
