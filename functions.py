import settings
import xy
import systeminfo
import scrape
import fortiapi
import fortigate



def server():
    mon = xy.Xymon(settings.XYMON_SERVER, settings.XYMON_PORT)
    return mon

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def system(serv):
    system, node, release, version, machine, processor  = systeminfo.get_system()
    msg = f'''
{system}
{node}
{release}
{version}
{machine}
{processor}
'''
    #xy.send_report(monitor=serv, server=settings.ALIENWARE, label=settings.SYSTEMINFO, indicator=settings.PASSING, msg=msg)
    


def disk_usage(serv):
    disk_info, total_read, total_write = systeminfo.get_disk_information()
    msg = f'''
Disk Information: 
-   Device     : {disk_info[0]['device']}
-   MNT Point  : {disk_info[0]['mountpoint']}
-   Filesystem : {disk_info[0]['fstype']}
-   Total Size : {get_size(bytes=disk_info[0]['total_size'])}
-   Used       : {get_size(bytes=disk_info[0]['used'])}
-   Free       : {get_size(bytes=disk_info[0]['free'])}
-   Percentage : {get_size(bytes=disk_info[0]['percentage'])}
Total Read:       {get_size(bytes=total_read)}
Total Write:      {get_size(bytes=total_write)}
'''
    #xy.send_report(monitor=serv, server=settings.ALIENWARE, label=settings.DISKUSAGE, indicator=settings.PASSING, msg=msg)


def get_wifi_clients(serv):
    response = fortiapi.get_fortigate_wifi_clients(fortigate_ip=settings.FORTIGATE_IP, api_key=settings.APIKEY, verify_ssl=settings.VERIFY)
    fortigate.send_messages(response=response, serv=serv)