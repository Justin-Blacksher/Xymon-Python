import settings
import functions
import psutil
import platform
from datetime import datetime
import xy



def get_system():
    
    uname = platform.uname()
    system = (f"System: {uname.system}")
    node = (f"Node Name: {uname.node}")
    release = (f"Release: {uname.release}")
    version = (f"Version: {uname.version}")
    machine = (f"Machine: {uname.machine}")
    processor = (f"Processor: {uname.processor}")
    return system, node, release, version, machine, processor



def get_disk_information():
    disk_info = []

    # Get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_data = {}
        partition_data['device'] = partition.device
        partition_data['mountpoint'] = partition.mountpoint
        partition_data['fstype'] = partition.fstype

        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            partition_data['total_size'] = partition_usage.total
            partition_data['used'] = partition_usage.used
            partition_data['free'] = partition_usage.free
            partition_data['percentage'] = partition_usage.percent
        except PermissionError:
            # Handle cases where the disk isn't ready
            continue

        disk_info.append(partition_data)

    # Get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    total_read = disk_io.read_bytes
    total_write = disk_io.write_bytes

    return disk_info, total_read, total_write