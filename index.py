from bs4 import BeautifulSoup
import concurrent.futures
import random
import requests
import string
import os
import time

class Gerador:
    @staticmethod
    def gerar_codigo_aleatorio(tamanho=16):
        caracteres = string.ascii_letters + string.digits
        codigo = ''.join(random.choices(caracteres, k=tamanho))
        return codigo

def verificar_codigo_presente(url):
    try:
        with requests.Session() as session:
            response = session.get(url, timeout=5)
            response.raise_for_status()  
            html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        if "Código de presente inválido" in soup.text:
            with open("chker.txt", "w") as ok:
                ok.write(f"Código de presente válido: {url}\n")
            return "\033[38;2;0;255;0m" + f"Código de presente válido encontrado no site. {url}" + "\033[0m"
            time.sleep(5)
        else:
            return "\033[38;2;255;0;0m" + f"Código de presente inválido. {url}" + "\033[0m"
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar o site: {e}"
        time.sleep(2)

def processar_codigo(_):
    while True:
        gerador = Gerador()
        codigo = gerador.gerar_codigo_aleatorio()
        url = f"http://discord.gift/{codigo}"
        resultado = verificar_codigo_presente(url)
        os.system("cls")
        print(resultado)

if __name__ == "__main__":
    num_threads = 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(processar_codigo, range(num_threads))
