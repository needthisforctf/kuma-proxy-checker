# kuma-proxy-checker

Программа состоит из двух ключевых компонентов:
- Конфигуратор XRAY: xray.py
- Конфигуратор Kuma: kuma.py

Компоненты независимы друг от друга и могут быть использованы отдельно. Xray служит для того, чтобы можно было подключаться к vless и ss ссылкам и получать локальный socks, через который можно на соотв. vless и ss ходить. 

Как это работает: в .env файле (пример в репозитории есть, .env.example) нужно указать путь к исходному YAML и итоговому xray_config. xray.py читает этот YAML и выдаёт JSON, пригодный для употребления Xray. 

YAML выглядит вот так:

```yaml
# Всё, что начинается на _kuma можно игонрировать
# Это служебные ключи, которые создаёт kuma.py

_kuma_groups:
  England: 105
  Finland: 106
  France: 107
  Germany: 108
  GermanyFast: 112
  HongKong: 109
  India: 110
  Kazakhstan: 111
  Latvia: 112
  Netherlands: 113
  Poland: 114
  Russia: 115
  Singapore: 116
  TikTok: 117
  Turkey: 118
  USA: 119
  Youtube: 120

# Если вам нужен только Xray, этот ключ можно пропустить целиком
links: # список со ссылками на проверку
- http://cp.cloudflare.com # Каждая ссылка проверяется всеми прокси ниже

# Обязательный ключ для Xray и Kuma
proxies: 
  England: # название может быть произвольной валидной для YAML строкой
  - _kuma_id: 101
    _kuma_monitor_id: 506
    _kuma_proxy_id: 263
    # можно подключиться на 20016 порт localhost (127.0.0.1) и вас прокинет
    # на vless-ссылку в out
    in: socks5://127.0.0.1:20016 
    out: vless://9c6036bb-4627-4abd-9c67-12360e2c2fe8@example.com:443?security=reality&type=tcp&headerType=&flow=xtls-rprx-vision&path=&host=&sni=example.com&fp=chrome&pbk=0000jIOQnvRQ73iap9635ILHVigZ_Ikavz9nN56lc&sid=1c27e2d6b4dafc7f#England%E2%9C%A8%20%F0%9F%87%AC%F0%9F%87%A7%20-%5BVLESS%5D-%5B7663484207%5D
    type: reality # для Vless используется reality, для ss — shadowsocks
  - _kuma_id: 102
    _kuma_monitor_id: 507
    _kuma_proxy_id: 264
     # если ваш софт не выходит на локалхост
     # (например, в докер-сети)
     # можно также слушать на айпи
    in: socks5://192.168.18.10:30001 # комбинация ip-port должна быть уникальна в файле
    out: ss://Y2hhYztgcytAtaWV0Zi1wb2x5MTMwNTpkOWU1NDJkN2EzMWI0ZmQx@example.com:57456#
    type: shadowsocks
```
