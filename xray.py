from modules import inbounds, outbounds, routing
from modules.config import config
import yaml
import json
import copy

BLANK = {
    "log": {
        "loglevel": "none"
    },
    "routing": {
        "domainStrategy":
        "AsIs",
        "rules": [{
            "type": "field",
            "ip": ["geoip:private"],
            "outboundTag": "block"
        }]
    },
    "inbounds": [],
    "outbounds": [{
        "protocol": "blackhole",
        "tag": "block"
    }]
}


def gen_config():
    blank = copy.deepcopy(BLANK)
    with open(config.PROXIES_YAML, "r") as file:
        yml = yaml.safe_load(file)

    for country, proxies in yml['proxies'].items():
        print(f"Current country: {country}")
        for proxy in proxies:
            tag_in = f"{country}-{proxy['type']}-in"
            tag_out = f"{country}-{proxy['type']}-out"

            blank['inbounds'].append(inbounds.from_link(proxy['in'], tag_in))
            blank['outbounds'].append(
                outbounds.from_link(proxy['out'], tag_out))
            blank['routing']['rules'].append(routing.route(tag_in, tag_out))

    return blank


if __name__ == "__main__":
    with open(config.JSON_OUT, "w") as file:
        json.dump(gen_config(), file, indent=4)
