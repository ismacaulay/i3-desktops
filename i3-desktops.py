#!/usr/bin/env python

import logging
import sys
import i3ipc

i3 = i3ipc.Connection()

LOGGER = logging.getLogger()
LOG_FILE = '/tmp/i3-desktops.log'

OUTPUT_MAPPING = {
    'HDMI-0': 2,
    # 'DVI-D-0': 1,
    'DP-0': 1,
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
        if workspace.focused:
            return workspace.output
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
    return i3.command(f'workspace {name}')[0]

def move_container_to_workspace(name):
    return i3.command(f'move container to workspace {name}')[0]

def change_workspace(num):
    """
    Switches to workspace num
    """
    LOGGER.debug('change_workspace: requested workspace {}'.format(num))
    output = get_focused_output()
    prefix = get_workspace_prefix(output)
    ws_num = get_workspace_num(prefix, num)
    workspace = get_workspace(ws_num, prefix, num)
    result = switch_workspace(f'{workspace}')
    if not result.success:
        LOGGER.debug(f'change_workspace: faild to run command: {workspace}')
        LOGGER.debug(result.error)

def move_container(num):
    LOGGER.debug('move_container: requested workspace {}'.format(num))
    output = get_focused_output()
    prefix = get_workspace_prefix(output)
    ws_num = get_workspace_num(prefix, num)
    workspace = get_workspace(ws_num, prefix, num)
    result = move_container_to_workspace(workspace)
    if not result.success:
        LOGGER.debug(f'move_container: faild to move container to workspace {workspace}')
        LOGGER.debug(result.error)

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
