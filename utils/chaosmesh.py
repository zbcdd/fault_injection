import subprocess
import logging
import json
from typing import Tuple, List, Dict
from net import retry_session
from datetime import datetime, timedelta


def execute_cmd(cmd: str) -> Tuple[int, str]:
    status, output = subprocess.getstatusoutput(cmd)
    output_str = '\\n'.join(output.split('\n'))
    if status == 0:
        logging.info(f'Chaosmesh successfully execute command: cmd, status: {status}, output: {output_str}')
    else:
        logging.error(f'Chaosmesh execute command failed: cmd, status: {status}, output: {output_str}')
    return status, output


def check_all_chaosmesh_status(kinds: List[str]) -> None:
    for kind in kinds:
        cmd = f'kubectl get {kind} -A'
        status, output = execute_cmd(cmd)
        output_str = '\\n'.join(output.split('\n'))
        if status != 0:
            logging.error(f'Check chaosmesh status failed, status: {status}')
            raise Exception(f'Check chaosmesh status failed, status: {status}')
        if len(output.split('\n')) > 1:
            logging.error(f'Find {kind}, output: {output_str}')
            raise Exception(f'Find {kind}, output: {output_str}')
        logging.info(f'Chaosmesh {kind} clean!')
    logging.info('Check chaosmesh status successfully! All clean.')


def get_chaosmesh_records(url: str, st_time: datetime, ed_time: datetime) -> List[Dict]:
    session = retry_session(retries=5)
    records = json.loads(session.get(url).text)

    def time_filter(record: Dict) -> Tuple[bool, datetime]:
        create_time_str = record['created_at']
        create_time = datetime.strptime(create_time_str, '%Y-%m-%dT%H:%M:%SZ')
        create_time += timedelta(hours=8)
        return st_time <= create_time <= ed_time, create_time

    res = []
    for item in records:
        select, create_time = time_filter(item)
        if select:
            item['create_time'] = create_time.strftime('%Y-%m-%dT%H:%M:%S')
            res.append(item)

    return res


if __name__ == '__main__':
    st_time = datetime.strptime('2022-11-27T20:12:42', '%Y-%m-%dT%H:%M:%S')
    ed_time = datetime.strptime('2022-11-27T20:12:42', '%Y-%m-%dT%H:%M:%S')
    print(get_chaosmesh_records('http://10.176.122.154:30331/api/events', st_time, ed_time))
