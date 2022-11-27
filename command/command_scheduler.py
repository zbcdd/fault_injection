import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from .basic_command import BasicCommand


class CommandScheduler(object):
    def __init__(self, st_time: datetime):
        self.time_format = '%Y-%m-%d %H:%M:%S'
        self.cur_time = st_time
        self.scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

    def add_job(self, cmd: BasicCommand):
        self.scheduler.add_job(cmd.execute, 'date', run_date=self.cur_time)
        logging.info(f'Add execute job: [{self.cur_time.strftime(self.time_format)}] {cmd}')
        self.cur_time += timedelta(seconds=cmd.duration)

        self.scheduler.add_job(cmd.destroy, 'date', run_date=self.cur_time)
        logging.info(f'Add destroy job: [{self.cur_time.strftime(self.time_format)}] {cmd}')
        self.cur_time += timedelta(seconds=cmd.interval)

    def start(self):
        logging.info("[CommandScheduler] scheduler start.")
        self.scheduler.start()

    def shutdown(self):
        logging.info("[CommandScheduler] scheduler shutdown.")
        self.scheduler.shutdown()
