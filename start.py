#! /usr/bin/env python
import os
import shutil
import sys

from getgauge import connection, processor

PROJECT_ROOT_ENV = 'GAUGE_PROJECT_ROOT'
STEP_IMPL_DIR = "step_impl"
project_root = os.environ[PROJECT_ROOT_ENV]
impl_dir = os.path.join(project_root, STEP_IMPL_DIR)


def main():
    if sys.argv[1] == "--init":
        print("Initialising Gauge Python project")
        print("create  {}".format(impl_dir))
        shutil.copytree(STEP_IMPL_DIR, impl_dir)
    else:
        s = connection.connect()
        __import__("step_impl.step_impl")
        processor.dispatch_messages(s)


if __name__ == '__main__':
    main()
