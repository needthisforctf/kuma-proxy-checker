from uptime_kuma_api import UptimeKumaApi, ProxyProtocol, MonitorType
from modules.inbounds import from_link
from modules.config import config
from utils import dicttools
import yaml


def amend_proxies(api, yml):
    existing_full = api.get_proxies()
    existing = dicttools.trim_keys(
        existing_full,
        # important keys
        ["protocol", "active", "auth", "host", "port"],
    )

    for proxy_obj in yml["proxies"].values():
        for v in proxy_obj:
            p_data = from_link(v["in"])
            if p_data["protocol"] == "socks":
                planned = {
                    "protocol": ProxyProtocol.SOCKS5H,
                    "active": True,
                    "auth": False,
                    "host": p_data["listen"],
                    "port": p_data["port"],
                }
                try:  # to search it
                    v["_kuma_proxy"] = existing_full[existing.index(planned)]["id"]
                except ValueError:
                    v["_kuma_proxy"] = api.add_proxy(**planned)["id"]

    return yml


def amend_monitor_groups(api, yml):
    existing_full = [x for x in api.get_monitors() if x["type"] == MonitorType.GROUP]
    existing = dicttools.trim_keys(
        existing_full,
        ["type", "name"],  # important keys
    )

    if "_kuma_group" not in yml:
        yml["_kuma_group"] = {}
    for k, v in yml["proxies"].items():
        planned = {"type": MonitorType.GROUP, "name": k}
        try:  # to search it
            yml["_kuma_group"][k] = existing_full[existing.index(planned)]["id"]
        except ValueError:
            group_obj = api.add_monitor(**planned)
            if group_obj["msg"] == "successAdded":
                yml["_kuma_group"][k] = group_obj["monitorID"]
    return yml


def amend_monitors(api, yml):
    existing = dicttools.trim_keys(
        [x for x in api.get_monitors() if x["type"] != MonitorType.GROUP],
        ["type", "url", "name", "proxyId", "parent"],  # important keys
    )

    for link in yml["links"]:
        for k, v in yml["proxies"].items():
            for proxy in v:
                planned = {
                    "type": MonitorType.HTTP,
                    "url": link,
                    "name": f"{proxy['type']} {link.split('://')[1]}",
                    "proxyId": proxy["_kuma_proxy"],
                    "parent": yml["_kuma_group"][k],
                }
                if planned not in existing:
                    proxy.setdefault("_kuma_monitors", []).append(
                        api.add_monitor(**planned)["monitorId"]
                    )
    return yml


def add_statuspages(api, yml):
    pgrouplist = []
    for index, (country, value) in enumerate(yml["proxies"].items()):
        pgrouplist.append(
            {
                "id": index,
                "monitorList": [],
                "name": country,
                "weight": index,
            }
        )
        for proxy in value:
            for m_id in proxy["_kuma_monitors"]:
                mon = api.get_monitor(m_id)
                pgrouplist[-1]["monitorList"].append(
                    {
                        "id": m_id,
                        "name": mon["name"],
                        "sendUrl": False,
                        "type": str(mon["type"]),
                    }
                )
    api.add_status_page


if __name__ == "__main__":
    with UptimeKumaApi(config.KUMA_URL, timeout=30.0) as api:
        api.login(config.KUMA_USERNAME, config.KUMA_PASSWORD)
        with open(config.PROXIES_YAML, "r") as file:
            yml = yaml.safe_load(file)
        yml = amend_proxies(api, yml)
        yml = amend_monitor_groups(api, yml)
        amend_monitors(api, yml)
