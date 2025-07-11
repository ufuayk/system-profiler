# System Profiler

A tool for collecting detailed system information on Linux systems.

## Installation

```bash
git clone https://github.com/mbrell/system-profiler
```

```bash
cd system-profiler
```

```bash
pip install -r requirements.txt
```

```bash
python3 main.py
```

The script saves all system information to `system_profile.json` in the current directory.

## Empty Profile

```json
{
    "os_info": {
        "hostname": "",
        "platform": "",
        "platform-release": "",
        "platform-version": "",
        "architecture": "",
        "kernel": "",
        "distro": "",
        "uptime": "",
        "boot_time": ""
    },
    "cpu_info": {
        "physical_cores": 0,
        "total_cores": 0,
        "max_frequency_mhz": 0.0,
        "min_frequency_mhz": 0.0,
        "current_frequency_mhz": 0.0,
        "cpu_usage_per_core": [],
        "total_cpu_usage": 0.0
    },
    "memory_info": {
        "total_ram": 0,
        "available_ram": 0,
        "used_ram": 0,
        "ram_percent": 0.0,
        "total_swap": 0,
        "used_swap": 0,
        "swap_percent": 0.0
    },
    "disk_info": [
        {
            "device": "",
            "mountpoint": "",
            "fstype": "",
            "total": 0,
            "used": 0,
            "free": 0,
            "percent": 0.0
        }
    ],
    "network_info": {
        "eth0": {
            "mac": "",
            "ipv4": "",
            "ipv6": ""
        },
        "default_gateway": ""
    },
    "user_info": {
        "current_user": "",
        "uid": 0,
        "gid": 0,
        "home": "",
        "shell": ""
    },
    "load_info": {
        "load_1min": 0.0,
        "load_5min": 0.0,
        "load_15min": 0.0,
        "process_count": 0
    },
    "serial_number": "",
    "time_info": {
        "system_time": "",
        "timezone": ["", ""]
    },
    "installed_packages": []
}
```

## Note

Some functions (etc: the serial number) may require root.
