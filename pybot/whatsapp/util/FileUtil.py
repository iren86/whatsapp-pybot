# -*- coding: utf-8 -*-
import errno
import os


def mkdirs(file_path):
    assert file_path is not None, "File path must be initialized"
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def read_file_lines(file_path):
    assert os.path.isfile(file_path), \
        "File must exists: %s" % file_path

    lines = None
    with open(file_path, "rb") as f:
        # decode line before using it to avoid encoding problems
        lines = list(line.decode('utf8') for line in (l.strip() for l in f) if line)

    return lines


def read_file(file_path):
    assert os.path.isfile(file_path), \
        "File must exists: %s" % file_path

    return "\n".join(read_file_lines(file_path))
