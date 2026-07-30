import websocket, json, time, datetime

print('\n[EDGEX RADAR] Инициализация WebSocket-соединения с EdgeX...', flush=True)

def on_message(ws, message):
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] [WS-DATA] Сигнал рынка: {message[:120]}...', flush=True)

def on_error(ws, error):
    print(f'[ERROR] Сбой EdgeX WS: {error}', flush=True)

def on_close(ws, close_status_code, close_msg):
    print('[CLOSED] Соединение разорвано. Переподключение через 5 секунд...', flush=True)

def on_open(ws):
    print('[SUCCESS] WebSocket EdgeX подключен! Протокол хеджирования активен.', flush=True)

if __name__ == '__main__':
    while True:
        try:
            ws = websocket.WebSocketApp('wss://ws.edgex.exchange/v1/market',
                                      on_open=on_open,
                                      on_message=on_message,
                                      on_error=on_error,
                                      on_close=on_close)
            ws.run_forever(ping_interval=30, ping_timeout=10)
        except Exception as e:
            time.sleep(5)
