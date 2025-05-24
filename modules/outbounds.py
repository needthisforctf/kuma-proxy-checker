import re
import base64


def splitter(uri, target):
    if "&" in uri.split(target)[1]:
        spx = uri.split(target)[1].split("&")[0]
    elif "#" in uri.split(target)[1]:
        spx = uri.split(target)[1].split("#")[0]
    return spx


def _unwrap_ss(uri, tag="proxy"):
    pattern = r'ss://(.*?)#'
    info = re.search(pattern, uri).group(1)

    base64_part, host_port = info.split('@')
    host, port = host_port.split(':')

    cipher, password = base64.b64decode(base64_part).decode('utf-8').split(":")

    return {
        "tag": tag,
        "protocol": "shadowsocks",
        "mux": {
            "enabled": False,
            "concurrency": -1
        },
        "settings": {
            "servers": [{
                "email": "t@t.tt",
                "method": cipher,
                "password": password,
                "address": host,
                "port": int(port),
                "uot": True
            }]
        }
    }


def _unwrap_reality(uri, tag="proxy"):
    protocol = uri.split("://")[0]
    uid = uri.split("//")[1].split("@")[0]
    address = uri.split("@")[1].split(":")[0]
    destination_port = int(uri.split(address + ":")[1].split("?")[0])
    network = splitter(uri, "type=")
    security = splitter(uri, "security=")
    sni = splitter(uri, "sni=")
    fp = splitter(uri, "fp=")
    pbk = splitter(uri, "pbk=")

    if "sid=" in uri:
        sid = splitter(uri, "sid=")
    else:
        sid = ""

    if "spx=" in uri:
        spx = splitter(uri, "spx=")
    else:
        spx = ""

    if "flow" in uri:
        flow = splitter(uri, "flow=")
    else:
        flow = ""

    data = {
        "tag": tag,
        "protocol": protocol,
        "settings": {
            "vnext": [{
                "address":
                address,
                "port":
                destination_port,
                "users": [{
                    "id": uid,
                    "alterId": 0,
                    "email": "t@t.tt",
                    "security": "auto",
                    "encryption": "none",
                    "flow": flow,
                }],
            }]
        },
        "streamSettings": {
            "network": network,
            "security": security,
            "realitySettings": {
                "serverName": sni,
                "fingerprint": fp,
                "show": False,
                "publicKey": pbk,
                "shortId": sid,
                "spiderX": spx,
            },
        },
        "mux": {
            "enabled": False,
            "concurrency": -1
        },
    }

    if network == "grpc":
        serviceName = ""
        if "serviceName=" in uri:
            serviceName = splitter(uri, "serviceName=")
        new_dict = {
            "grpcSettings": {
                "serviceName": serviceName,
                "multiMode": False,
                "idle_timeout": 60,
                "health_check_timeout": 20,
                "permit_without_stream": False,
                "initial_windows_size": 0,
            }
        }
        data["streamSettings"].update(new_dict)

    return data


def from_link(link, tag):
    if "vless://" in link:
        return _unwrap_reality(link, tag)
    elif "ss://" in link:
        return _unwrap_ss(link, tag)
