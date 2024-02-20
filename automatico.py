import schedule
import time
import requests


def atualizar_dado():
    response = requests.get('https://lista-tarefas-uvq7.onrender.com/atualizar_registro_expirado')
    print(response.text)

# Agende a execução a cada 24 horas
schedule.every(2).hours.do(atualizar_dado)

while True:
    schedule.run_pending()
    time.sleep(1)
