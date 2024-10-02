import xy
import settings
from xymon import Xymon

def send_report(monitor, server, label, indicator, msg):
    monitor.report(server, label, indicator, msg)
    




