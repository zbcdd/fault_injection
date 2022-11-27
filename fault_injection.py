import click
import kubernetes
import logging
import os
from command.command_builder import CommandBuilder
from command.command_scheduler import CommandScheduler
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
                                f"{fault_config['injection']['metadata']['st_time']}.log")
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
    st_time = fault_config['injection']['metadata']['st_time']
    tt_namespace = fault_config['injection']['metadata']['namespace']
    chaosmesh_tmp_dir = fault_config['injection']['metadata']['chaosmesh']['tmp_dir']
    faults = fault_config['injection']['metadata']['faults']
    spec = fault_config['injection']['spec']
    command_builder = CommandBuilder()
    command_scheduler = CommandScheduler(st_time)
    for fault_name in faults:
        fault = spec[fault_name]
        fault_info = fault['info']
        fault_info['tt_namespace'] = tt_namespace
        fault_info['chaosmesh_tmp_dir'] = chaosmesh_tmp_dir
        fault_info['fault_name'] = fault_name
        fault_targets = fault['targets']
        for target in fault_targets:
            cmd = command_builder.build(fault_info, target)
            command_scheduler.add_job(cmd)


if __name__ == '__main__':
    _fault_injection()
