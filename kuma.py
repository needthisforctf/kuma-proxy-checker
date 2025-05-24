from uptime_kuma_api import UptimeKumaApi, ProxyProtocol, MonitorType
from modules.inbounds import from_link
from modules.config import config
import yaml

def add_proxies(api):
    with open(config.PROXIES_YAML, "r") as file:
        yml = yaml.safe_load(file)

    [api.delete_proxy(x['id']) for x in api.get_proxies()]
    for k, proxy_obj in yml['proxies'].items():
        for v in proxy_obj:
            if v['type'] != "meta":
                p_data = from_link(v['in'])
                if p_data['protocol'] == 'socks':
                    v['_kuma_id'] = api.add_proxy(
                        protocol=ProxyProtocol.SOCKS5H,
                        active=True,
                        auth=False,
                        host=p_data['listen'],
                        port=p_data['port'])['id']

    with open(config.PROXIES_YAML, "w") as file:
        yaml.dump(yml, file)


def add_monitor_groups(api):
    [api.delete_monitor(x['id']) for x in api.get_monitors()]
    with open(config.PROXIES_YAML, "r") as file:
        yml = yaml.safe_load(file)

    for k, v in yml['proxies'].items():
        group_obj = api.add_monitor(type=MonitorType.GROUP, name=k)
        if group_obj['msg'] == 'successAdded':
            if '_kuma_groups' not in yml:
                yml['_kuma_groups'] = {}
            yml['_kuma_groups'][k] = group_obj['monitorID']

    with open(config.PROXIES_YAML, "w") as file:
        yaml.dump(yml, file)


def add_monitors(api):
    with open(config.PROXIES_YAML, "r") as file:
        yml = yaml.safe_load(file)

    for link in yml['links']:
        for k, v in yml['proxies'].items():
            for proxy in v:
                api.add_monitor(type=MonitorType.HTTP,
                                url=link,
                                name=f"{proxy['type']} {link.split("://")[1]}",
                                proxyId=proxy['_kuma_id'],
                                parent=yml['_kuma_groups'][k])


if __name__ == "__main__":
    with UptimeKumaApi(config.KUMA_URL, timeout=30.0) as api:
        api.login(config.KUMA_USERNAME, config.KUMA_PASSWORD)
        add_proxies(api)
        add_monitor_groups(api)
        add_monitors(api)
