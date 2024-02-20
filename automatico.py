import schedule
import time
import threading
import requests

def atualizar_dado():
    url = 'https://lista-tarefas-uvq7.onrender.com//atualizar_registro_expirado'
    response = requests.get(url)
    print(response.text)

# Agende a execução a cada 4 horas (ajuste conforme necessário)
schedule.every(2).minutes.do(atualizar_dado)

# Função para iniciar o agendamento em uma thread separada
def iniciar_agendamento():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Inicie o agendamento em uma thread separada
threading.Thread(target=iniciar_agendamento).start()
