'''
系统信息工具
'''


import psutil


def get_system_info():
    '''
    获取系统 CPU、内存和磁盘信息
    '''
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_total = memory.total / (1024 ** 3)
    memory_used = memory.used / (1024 ** 3)

    disk_total = 0
    disk_used = 0

    disk_partitions = psutil.disk_partitions()
    valid_disks = []

    for part in disk_partitions:
        if 'cdrom' in part.opts or part.fstype == '' or part.fstype == 'tmpfs':
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            valid_disks.append({
                'mountpoint': part.mountpoint,
                'total_gb': usage.total / (1024 ** 3),
                'used_gb': usage.used / (1024 ** 3)
            })
        except:
            continue

    if valid_disks != []:
        largest_disk = max(valid_disks, key=lambda x: x['total_gb'])
        disk_total = largest_disk['total_gb']
        disk_used = largest_disk['used_gb']

    return True, 'success', {
        'cpu_percent': cpu_percent,
        'memory_total': memory_total,
        'memory_used': memory_used,
        'disk_total': disk_total,
        'disk_used': disk_used
    }