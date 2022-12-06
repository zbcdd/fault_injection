import os
from datetime import datetime
from utils.file import make_sure_dir_exists
from utils.records import get_records


if __name__ == '__main__':
    time_format = '%Y-%m-%d %H:%M:%S'
    st_time = datetime.strptime('2022-12-06 00:05:00', time_format)
    final_time = datetime.strptime('2022-12-06 08:05:00', time_format)
    st_time_str = str(st_time).replace(' ', 'T')
    final_time_str = str(final_time).replace(' ', 'T')
    record_path = os.path.join('./records/', f'{st_time_str}_{final_time_str}.csv')
    make_sure_dir_exists(record_path)
    chaosmesh_url = 'http://10.176.122.154:30331/api/events'
    ips = [
        '10.176.122.154',
        '10.176.122.151',
        '10.176.122.152',
        '10.176.122.153',
        '10.176.122.161',
        '10.176.122.162'
    ]
    df = get_records(ips, chaosmesh_url, './command/chaos_mesh/tmp/', st_time, final_time)
    df.to_csv(record_path, index=False)
    print(f'records saved at {record_path}, st_time: {st_time}, final_time: {final_time}')
