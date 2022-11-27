import json
import logging
from datetime import datetime
from net import retry_session
from typing import Dict, List


def execute_cmd(ip: str, cmd: str, do_log: bool = True) -> Dict:
    req_url = f'http://{ip}:9526/chaosblade'
    session = retry_session(retries=5)
    response = session.get(req_url, params={'cmd': cmd})
    res = json.loads(response.text)
    if do_log:
        if 'result' not in res or 'code' not in res or res['code'] != 200:
            logging.error(f'Chaosblade execute command failed: {req_url}, {cmd}, {res}')
        else:
            logging.info(f'Chaosblade successfully execute command: {req_url}, {cmd}, {res}')
    return res


def check_chaosblade_status(ip: str) -> None:
    res = execute_cmd(ip, 'status --type c --asc', False)
    for fault in res['result']:
        if fault['Status'] != 'Destroyed':
            logging.error(f'Find fault which status is not Destroyed: {fault}')
            raise Exception(f'Find fault which status is not Destroyed: {fault}')
    logging.info(f'Check {ip} chaosblade faults status all Destroyed: ok.')


def check_all_chaosblade_status(ips: List[str]) -> None:
    for ip in ips:
        check_chaosblade_status(ip)
    logging.info(f"Check chaosblade status successfully! All clean: {','.join(ips)}")


def get_chaosblade_records(ip: str, st_time: datetime, ed_time: datetime) -> List[Dict]:
    res = execute_cmd(ip, 'status --type c --asc', False)
    records = res['result']

    def time_filter(record: Dict) -> bool:
        create_time_str = record['CreateTime'].split('.')[0]
        create_time = datetime.strptime(create_time_str, '%Y-%m-%dT%H:%M:%S')
        return st_time <= create_time <= ed_time

    return [record for record in records if time_filter(record)]


def get_all_ips_chaosblade_records(ips: List[str], st_time: datetime, ed_time: datetime) -> Dict[str, List[Dict]]:
    res = {}
    for ip in ips:
        res[ip] = get_chaosblade_records(ip, st_time, ed_time)
    return res
