# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from psutil import sensors_battery

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

]

# Name of Groups
groups = [Group('WWW', layout='max'),
          Group('DEV', layout='max'),
          Group('SYS', layout='max'),
          Group('DOC', layout='max'),
          Group('VID', layout='max'),
          Group('PHO', layout='max'),
          Group('MUS', layout='max'),
          Group('COM', layout='max'),
          Group('GFX', layout='max'), ]

for i in range(1, len(groups) + 1):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                str(i),
                lazy.group[groups[i - 1].name].toscreen(),
                desc="Switch to group {}".format(groups[i - 1].name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(i),
                lazy.window.togroup(groups[i - 1].name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(groups[i - 1].name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=2),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

colors = [['#000000', '#000000'],  # Bar background
          ['#b31902', '#e6b553'],  # Highlight Color
          ['#580201', '#580201'],  # Wine
          ['#ab0068', '#ab0068'],  # Purple
          ['#e00702', '#e00702'],  # Red
          ['#ff6c02', '#ff6c02'],  # Orange
          ['#fec106', '#fec106'],  # Yellow
          ['#149603', '#149603'],  # Green
          ['#ffffff', '#ffffff'],  # White
          ['#0030a8', '#0030a8'],  # Blue
          ]

widget_defaults = dict(
    font="Ubuntu Regular",
    fontsize=12,
    padding=3,
)


# Function for determining status color when battery has certain percentage left
def battery_color_status():
    battery = sensors_battery()
    percentage = battery.percent

    if percentage < 20:
        color_status = colors[4]
    elif 40 > percentage >= 20:
        color_status = colors[6]
    else:
        color_status = colors[7]

    return color_status


extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                # Workspaces
                widget.Spacer(length=5,
                              background=colors[2]),
                widget.GroupBox(highlight_method='line',
                                highlight_color=colors[1],
                                this_current_screen_border='fc7703',
                                inactive='5e5d5a',
                                background=colors[2]
                                ),
                widget.Spacer(length=3,
                              background=colors[2]),
                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[2],
                               background=colors[0],
                               padding=0),

                # Quick Spawn
                widget.Spacer(length=3,
                              background=colors[0]),
                widget.Prompt(),

                # Window Name
                widget.Spacer(length=3,
                              background=colors[0]),
                widget.WindowName(max_chars=70),
                # widget.Chord(
                #     chords_colors={
                #         "launch": ("#ff0000", "#ffffff"),
                #     },
                #     name_transform=lambda name: name.upper(),
                #     background=colors[2],
                # ),

                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[0],
                               background=colors[3],
                               padding=0),

                # Network
                widget.Spacer(length=3,
                              background=colors[3]),
                widget.TextBox(text='🌎',
                               background=colors[3]),
                widget.Net(background=colors[3],
                           format='↓{down} ↑{up}'),
                widget.Spacer(length=3,
                              background=colors[3]),
                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[3],
                               background=colors[4],
                               padding=0),

                # Layout
                widget.Spacer(length=3,
                              background=colors[4]),
                widget.TextBox(text='᎒᎒᎒',
                               background=colors[4]),
                widget.CurrentLayout(background=colors[4]),
                widget.Spacer(length=3,
                              background=colors[4]),
                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[4],
                               background=colors[5],
                               padding=0),

                # Calendar
                widget.Spacer(length=3,
                              background=colors[5]),
                widget.TextBox(text='📅',
                               background=colors[5]),
                widget.Clock(format="%d/%m/%Y",
                             background=colors[5]),
                widget.Spacer(length=3,
                              background=colors[5]),
                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[5],
                               background=colors[6],
                               padding=0),

                # Clock
                widget.Spacer(length=3,
                              background=colors[6]),
                widget.TextBox(text='🕒',
                               background=colors[6],
                               font_shadow=colors[0]),
                widget.Clock(format="%H:%M",
                             background=colors[6],
                             font_shadow=colors[0]),
                widget.Spacer(length=3,
                              background=colors[6]),
                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[6],
                               background=colors[9],
                               padding=0),

                # Battery
                widget.Spacer(length=3,
                              background=colors[9]),
                widget.Battery(format='{char} {percent:2.0%} {hour:d}:{min:02d}',
                               charge_char='⚡',
                               discharge_char='↯',
                               background=colors[9],
                               low_foreground=colors[4],
                               low_percentage=0.2,
                               notify_below=10),
                widget.Spacer(length=3,
                              background=colors[9]),
                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[9],
                               background=colors[8],
                               padding=0),

                # Utilities
                widget.Spacer(length=3,
                              background=colors[8]),
                widget.Systray(background=colors[8]),
                widget.Spacer(length=5,
                              background=colors[8]),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                # Workspaces
                widget.Spacer(length=5,
                              background=colors[2]),
                widget.GroupBox(highlight_method='line',
                                highlight_color=colors[1],
                                this_current_screen_border='fc7703',
                                inactive='5e5d5a',
                                background=colors[2]
                                ),
                widget.Spacer(length=3,
                              background=colors[2]),
                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[2],
                               background=colors[0],
                               padding=0),

                # Quick Spawn
                widget.Spacer(length=3,
                              background=colors[0]),
                widget.Prompt(),

                # Window Name
                widget.Spacer(length=3,
                              background=colors[0]),
                widget.WindowName(max_chars=70),
                # widget.Chord(
                #     chords_colors={
                #         "launch": ("#ff0000", "#ffffff"),
                #     },
                #     name_transform=lambda name: name.upper(),
                #     background=colors[2],
                # ),

                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[0],
                               background=colors[3],
                               padding=0),

                # Network
                widget.Spacer(length=3,
                              background=colors[3]),
                widget.TextBox(text='🌎',
                               background=colors[3]),
                widget.Net(background=colors[3],
                           format='↓{down} ↑{up}'),
                widget.Spacer(length=3,
                              background=colors[3]),
                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[3],
                               background=colors[4],
                               padding=0),

                # Layout
                widget.Spacer(length=3,
                              background=colors[4]),
                widget.TextBox(text='᎒᎒᎒',
                               background=colors[4]),
                widget.CurrentLayout(background=colors[4]),
                widget.Spacer(length=3,
                              background=colors[4]),
                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[4],
                               background=colors[5],
                               padding=0),

                # Calendar
                widget.Spacer(length=3,
                              background=colors[5]),
                widget.TextBox(text='📅',
                               background=colors[5]),
                widget.Clock(format="%d/%m/%Y",
                             background=colors[5]),
                widget.Spacer(length=3,
                              background=colors[5]),
                widget.TextBox(text='█',
                               font='Ubuntu Bold',
                               foreground=colors[5],
                               background=colors[6],
                               padding=0),

                # Clock
                widget.Spacer(length=3,
                              background=colors[6]),
                widget.TextBox(text='🕒',
                               background=colors[6],
                               font_shadow=colors[0]),
                widget.Clock(format="%H:%M",
                             background=colors[6],
                             font_shadow=colors[0]),
                widget.Spacer(length=5,
                              background=colors[6]),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


# Autostart stuff
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])
