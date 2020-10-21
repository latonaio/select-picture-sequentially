#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Latona. All rights reserved.

import os
import sys
import random

from glob import glob
from time import sleep
from aion.microservice import main_decorator, Options
from aion.kanban import Kanban
from aion.logger import lprint, initialize_logger

SERVICE_NAME = os.environ.get("SERVICE")
SELECT_NUM = os.environ.get("SELECT_NUM", "3")
initialize_logger(SERVICE_NAME)


class NewerFileList():
    def __init__(self, expand, dir_path):
        self.expand = expand
        self.dir_path = dir_path
        self.file_list = []

    def set_file_list(self):
        self.file_list = sorted(
            glob(os.path.join(self.dir_path, "*." + self.expand)),
            reverse=False)

    def get_file_list_sequentially(self, start_num, end_num):
        return self.file_list[start_num:end_num]


class SelectPictureByTime():
    def __init__(self, dir_path):
        lprint("watch dir ", dir_path)
        if not os.path.isdir(dir_path):
            lprint("Error: transcript data is None")
            sys.exit(1)

        self.dir_path = dir_path
        self.search_jpg = NewerFileList("jpg", dir_path)
        self.index = 0

    def __call__(self, num=3):
        self.search_jpg.set_file_list()
        select_file_list = self.search_jpg.get_file_list_sequentially(self.index, self.index + num)
        self.index = self.index + num
        return select_file_list


@main_decorator(SERVICE_NAME)
def main(opt: Options):
    lprint("start select-picture-sequentially")

    conn = opt.get_conn()
    num = opt.get_number()
    kanban: Kanban = conn.set_kanban(SERVICE_NAME, num)

    # assume /var/lib/aion/Data/select-picture-by-random_1
    input_file_path = kanban.get_data_path()
    select_picture = SelectPictureByTime(input_file_path)

    while True:
        picture_list = select_picture(int(SELECT_NUM))

        if picture_list:
            conn.output_kanban(
                result=True,
                process_number=num,
                metadata={"picture_list": picture_list},
            )
            lprint("send picture_list ", picture_list)
        sleep(0.5)


if __name__ == "__main__":
    main()
