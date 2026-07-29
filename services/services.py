import httpx


class Api:
    @staticmethod
    def listar_moeda():
        requisicao = httpx.get("https://economia.awesomeapi.com.br/json/available")
        moedas = requisicao.json()
        lista_moedas = sorted(moedas.keys())
        return lista_moedas

    def buscar_cotacao(sef, moeda, data):
        ano = data[-4:]
        mes = data[3:5]
        dia = data[:2]
        link = f"https://economia.awesomeapi.com.br/json/daily/{moeda}/?start_date={ano}{mes}{dia}&end_date={ano}{mes}{dia}"
        requisicao_moeda = httpx.get(link)
        requisicao_moeda.raise_for_status()
        cotacao = requisicao_moeda.json()
        valor_moeda = cotacao[0]["bid"]
        return valor_moeda


print(Api.listar_moeda())
