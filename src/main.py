# GUI and Logic

import os
import platform
import subprocess
import sys
import ctypes
import wmi
import urllib.request
import webbrowser

## packages path (when finishied)
#INSTALLERS = {
#    "directx": "src/installers/directx.exe",
#    "dotnet": "src/installers/dotnet.exe",
#    "vc_redist": {
#        "x86": "src/installers/vc_redist.x86.exe",
#        "x64": "src/installers/vc_redist.x64.exe",
#        "arm64": "src/installers/vc_redist.arm64.exe"
#    }
#}

# packages path (for testing)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLERS = {
    "directx": os.path.join(ROOT_DIR, "installers/directx.exe"),
    "dotnet": os.path.join(ROOT_DIR, "installers/dotnet.exe"),
    "vc_redist": {
        "x86": os.path.join(ROOT_DIR, "installers/vc_redist.x86.exe"),
        "x64": os.path.join(ROOT_DIR, "installers/vc_redist.x64.exe"),
        "arm64": os.path.join(ROOT_DIR, "installers/vc_redist.arm64.exe")
    }
}

# Autodetect OS Arch
def detect_arch():
    arch = platform.machine().lower()
    if "amd64" in arch or "x86_64" in arch:
        return "x64"
    elif "arm64" in arch:
        return "arm64"
    elif "x86" in arch:
        return "x86"
    else:
        return "unknown"

# Autodetect GPU Vendor
def detect_gpu_vendor():
    w = wmi.WMI()
    gpus = w.Win32_VideoController()

    for gpu in gpus:
        name = gpu.Name.lower()
        if "nvidia" in name:
            return "Nvidia"
        elif "amd" in name or "radeon" in name:
            return "AMD"
        elif "intel" or "iris" in name:
            return "Intel"

    return "unknown"

# Autoinstall GPU Driver
def handle_gpu_driver_installation(vendor):

    if vendor == "Nvidia":
        print("[INFO] Downloading NVIDIA driver installer...")
        url = "https://us.download.nvidia.com/nvapp/client/11.0.3.232/NVIDIA_app_v11.0.3.232.exe"
        filename = os.path.join("installers", "NVIDIA_app_v11.0.3.232.exe")
        try:
            urllib.request.urlretrieve(url, filename)
            print("[INFO] Running NVIDIA installer...")
        except Exception as e:
            print(f"[ERROR] Failed to download NVIDIA installer: {e}")
            print("[INFO] Please install the drivers manually from the NVIDIA website link below: ")
            print("[LINK] https://us.download.nvidia.com/nvapp/client/11.0.3.232/NVIDIA_app_v11.0.3.232.exe")
            print("[INFO] Press any key to exit.")
            resp = input()
            return
        # Run the installer with subprocess after downloading
        try:
            subprocess.run([filename], check=True)
            print("[OK] NVIDIA driver installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to run NVIDIA installer: {e}")
            print("[INFO] Please install the drivers manually from the NVIDIA website link below: ")
            print("[LINK] https://us.download.nvidia.com/nvapp/client/11.0.3.232/NVIDIA_app_v11.0.3.232.exe")
            print("[INFO] Press any key to exit.")
            resp = input()            
            return
    
    elif vendor == "AMD":
        # Open browser to download AMD drivers cuz autistic micro device don't let me download directly
        print("[INFO] AMD installer can't be downloaded directly. Opening browser...")
        try:
            webbrowser.open("https://www.amd.com/en/support")
        except Exception as e:
            print(f"[ERROR] Failed to open browser for AMD drivers: {e}")
            print("[INFO] Please install the drivers manually from the AMD website link below: ")
            print("[LINK] https://www.amd.com/en/support")
            print("[INFO] Press any key to exit.")
            resp = input()
            return
    elif vendor == "Intel":
        # shIntel don't install drivers, just a SPYWARE to know my components
        print("[INFO] Downloading Intel Support Assistant...")
        url = "https://downloadmirror.intel.com/28425/a08/Intel-Driver-and-Support-Assistant-Installer.exe"
        filename = os.path.join("installers", "Intel-Driver-and-Support-Assistant-Installer.exe")
        try:
            urllib.request.urlretrieve(url, filename)
            print("[INFO] Running Intel Support Assistant installer...")
        except Exception as e:
            print(f"[ERROR] Failed to download Intel Support Assistant: {e}")
            print("[INFO] Please install the drivers manually from the Intel website link below: ")
            print("[LINK] https://downloadmirror.intel.com/28425/a08/Intel-Driver-and-Support-Assistant-Installer.exe")
            print("[INFO] Press any key to exit.")
            resp = input()
            return
        # Run the installer with subprocess after downloading
        try:
            subprocess.run([filename], check=True)
            print("[OK] Intel Support Assistant installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to run Intel Support Assistant installer: {e}")
            print("[INFO] Please install the drivers manually from the Intel website link below: ")
            print("[LINK] https://downloadmirror.intel.com/28425/a08/Intel-Driver-and-Support-Assistant-Installer.exe")
            print("[INFO] Press any key to exit.")
            resp = input()
            return
    elif vendor == "unknown":
        print("[WARNING] Unknown GPU vendor. Please install drivers manually.")
    elif vendor == "":
        print("[WARNING] No GPU detected. Please install drivers manually.")

