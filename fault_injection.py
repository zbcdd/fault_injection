import click
import kubernetes
import logging
import os
import time
from datetime import datetime, timedelta
from command.command_builder import CommandBuilder
from command.command_scheduler import CommandScheduler
from utils.file import load_yaml, make_sure_dir_exists
from utils.chaosblade import check_all_chaosblade_status
from utils.chaosmesh import check_all_chaosmesh_status
from utils.records import get_records


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
    k8s_master_ip = next(iter(k8s_config['k8s-master']))['ip']
    spec = fault_config['injection']['spec']
    command_builder = CommandBuilder()
    command_scheduler = CommandScheduler(st_time)
    for fault_name in faults:
        fault = spec[fault_name]
        fault_info = fault['info']
        fault_info['namespace'] = tt_namespace
        fault_info['chaosmesh_tmp_dir'] = chaosmesh_tmp_dir
        fault_info['fault_name'] = fault_name
        fault_info['k8s_master_ip'] = k8s_master_ip
        fault_targets = fault['targets']
        for target in fault_targets:
            cmd = command_builder.build(fault_info, target)
            command_scheduler.add_job(cmd)

    # run
    command_scheduler.start()
    final_time = command_scheduler.cur_time + timedelta(minutes=10)
    try:
        while True:
            now = datetime.now()
            if now > final_time:
                command_scheduler.shutdown()
                break
            time.sleep(10)
    except(KeyboardInterrupt, SystemExit):
        command_scheduler.shutdown()

    # get record
    st_time_str = str(st_time).replace(' ', 'T')
    final_time_str = str(final_time).replace(' ', 'T')
    record_path = os.path.join(fault_config['records']['dir'], f'{st_time_str}_{final_time_str}.csv')
    make_sure_dir_exists(record_path)
    chaosmesh_url = fault_config['records']['chaosmesh_records']
    df = get_records(ips, chaosmesh_url, chaosmesh_tmp_dir, st_time, final_time)
    df.to_csv(record_path, index=False)
    logging.info(f'records saved at {record_path}, st_time: {st_time}, final_time: {final_time}')


if __name__ == '__main__':
    _fault_injection()
