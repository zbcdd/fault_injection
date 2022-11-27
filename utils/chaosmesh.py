import subprocess
import logging
from typing import Tuple, List


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


def get_chaosmesh_record(ip: str, st_time: datetime, ed_time: datetime) -> List[Dict]:
    TODO