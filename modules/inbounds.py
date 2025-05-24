def _unwrap_socks5(uri, tag="socks5"):
    # {socks4|socks5}://[user[:pass]@][host[:port]]
    # socks5://user:pass@host:port
    # Doesn't support auth (for now)
    host, port = uri[9:].split(":")
    return {
        "listen": host,
        "port": int(port),
        "protocol": "socks",
        "settings": {
            "auth": "noauth",
            "udp": True
        },
        "tag": tag
    }


def from_link(link, tag="socks5"):
    if "socks5://" in link:
        return _unwrap_socks5(link, tag)
