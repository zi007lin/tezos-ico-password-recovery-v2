import PyInstaller.__main__
import os
import site
import bitcoin

# Get the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get bitcoin package directory
bitcoin_dir = os.path.dirname(bitcoin.__file__)
english_txt = os.path.join(bitcoin_dir, "english.txt")

PyInstaller.__main__.run(
    [
        "PassRecoveryMain.py",  # Your main script
        "--name=TezosPasswordRecovery",  # Name of the executable
        "--onefile",  # Create a single executable
        "--windowed",  # Windows only: hide console window
        "--icon=assets/tz_recovery.ico",  # Application icon
        f"--add-data={english_txt};bitcoin",  # Include bitcoin wordlist
        "--add-data=assets/tz_recovery.png;assets",  # Include splash image
        "--add-data=assets/tz_recovery.ico;assets",  # Include icon file
        "--clean",  # Clean cache
        "--noconfirm",  # Replace output directory without asking
        f'--distpath={os.path.join(current_dir, "dist")}',  # Output directory
        f'--workpath={os.path.join(current_dir, "build")}',  # Work directory
        "--noconsole",  # No console window
        "--hidden-import=bitcoin",  # Force include bitcoin module
        "--hidden-import=bitcoin.mnemonic",  # Force include mnemonic module
        "--hidden-import=yaml",  # Add PyYAML dependency
    ]
)
