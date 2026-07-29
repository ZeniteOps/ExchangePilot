import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from services.services import Api
import pandas as pd
import httpx
from datetime import datetime, date
import numpy as np

api = Api()

lista_moedas = list(Api.listar_moeda())


def pegar_cotacao():
    moeda = combobox_selecionarmoeda.get()
    data = calendario_moeda.get()
    valor = api.buscar_cotacao(moeda, data)
    label_textocotacao["text"] = f"A cotação {moeda} na data {data} foi de {valor}"


def selecionar_arquivo():
    caminho_arquivo = askopenfilename(title="Selecione o Arquivo de Moeda")
    var_caminhoarquivo.set(caminho_arquivo)
    if caminho_arquivo:
        label_arquivoselecionado["text"] = f"Arquivo Selecionado: {caminho_arquivo}"


def atualizar_cotacoes():
    try:
        df = pd.read_excel(var_caminhoarquivo.get())
        moedas = df.iloc[:, 0]
        data_final = date.today()
        data_inicial = calendario_datainicial.get_date()
        if data_inicial > data_final:
            raise ValueError("A data final não pode ser menor que a data inicial")
        numero_dias = abs(data_inicial - data_final).days + 1

        for moeda in moedas:
            link = (
                f"https://economia.awesomeapi.com.br/json/daily/{moeda}/{numero_dias}"
            )
            requisicao_moeda = httpx.get(link)
            requisicao_moeda.raise_for_status()
            cotacoes = requisicao_moeda.json()
            for cotacao in cotacoes:
                timestamp = int(cotacao["timestamp"])
                bid = float(cotacao["bid"])
                data = datetime.fromtimestamp(timestamp)
                data = data.strftime("%d/%m/%Y")
                if data not in df:
                    df[data] = np.nan

                df.loc[df.iloc[:, 0] == moeda, data] = bid
        print(cotacoes)
        df.to_excel(r"dataset/teste.xlsx")
        label_atualizarcotacoes["text"] = "Arquivo Atualizado com Sucesso"
    except Exception as e:
        label_atualizarcotacoes["text"] = (
            "Selecione um arquivo excel no formato correto"
        )
        print(e)


janela = tk.Tk()

janela.title("Ferramenta de Cotação de Moedas")

label_cotacao_moeda = tk.Label(
    text="Cotação de uma moeda especifica", borderwidth=2, relief=tk.SOLID
)
label_cotacao_moeda.grid(row=0, column=0, padx=10, pady=10, sticky="nswe", columnspan=3)

label_selecionarmoeda = tk.Label(text="Selecionar Moeda", anchor="e")
label_selecionarmoeda.grid(
    row=1, column=0, padx=10, pady=10, sticky="nswe", columnspan=2
)

combobox_selecionarmoeda = ttk.Combobox(values=lista_moedas)
combobox_selecionarmoeda.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

label_selecionardia = tk.Label(
    text="Selecione o dia que deseja pegar a cotação", anchor="e"
)
label_selecionardia.grid(row=2, column=0, padx=10, pady=10, sticky="nswe", columnspan=2)

calendario_moeda = DateEntry(year=2026, locale="pt_br")
calendario_moeda.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

label_textocotacao = tk.Label(text="")
label_textocotacao.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

botao_pegarcotacao = tk.Button(text="Pegar Cotação", command=pegar_cotacao)
botao_pegarcotacao.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

# Cotação varias moedas

label_cotacao_variasmoedas = tk.Label(
    text="Cotação de Multiplas Moedas", borderwidth=2, relief=tk.SOLID
)
label_cotacao_variasmoedas.grid(
    row=4, column=0, padx=10, pady=10, sticky="nswe", columnspan=3
)

var_caminhoarquivo = tk.StringVar()

label_selecionararquivo = tk.Label(
    text="Selecione um arquivo em Excel com as moedas na Coluna A"
)
label_selecionararquivo.grid(
    row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
)

botao_selecionar_arquivo = tk.Button(
    text="Clique aqui para selecionar", command=selecionar_arquivo
)
botao_selecionar_arquivo.grid(row=5, column=2, padx=10, pady=10, sticky="nsew")

label_arquivoselecionado = tk.Label(text="Nenhum Arquivo Selecionado", anchor="e")
label_arquivoselecionado.grid(
    row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew"
)

label_datafinal = tk.Label(text="Data Final", anchor="e")
label_datainicial = tk.Label(text="Data Inicial", anchor="e")
label_datafinal.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")
label_datainicial.grid(row=8, column=0, padx=10, pady=10, sticky="nsew")

calendario_datafinal = tk.Label(text=date.today().strftime("%d/%m/%Y"))
calendario_datainicial = DateEntry(year=2026, lacale="pt_br")
calendario_datafinal.grid(row=7, column=1, padx=10, pady=10, sticky="nsew")
calendario_datainicial.grid(row=8, column=1, padx=10, pady=10, sticky="nsew")

botao_atualizarcotacoes = tk.Button(
    text="Atualizar Cotações", command=atualizar_cotacoes
)
botao_atualizarcotacoes.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")


label_atualizarcotacoes = tk.Label(text="")
label_atualizarcotacoes.grid(
    row=9, column=1, columnspan=2, padx=10, pady=10, sticky="nsew"
)

botao_fechar = tk.Button(text="Fechar", command=janela.quit)
botao_fechar.grid(row=10, column=2, padx=10, pady=10, sticky="nsew")

janela.mainloop()
