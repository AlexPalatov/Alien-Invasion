import cx_Freeze


shortcut_table = [
    (
        "DesktopShortcut",              # Shortcut
        "DesktopFolder",                # Directory
        "Alien Invasion",               # Name
        "TARGETDIR",                    # Component
        "[TARGETDIR]alien_invasion.exe",# Target
        None,                           # Arguments
        "Alien Invasion by Sleepy Plov",# Description
        None,                           # Hotkey
        "[TARGETDIR]icon.ico",          # Icon
        "[TARGETDIR]icon.ico",          # IconIndex
        False,                          # ShowCmd
        'TARGETDIR'                     # WkDir
    )
]
msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

executables = [
    cx_Freeze.Executable("alien_invasion.py", base="Win32GUI", icon="icon.ico")
]

cx_Freeze.setup(
    name="Alien Invasion",
    options = {
        "bdist_msi": bdist_msi_options,
    },
    version="1.0",
    description="Alien Invasion game by Sleepy Plov",
    executables=executables
)
