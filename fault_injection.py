import os.path

import click
import logging
import kubernetes
from utils.file import load_yaml, make_sure_dir_exists
from utils.chaosblade import check_all_chaosblade_status
from utils.chaosmesh import check_all_chaosmesh_status


@click.command()
@click.option('--k8s', help='Kubernetes kube_config config information yaml.', required=True)
@click.option('--fault', help='Fault injection config information yaml.', required=True)
def _fault_injection(k8s: str, fault: str) -> None:
    # config
    k8s_config = load_yaml(k8s)['k8s']
    kubernetes.config.load_kube_config(k8s_config['kube_config'])
    fault_config = load_yaml(fault)
    log_filepath = os.path.join(fault_config['logs']['dir'],
                                f"{fault_config['injection']['metadata']['st_time']}.logs")
    make_sure_dir_exists(log_filepath)
    log_format = fault_config['logs']['format']
    logging.basicConfig(filename=log_filepath, level=logging.INFO, format=log_format)
    logging.getLogger('apscheduler').setLevel(logging.WARNING)

    # check lab environment clean
    ips = [node['ip'] for node_type in ['k8s-master', 'k8s-nodes'] for node in k8s_config[node_type]]
    check_all_chaosblade_status(ips)
    check_all_chaosmesh_status(fault_config['injection']['metadata']['chaosmesh']['kinds'])
    logging.info(f'Lab environment clean!')

    # fault injection
    faults = fault_config['injection']['metadata']['faults']
    spec = fault_config['injection']['spec']
    for fault_name in faults:
        fault = spec[fault_name]
        fault_info = fault['info']
        fault_targets = fault['targets']
        for target in fault_targets:
            pass  # TODO


if __name__ == '__main__':
    _fault_injection()
