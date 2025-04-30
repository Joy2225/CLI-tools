import os
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: build_qbdi yourfile.cpp")
        return

    cpp_file = sys.argv[1]
    if not os.path.exists(cpp_file):
        print(f"Error: File \"{cpp_file}\" not found.")
        return

    vswhere = os.path.join(os.environ["ProgramFiles(x86)"], "Microsoft Visual Studio", "Installer", "vswhere.exe")
    if not os.path.exists(vswhere):
        print("vswhere.exe not found.")
        print("Please install Visual Studio with C++ development tools.")
        return

    try:
        vs_path = subprocess.check_output([
            vswhere, "-latest", "-products", "*",
            "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
            "-property", "installationPath"
        ], encoding='utf-8').strip()
    except subprocess.CalledProcessError:
        print("Failed to detect Visual Studio installation.")
        return

    if not vs_path:
        print("No suitable Visual Studio installation found.")
        return

    vcvarsall = os.path.join(vs_path, "VC", "Auxiliary", "Build", "vcvarsall.bat")
    if not os.path.exists(vcvarsall):
        print("vcvarsall.bat not found.")
        return

    qbdi_include = r"C:\Program Files\QBDI 0.11.0\include"
    qbdi_lib = r"C:\Program Files\QBDI 0.11.0\lib\QBDI_static.lib"

    if not os.path.exists(qbdi_include) or not os.path.exists(qbdi_lib):
        print("QBDI not found in default location.")
        print("Please install QBDI and ensure the include and lib directories exist.")
        return
    
    compile_cmd = f'cmd /c "\"{vcvarsall}\" x64 && cl /I\"{qbdi_include}\" /MD /EHsc \"{cpp_file}\" \"{qbdi_lib}\""'
    
    subprocess.run(compile_cmd, shell=True)

if __name__ == "__main__":
    main()