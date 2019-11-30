# i3-desktops

Changes each monitor into individual desktops [i3 window manager](https://i3wm.org/) similar to the behaviour of [awesome](https://awesomewm.org/).

### Dependencies

- [i3ipc-python](https://github.com/altdesktop/i3ipc-python)

### Usage

```
Usage: i3-desktops.py <cmd: optional> <ws_num>

cmd:
    - move: moves the container

ws_num:
    - the workspaces number to use
```

### Setup

1. Download [i3-desktops.py](https://raw.githubusercontent.com/ismacaulay/i3-desktops/master/i3-desktops.py) or clone the repo
2. In `i3-desktops.py`, update the `OUTPUT_MAPPING` variable to specify which outputs you are using in which order. To find them, use `xrandr`.
3. Update the config:
    ```
    set $ws_switch exec --no-startup-id <path-to-i3-desktops>/i3-desktops.py

    # switching workspaces
    bindsym $mod+1 $ws_switch 1
    bindsym $mod+2 $ws_switch 2
    bindsym $mod+3 $ws_switch 3
    bindsym $mod+4 $ws_switch 4
    bindsym $mod+5 $ws_switch 5
    bindsym $mod+6 $ws_switch 6
    bindsym $mod+7 $ws_switch 7
    bindsym $mod+8 $ws_switch 8
    bindsym $mod+9 $ws_switch 9
    bindsym $mod+0 $ws_switch 10

    # moveing containers
    bindsym $mod+Shift+1 $ws_switch move 1
    bindsym $mod+Shift+2 $ws_switch move 2
    bindsym $mod+Shift+3 $ws_switch move 3
    bindsym $mod+Shift+4 $ws_switch move 4
    bindsym $mod+Shift+5 $ws_switch move 5
    bindsym $mod+Shift+6 $ws_switch move 6
    bindsym $mod+Shift+7 $ws_switch move 7
    bindsym $mod+Shift+8 $ws_switch move 8
    bindsym $mod+Shift+9 $ws_switch move 9
    bindsym $mod+Shift+0 $ws_switch move 10
    ```
4. To work nicely with i3, an internal workspace number is used, to hide this workspace number add the following to your config:
    ```
    bar {
        ...
        strip_workspace_numbers yes
        ...
    }
    ```
