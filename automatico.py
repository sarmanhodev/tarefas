import schedule
import time
import threading
import requests

def atualizar_dado():
    url = 'https://localhost/atualizar_registro_expirado'
    response = requests.get(url)
    print(response.text)


schedule.every(60).seconds.do(atualizar_dado)
print("\nTarefa funcionou\n")

def iniciar_agendamento():
    while True:
        schedule.run_pending()
        time.sleep(1)


threading.Thread(target=iniciar_agendamento).start()
