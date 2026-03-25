import os
import shutil
import subprocess
import sys


def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    for folder in ("build", "dist"):
        if os.path.exists(folder):
            shutil.rmtree(folder)

    spec_file = "speedtest_gui.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)

    data_sep = ";" if os.name == "nt" else ":"
    output_name = "speedtest_trigger_gui.exe" if os.name == "nt" else "speedtest_gui"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--add-data",
        f"speedtest-cli{os.sep}speedtest.py{data_sep}speedtest-cli",
        "--add-data",
        f"icon.png{data_sep}.",
        "--hidden-import=xml",
        "--hidden-import=xml.etree",
        "--hidden-import=xml.etree.ElementTree",
        "--hidden-import=requests",
    ]

    if os.name == "nt":
        cmd.extend(
            [
                "--icon=icon.ico",
                "--add-data",
                f"icon.ico{data_sep}.",
            ]
        )

    cmd.append("speedtest_trigger_gui.py")

    print("Building app...")
    print(" ".join(cmd))
    print()

    result = subprocess.run(cmd)

    print()
    if result.returncode == 0:
        print("Build complete.")
        print(f"Output: dist{os.sep}{output_name}")
    else:
        print(f"Build failed with exit code {result.returncode}")

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
