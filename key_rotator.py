"""
file: key_rotator.py
event: Brick Hack 6
author: Albin Liang
version: 0.0
purpose: A module that rotates the subscription keys for Wegman's API.
"""

import queue
KEYCHAIN = queue.Queue()

def init_keys(*args):
    """
    pass the Wegman's API Subscription Keys to this initializer
    :param args: variable number of subscription keys
    :return:
    """
    global KEYCHAIN
    for arg in args:
        print(arg)
        KEYCHAIN.put(arg)
    return none

def next_key(keychain):
    front = keychain.get()
    keychain.put(front)
    return front
