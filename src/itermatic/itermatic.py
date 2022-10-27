import os
import re
from pathlib import Path
from json import load
import iterm2
import AppKit
import yaml


def customize_profile(name):
    # create writable profile
    profile = iterm2.LocalWriteOnlyProfile()
    profile.set_allow_title_setting(True)
    # determine region (or default) for color assignment
    profile.set_tab_color(iterm2.Color(0, 255, 0))
    #profile.set_blend(0.1)
    profile.set_use_tab_color(True)
    profile.set_name(name)
    return profile

def load_config() -> dict:
    config_name = 'config.yml'
    config_path = Path(__file__).parent.resolve()
    with open(config_path/config_name) as config_file:
        return yaml.safe_load(config_file)

async def itermatic(connection):
    # load config.yml
    config = load_config()
    print(config)


    # get app handle
    app = await iterm2.async_get_app(connection)

    # set the dynamic profile or use default (no logging)
    profiles = await iterm2.PartialProfile.async_query(connection)
    # Iterate over each partial profile to find the profile you want to pull config or make changes
    #for partial in profiles:
    #    if partial.name == "Default":
    #        default_profile = await partial.async_get_full_profile()
    #await session.async_set_profile_properties(default_profile)

    window = await iterm2.Window.async_create(connection, profile="Default", 
            profile_customizations=customize_profile("Window1"))
    session = app.current_window.current_tab.current_session

    await session.async_split_pane(
                vertical=True, profile="Default", profile_customizations=customize_profile("Window2"))
    await window.async_set_title(config['window']['title'])
    # give focus to this tab
    await app.async_activate()

    # set to fullscreen
    #await app.current_window.async_set_fullscreen(True)
    # create alert window and generate text
    alert = iterm2.Alert(config['window']['alert_title'], config['window']['alert_text'])
    await alert.async_run(connection)


def main():
    # all argument validation, processing and loading
    #process_args()
    # Launch ITerm
    AppKit.NSWorkspace.sharedWorkspace().launchApplication_("iTerm")
    # Passing True for the second parameter means keep trying to
    # connect until the app launches.
    iterm2.run_until_complete(itermatic, True)

if __name__ == '__main__':
    main()