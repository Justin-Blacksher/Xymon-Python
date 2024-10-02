import json
import xy
import settings

def process_wifi_clients_data(data_json):
    clients = []
   
    data = json.loads(data_json)

    for result in data['results']:
        ip = result["ip"]
        hostname = result["host"]
        mac = result["mac"]
        signal_level = result["health"]["signal_strength"]["value"]
        signal_severity = result["health"]["signal_strength"]["severity"]
        signal_noise_ratio_level = result["health"]["snr"]["value"]
        signal_noise_ratio_severity = result["health"]["snr"]["severity"]
        signal_band_level = result["health"]["band"]["value"]
        signal_band_severity = result["health"]["band"]["severity"]
        

        # Create a dictionary for each client
        client_info = {
            'ip': ip,
            'hostname': hostname,
            'mac': mac,
            'signal_level': signal_level,
            'signal_severity': signal_severity,
            'noise_level': signal_noise_ratio_level,
            'noise_severity': signal_band_severity,
            'band_level': signal_band_level,
            'band_severity': signal_band_severity
        }
        clients.append(client_info)

    return clients

def signal(client, serv):
    # ----- [ Signal ] -------
    message = "Wi-Fi Client Info:\n\n"
    if client['hostname']:
        s_name = client['hostname']
        message += f"Hostname: {client['hostname']}\n"
        message += f"MAC: {client['mac']}\n"
    else:
        s_name = client['ip']
        message += f"IP: {client['ip']}\n"
        message += f"MAC: {client['mac']}\n"
    if client['signal_severity'] == 'good':
        message += f"Signal Severity: {client['signal_severity']}\n"
        message += f"Signal Level: {client['signal_level']} dBm\n"
        xy.send_report(monitor=serv, server=s_name, label=settings.SIGNALQUALITY, indicator=settings.PASSING, msg=message)
    elif client['signal_severity'] == 'fair':
        message += f"Signal Severity: {client['signal_severity']}\n"
        message += f"Signal Level: {client['signal_level']} dBm\n"
        xy.send_report(monitor=serv, server=s_name, label=settings.SIGNALQUALITY, indicator=settings.WARNING, msg=message)
    elif client['signal_severity'] == 'poor':
        message += f"Signal Severity: {client['signal_severity']}\n"
        message += f"Signal Level: {client['signal_level']} dBm\n"
        xy.send_report(monitor=serv, server=s_name, label=settings.SIGNALQUALITY, indicator=settings.CRITICAL, msg=message)
    # -----------------------


def signaltonoise(client, serv):
    message = "Wi-Fi Client Info:\n\n"
    if client['hostname']:
        s_name = client['hostname']
        message += f"Hostname: {client['hostname']}\n"
        message += f"MAC: {client['mac']}\n"
    else:
        s_name = client['ip']
        message += f"IP: {client['ip']}\n"
        message += f"MAC: {client['mac']}\n"
    # ----- [ Signal to Noise Ratio ] -------
    if client['noise_severity'] == 'good':   
        message += f"Noise Severity: {client['noise_severity']}\n"
        message += f"Noise Level : {client['noise_level']}\n"
        xy.send_report(monitor=serv, server=s_name, label=settings.SNR, indicator=settings.PASSING, msg=message)
    elif client['noise_severity'] == 'fair':
        message += f"Noise Severity: {client['noise_severity']}\n"
        message += f"Noise Level : {client['noise_level']}\n"
        xy.send_report(monitor=serv, server=s_name, label=settings.SNR, indicator=settings.WARNING, msg=message)
    elif client['noise_severity'] == 'poor':
        message += f"Noise Severity: {client['noise_severity']}\n"
        message += f"Noise Level : {client['noise_level']}\n"
        xy.send_report(monitor=serv, server=s_name, label=settings.SNR, indicator=settings.CRITICAL, msg=message) 
    

    # -----------------------
def signalscore(client, serv):
    message = "Wi-Fi Client Info:\n\n"
    if client['hostname']:
        s_name = client['hostname']
        message += f"Hostname: {client['hostname']}\n"
        message += f"MAC: {client['mac']}\n"
    else:
        s_name = client['ip']
        message += f"IP: {client['ip']}\n"
        message += f"MAC: {client['mac']}\n"
    # ------ [ SNR score ] ----------
    if client['signal_level'] + client['noise_level'] > 20:
        message += f"Signal Score: {client['noise_level'] + client['signal_level']}"
        xy.send_report(monitor=serv, server=s_name, label=settings.SCORE, indicator=settings.PASSING, msg=message)
    elif client['signal_level'] + client['noise_level'] < 20 and client['signal_level'] + client['noise_level'] > 0:
        message += f"Signal Score: {client['noise_level'] + client['signal_level']}"
        xy.send_report(monitor=serv, server=s_name, label=settings.SCORE, indicator=settings.WARNING, msg=message)
    elif client['signal_level'] + client['noise_level'] < 0:
        message += f"Signal Score: {client['noise_level'] + client['signal_level']}"
        xy.send_report(monitor=serv, server=s_name, label=settings.SCORE, indicator=settings.CRITICAL, msg=message)

def band(client, serv):
    message = "Wi-Fi Client Info:\n\n"
    if client['hostname']:
        s_name = client['hostname']
        message += f"Hostname: {client['hostname']}\n"
        message += f"MAC: {client['mac']}\n"
    else:
        s_name = client['ip']
        message += f"IP: {client['ip']}\n"
        message += f"MAC: {client['mac']}\n"
     # ----- [ Band ] -------
    if client['band_severity'] == 'good':   
        message += f"Band Severity: {client['band_severity']}\n"
        message += f"Band Frequency: {client['band_level']}\n"
        xy.send_report(monitor=serv, server=s_name, label=settings.BAND, indicator=settings.PASSING, msg=message)
    elif client['band_severity'] == 'fair':   
        message += f"Band Severity: {client['band_severity']}\n"
        message += f"Band Frequency: {client['band_level']}\n"
        xy.send_report(monitor=serv, server=s_name, label=settings.BAND, indicator=settings.WARNING, msg=message)
    if client['band_severity'] == 'poor':   
        message += f"Band Severity: {client['band_severity']}\n"
        message += f"Band Frequency: {client['band_level']}\n"
        xy.send_report(monitor=serv, server=s_name, label=settings.BAND, indicator=settings.CRITICAL, msg=message)   
    # -----------------------

def format_wifi_client_messages(clients, serv):
    
    for client in clients:
        signal(client=client, serv=serv)
        signaltonoise(client=client, serv=serv)
        band(client=client, serv=serv)
        signalscore(client=client, serv=serv)
        
def send_messages(response, serv):
    if response.status_code == 200:
        clients = process_wifi_clients_data(data_json=response.text)
        format_wifi_client_messages(clients=clients, serv=serv)
    else:
        msg = f'{response.status_code} {response.headers} {response.reason}'
        xy.send_report(monitor=serv, server=settings.ALIENWARE, label=settings.WIFI, indicator=settings.WARNING, msg=msg)



