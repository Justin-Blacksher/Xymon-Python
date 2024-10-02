import requests

def get_fortigate_wifi_clients(api_key, fortigate_ip, verify_ssl):
    url = f"https://{fortigate_ip}/api/v2/monitor/wifi/client"
    headers = {'Authorization': f'Bearer {api_key}'}

    response = requests.get(url, headers=headers, verify=verify_ssl)
    print(response)
    return response



