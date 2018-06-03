#!/usr/bin/env python

import logging
import sys
import i3

LOGGER = logging.getLogger()
LOG_FILE = '/tmp/i3-desktops.log'

OUTPUT_MAPPING = {
    'HDMI-0': 1,
    'DP-2': 2,
    'HDMI-1': 3,
}

def setup_logger():
    """Initializes the logger"""
    LOGGER.setLevel(logging.DEBUG)
    channel = logging.FileHandler(LOG_FILE)
    channel.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    channel.setFormatter(formatter)
    LOGGER.addHandler(channel)

def get_focused_output():
    for workspace in i3.get_workspaces():
        if workspace['focused']:
            return workspace['output']
    raise LookupError('No focused output found')

def get_workspace_prefix(output):
    prefix = OUTPUT_MAPPING.get(output, None)
    return prefix

def get_workspace_num(prefix, num):
    ws_num = (prefix*10) + int(num)
    return ws_num

def get_workspace(ws_num, prefix, num):
    workspace = '{}:{}-{}'.format(ws_num, prefix, num)
    return workspace

def switch_workspace(name):
    i3.workspace('{}'.format(name))

def change_workspace(num):
    """
    Switches to workspace num
    """
    LOGGER.debug('change_workspace: requested workspace {}'.format(num))
    output = get_focused_output()
    prefix = get_workspace_prefix(output)
    ws_num = get_workspace_num(prefix, num)
    workspace = get_workspace(ws_num, prefix, num)
    cmd = '{}'.format(workspace)
    success = i3.workspace(cmd)
    if not success:
        LOGGER.debug('change_workspace: faild to run command: {}'.format(cmd))

def move_container(num):
    LOGGER.debug('move_container: requested workspace {}'.format(num))
    output = get_focused_output()
    prefix = get_workspace_prefix(output)
    ws_num = get_workspace_num(prefix, num)
    workspace = get_workspace(ws_num, prefix, num)
    cmd = 'container to workspace {}'.format(workspace)
    success = i3.move(cmd)
    if not success:
        LOGGER.debug('move_container: faild to run command: {}'.format(cmd))

if __name__ == '__main__':
    setup_logger()

    try:
        if len(sys.argv) == 2:
            num = sys.argv[1]
            change_workspace(num)
        elif len(sys.argv) == 3:
            cmd = sys.argv[1]
            num = sys.argv[2]
            if cmd == 'move':
                move_container(num)
            else:
                LOGGER.critical('unknown cmd: {}'.format(cmd))
                sys.exit(1)
        else:
            LOGGER.critical('Usage: {} <cmd: optional> <ws_num>'.format(sys.argv[0]))
            sys.exit(1)
    except Exception:
        LOGGER.exception('An error occured')
