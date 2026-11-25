import json
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BOT_TOKEN = os.environ['BOT_TOKEN']
IA_KEY = os.environ['IA_KEY']
IA_MODEL = os.environ['IA_MODEL']
IA_URL = os.environ['IA_URL'].rstrip('/')
ALLOWED = os.environ.get('ALLOWED_CHAT_ID', '')
RSS_URL = os.environ.get('RSS_URL', 'https://techcrunch.com/category/artificial-intelligence/feed/')
MONITOR_URL = os.environ.get('MONITOR_URL', '')
STATE = Path.home() / 'central-ia' / 'site-estado.txt'


def request(url, payload=None, key=None, timeout=45):
    headers = {'User-Agent': 'BTV-Central-IA/1.0'}
    if key:
        headers['Authorization'] = 'Bearer ' + key
    data = None
    if payload is not None:
        headers['Content-Type'] = 'application/json'
        data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.load(response)


def telegram(method, payload):
    result = request('https://api.telegram.org/bot' + BOT_TOKEN + '/' + method, payload)
    if not result.get('ok'):
        raise RuntimeError('Falha na API do Telegram')
    return result['result']


def enviar(chat_id, texto):
    for start in range(0, len(texto), 3500):
        telegram('sendMessage', {'chat_id': chat_id, 'text': texto[start:start+3500]})


def ia(pergunta):
    result = request(IA_URL + '/chat/completions', {
        'model': IA_MODEL,
        'messages': [{'role': 'user', 'content': pergunta}],
        'stream': False,
    }, key=IA_KEY, timeout=90)
    return result['choices'][0]['message']['content']


def bot():
    offset = 0
    while True:
        try:
            updates = telegram('getUpdates', {
                'offset': offset, 'timeout': 25, 'allowed_updates': ['message']
            })
            for update in updates:
                offset = update['update_id'] + 1
                msg = update.get('message', {})
                chat = msg.get('chat', {})
                if chat.get('type') != 'private':
                    continue
                chat_id = str(chat['id'])
                texto = msg.get('text', '').strip()
                if texto == '/id' and (not ALLOWED or chat_id == ALLOWED):
                    enviar(chat_id, 'Seu chat_id: ' + chat_id)
                    continue
                if not ALLOWED or chat_id != ALLOWED:
                    continue
                if texto.startswith('/ia '):
                    try:
                        enviar(chat_id, ia(texto[4:]))
                    except Exception:
                        enviar(chat_id, 'Falha ao consultar o New API.')
                elif texto == '/status':
                    try:
                        request(IA_URL + '/models', key=IA_KEY)
                        enviar(chat_id, 'New API acessível. Use /ia para testar o modelo.')
                    except Exception:
                        enviar(chat_id, 'Não consegui acessar o New API.')
                else:
                    enviar(chat_id, 'Comandos: /id, /status, /ia sua pergunta')
        except Exception:
            print('Falha temporária; nova tentativa em 5 segundos.', flush=True)
            time.sleep(5)


def resumo():
    if not ALLOWED:
        raise RuntimeError('Configure ALLOWED_CHAT_ID')
    req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'BTV-Central-IA/1.0'})
    with urllib.request.urlopen(req, timeout=30) as response:
        xml = ET.fromstring(response.read(2_000_000))
    manchetes = '\n'.join(
        (item.findtext('title') or '') + ' — ' + (item.findtext('link') or '')
        for item in xml.findall('./channel/item')[:5]
    )
    if not manchetes.strip():
        enviar(ALLOWED, 'Nenhuma manchete encontrada.')
        return
    try:
        texto = ia('Resuma em português somente os títulos a seguir, sem inventar detalhes:\n' + manchetes)
    except Exception:
        texto = 'Modelo indisponível.'
    enviar(ALLOWED, 'Resumo de manchetes RSS:\n' + texto + '\n\nFontes:\n' + manchetes)


def site():
    if not ALLOWED or not MONITOR_URL:
        raise RuntimeError('Configure ALLOWED_CHAT_ID e MONITOR_URL')
    try:
        req = urllib.request.Request(MONITOR_URL, headers={'User-Agent': 'BTV-Central-IA/1.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            estado = 'acessível' if response.status < 400 else 'falha HTTP'
    except Exception:
        estado = 'falha de acesso'
    anterior = STATE.read_text().strip() if STATE.exists() else ''
    if estado != anterior:
        enviar(ALLOWED, 'Monitor: ' + MONITOR_URL + ' — ' + estado)
        STATE.write_text(estado)


if __name__ == '__main__':
    modos = {'bot': bot, 'resumo': resumo, 'site': site}
    if len(sys.argv) != 2 or sys.argv[1] not in modos:
        sys.exit('Uso: bot | resumo | site')
    modos[sys.argv[1]]()
