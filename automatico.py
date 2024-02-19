import schedule
import time
import requests


def atualizar_dado():
    response = requests.get('http://localhost:5000/atualizar_registro_expirado')
    print(response.text)

# Agende a execução a cada 24 horas
schedule.every(24).hours.do(atualizar_dado)

while True:
    schedule.run_pending()
    time.sleep(1)