# github:mbrell

import platform
import os
import psutil
import socket
import json
import uuid
import netifaces
import subprocess
import time
from datetime import datetime
from uptime import uptime

def get_os_info():
    try:
        import distro
        distro_name = distro.name()
        distro_version = distro.version()
    except ImportError:
        distro_name = platform.system()
        distro_version = platform.version()

    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform-release": platform.release(),
        "platform-version": distro_version,
        "architecture": platform.machine(),
        "kernel": platform.uname().release,
        "distro": distro_name,
        "uptime": f"{uptime():.2f} seconds",
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
    }

def get_cpu_info():
    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency_mhz": psutil.cpu_freq().max,
        "min_frequency_mhz": psutil.cpu_freq().min,
        "current_frequency_mhz": psutil.cpu_freq().current,
        "cpu_usage_per_core": psutil.cpu_percent(percpu=True),
        "total_cpu_usage": psutil.cpu_percent()
    }

def get_memory_info():
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "total_ram": svmem.total,
        "available_ram": svmem.available,
        "used_ram": svmem.used,
        "ram_percent": svmem.percent,
        "total_swap": swap.total,
        "used_swap": swap.used,
        "swap_percent": swap.percent
    }

def get_disk_info():
    partitions = psutil.disk_partitions()
    disks = []
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
        except PermissionError:
            continue
        disks.append({
            "device": p.device,
            "mountpoint": p.mountpoint,
            "fstype": p.fstype,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent
        })
    return disks

def get_network_info():
    interfaces = netifaces.interfaces()
    net_data = {}

    for interface in interfaces:
        iface_data = {}
        addrs = netifaces.ifaddresses(interface)

        iface_data["mac"] = addrs.get(netifaces.AF_LINK, [{}])[0].get('addr', '')
        iface_data["ipv4"] = addrs.get(netifaces.AF_INET, [{}])[0].get('addr', '')
        iface_data["ipv6"] = addrs.get(netifaces.AF_INET6, [{}])[0].get('addr', '')

        net_data[interface] = iface_data

    gateways = netifaces.gateways()
    net_data["default_gateway"] = gateways.get('default', {}).get(netifaces.AF_INET, [None])[0]

    return net_data

def get_user_info():
    return {
        "current_user": os.getlogin(),
        "uid": os.getuid(),
        "gid": os.getgid(),
        "home": os.path.expanduser("~"),
        "shell": os.environ.get("SHELL", "")
    }

def get_system_load():
    load1, load5, load15 = os.getloadavg()
    return {
        "load_1min": load1,
        "load_5min": load5,
        "load_15min": load15,
        "process_count": len(psutil.pids())
    }

def get_serial_number():
    try:
        output = subprocess.check_output("sudo dmidecode -s system-serial-number", shell=True, stderr=subprocess.DEVNULL)
        return output.decode().strip()
    except Exception:
        return "Unknown or requires sudo"

def get_installed_packages():
    try:
        output = subprocess.check_output("dpkg -l", shell=True, stderr=subprocess.DEVNULL)
        return output.decode(errors="ignore").splitlines()[5:]
    except Exception:
        return ["Could not retrieve package list"]

def get_time_info():
    return {
        "system_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": time.tzname
    }

def collect_system_info():
    data = {
        "os_info": get_os_info(),
        "cpu_info": get_cpu_info(),
        "memory_info": get_memory_info(),
        "disk_info": get_disk_info(),
        "network_info": get_network_info(),
        "user_info": get_user_info(),
        "load_info": get_system_load(),
        "serial_number": get_serial_number(),
        "time_info": get_time_info(),
        "installed_packages": get_installed_packages()
    }
    return data

def export_to_json(data, filename="system_profile.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    print("Collecting system info..")
    info = collect_system_info()
    export_to_json(info)
    print("System profile exported to system_profile.json!")