# Install DirectX (requires proper installation function cuz idk lol, some shitty macrohard idea)
def install_directx(installer_path):
    print("[INFO] Extracting DirectX installer...")
    extract_dir = os.path.join(os.getenv("TEMP"), "directx_temp")
    os.makedirs(extract_dir, exist_ok=True)

    # Extract files
    try:
        subprocess.run([installer_path, "/Q", f"/T:{extract_dir}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to extract DirectX installer: {e}")
        return
    print("[OK] DirectX installer extracted as DXSETUP.exe.")
    # Runs real installer
    dxsetup_path = os.path.join(extract_dir, "DXSETUP.exe")
    if os.path.exists(dxsetup_path):
        print("[INFO] Running DXSETUP...")
        try:
            subprocess.run([dxsetup_path, "/silent"], check=True)
            print("[OK] DirectX installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to run DXSETUP: {e}")
    else:
        print("[ERRO] DXSETUP.exe not found after extraction.")


# Run installers
def run_installers(path, name=""):
    """run installers bypassing via parameters."""
    if not os.path.exists(path):
        print(f"[ERROR] Installer {name} not found in {path}")
        return

    print(f"[INFO] Running {name}...")
    try:
        subprocess.run([path,"/quiet", "/norestart"], check=True)
        print(f"[OK] {name} Succefully installed.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed during installation {name}: {e}")

# main function
def main():
    # Detects OS architecture
    print("[INFO] Detecting OS architecture...")
    arch = detect_arch()
    print(f"[INFO] Detected OS as: {arch}")

    # Detects GPU vendor
    print("[INFO] Detecting GPU vendor...")
    vendor = detect_gpu_vendor()
    print(f"[INFO] GPU Vendor detected: {vendor}")
    
    # Check if user wants to continue
    print("Type [Y] or [Q] to quit.")
    resp = input().lower()
    if resp == "q":
        print("[INFO] User requested to quit.")
        sys.exit(0)
    elif resp != "y":
        print("[INFO] User requested to quit.")
        sys.exit(0)
    elif resp == "y":
        print("[INFO] User requested to continue.")
        # Installs DirectX
        install_directx(INSTALLERS["directx"])

        # Installs .NET Framework
        run_installers(INSTALLERS["dotnet"], ".NET Framework")

        # Installs Visual C++ Redistributable by architecture
        vc_path = INSTALLERS["vc_redist"].get(arch)
        if vc_path:
            run_installers(vc_path, f"Visual C++ ({arch})")
        else:
            print("[WARNING] Unknown architecture for Visual C++.")

        # Installs GPU Driver
        handle_gpu_driver_installation(vendor)

# Admin check function
def run_as_admin():
    # Request admin privileges cuz they think im gonna clone your wallet or install a ransonware
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        print("[INFO] Elevating privileges...")
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
            sys.exit()
        except Exception as e:
            print(f"[ERRO] Failed to request adminitrator privileges: {e}")
            sys.exit(1)

if __name__ == "__main__":
    if not sys.platform.startswith("win"):
        print("This installer only runs on Windows.")
        sys.exit(1)
    if not run_as_admin():
        sys.exit(0)

    main()