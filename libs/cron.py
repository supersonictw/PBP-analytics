import asyncio
import multiprocessing
import time

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Cron:
    def __init__(self, pbp_handle):
        self.handle = pbp_handle
        self.task = None

    def start(self):
        self.task = CronTimer(self.handle)
        self.task.start()

    def stop(self):
        if self.task:
            self.task.terminal()


class CronTimer(multiprocessing.Process):
    def __init__(self, pbp_handle):
        multiprocessing.Process.__init__(self)
        self.handle = pbp_handle
        self.last_time = -1

    def run(self):
        while True:
            if time.localtime().tm_hour != self.last_time:
                self.last_time = time.localtime().tm_hour
                threads = Update(self.handle)
                threads.start()


class Update(multiprocessing.Process):
    def __init__(self, pbp_handle):
        multiprocessing.Process.__init__(self)
        self.handle = pbp_handle

    def run(self):
        asyncio.run(self.handle.gen_sample())
        self.handle.data_control.clean_result_cache()
        self.handle.update_blacklist_from_phishtank()