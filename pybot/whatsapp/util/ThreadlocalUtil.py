# -*- coding: utf-8 -*-
import threading

threadlocal = threading.local()


def get_threadlocal_var(var):
    return getattr(threadlocal, var, None)


def set_threadlocal_var(var, value):
    setattr(threadlocal, var, value)
    return value
