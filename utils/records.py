import logging
import os.path
import pandas as pd
from typing import List
from datetime import datetime
from chaosblade import get_all_ips_chaosblade_records
from chaosmesh import get_chaosmesh_records
from typing import Dict


def conflict_panic(record: Dict, fault_type1: str, fault_type2: str):
    logging.error(f'Find record which matches at least two fault_types: {fault_type1}, {fault_type2}: {record}')
    raise Exception(f'Find record which matches at least two fault_types: {fault_type1}, {fault_type2}: {record}')


def get_info_from_chaosblade_record(record: Dict) -> Dict:
    command = record['Command']
    sub_command = record['SubCommand']
    flag = record['Flag']
    flag_dict = {}
    flag_items = flag.strip().split()
    for item in flag_items:
        k, v = item.strip().split('=')
        flag_dict[k] = v

    res = {
        'fault_type': '',
        'target': '',
        'cmd': ' '.join([command, sub_command, flag])
    }

    def set_res(fault_type: str, target: str):
        if res['fault_type'] or res['target']:
            conflict_panic(record, res['fault_type'], fault_type)
        res['fault_type'] = fault_type
        res['target'] = target

    if command == 'k8s':
        src_pod_names = flag_dict['--names'].strip().split(',')
        dest_pod_ips = flag_dict['--destination-ip'].strip().split(',')
        if sub_command == 'pod-network delay':
            if len(src_pod_names) == 1 and len(dest_pod_ips) == 1:
                set_res('pod-pod-network-delay', f'{src_pod_names[0]} {dest_pod_ips[0]}')
            if len(src_pod_names) > 1 and len(dest_pod_ips) > 1:
                set_res('svc-svc-network-delay', f"{','.join(src_pod_names)} {','.join(dest_pod_ips)}")
        if sub_command == 'container-network drop':
            if len(src_pod_names) == 1 and len(dest_pod_ips) == 1:
                set_res('pod-pod-network-drop', f'{src_pod_names[0]} {dest_pod_ips[0]}')
            if len(src_pod_names) > 1 and len(dest_pod_ips) > 1:
                set_res('svc-svc-network-drop', f"{','.join(src_pod_names)} {','.join(dest_pod_ips)}")

    if command == 'cri':
        container_id = flag_dict['--container-id']
        classname = flag_dict['--classname']
        methodname = flag_dict['--methodname']
        if sub_command == 'jvm delay':
            set_res('api-delay', f'{container_id} {classname} {methodname}')
        if sub_command == 'jvm throwCustomException':
            set_res('api-exception', f'{container_id} {classname} {methodname}')

    if not res['fault_type']:
        logging.error(f"Cannot find fault type for record: {record}")
        raise Exception(f"Cannot find fault type for record: {record}")

    return res


def get_records(chaosblade_ips: List[str], chaosmesh_url: str, chaosmesh_tmp_dir: str,
                st_time: datetime, ed_time: datetime) -> pd.DataFrame:
    data = {
        'uid': [],
        'tool': [],
        'ip': [],
        'fault_type': [],
        'target': [],
        'status': [],
        'st_time': [],
        'ed_time': [],
        'filename': [],
        'cmd': []
    }

    chaosblade_records = get_all_ips_chaosblade_records(chaosblade_ips, st_time, ed_time)
    for ip, records in chaosblade_records.items():
        for record in records:
            if record['Status'] != 'Destroyed':
                logging.error(f'Find chaosblade record which status is not Destroyed: {record}')
                raise Exception(f'Find chaosblade record which status is not Destroyed: {record}')
            record_info = get_info_from_chaosblade_record(record)
            data['uid'].append(record['Uid'])
            data['tool'].append('chaosblade')
            data['ip'].append(ip)
            data['fault_type'].append(record_info['fault_type'])
            data['target'].append(record_info['target'])
            data['status'].append(record['Status'])
            data['st_time'].append(record['CreateTime'])
            data['ed_time'].append(record['UpdateTime'])
            data['filename'].append(f"{record['CreateTime']}_{record['UpdateTime']}")
            data['cmd'].append(record_info['cmd'])

    chaosmesh_records = get_chaosmesh_records(chaosmesh_url, st_time, ed_time)
    chaosmesh_dict = {}
    for record in chaosmesh_records:
        uid = record['object_id']
        if uid not in chaosmesh_dict:
            chaosmesh_dict[uid] = []
        chaosmesh_dict[uid].append(record)

    for uid, records in chaosmesh_dict.items():
        apply_records = []
        recover_records = []
        name = records[0]['name']
        apply_targets = []
        recover_targets = []
        record_st_time = None
        record_ed_time = None

        for record in records:
            message = record['message']
            create_time = record['create_time']
            if message.startswith('Successfully apply chaos for'):
                apply_records.append(record)
                apply_targets.append(message.strip().split()[-1].split('/')[-1])
                if not record_st_time or create_time > record_st_time:
                    record_st_time = create_time
            if message.startswith('Successfully recover chaos for'):
                recover_records.append(record)
                recover_targets.append(message.strip().split()[-1].split('/')[-1])
                if not record_ed_time or create_time < record_ed_time:
                    record_ed_time = create_time

        apply_targets = sorted(apply_targets)
        recover_targets = sorted(recover_targets)
        if apply_targets != recover_targets:
            logging.error(f'chaosmesh apply records did not match the recover records. apply: {apply_targets}, recover: {recover_targets}')
            raise Exception(f'chaosmesh apply records did not match the recover records. apply: {apply_targets}, recover: {recover_targets}')
        data['uid'].append(uid)
        data['tool'].append('chaosmesh')
        data['ip'].append('k8s-master')
        data['fault_type'].append(name.split('.')[0])
        data['target'].append(','.join(apply_targets))
        data['status'].append('ok')
        data['st_time'].append(record_st_time)
        data['ed_time'].append(record_ed_time)
        data['filename'].append(f'{record_st_time}_{record_ed_time}')
        with open(os.path.join(chaosmesh_tmp_dir, f'{name}.yaml'), 'r', encoding='utf-8') as f:
            data['cmd'].append(f.read().replace('\n', '\\n'))

        df = pd.DataFrame(data)
        df = df.sort_values('st_time')
        return df


if __name__ == '__main__':
    with open('../command/chaos_mesh/templates/http_request_delay.yaml', 'r', encoding='utf-8') as f:
        print(f.read().replace('\n', '\\n'))

