from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)


@app.route('/api_valor_pte', methods=["POST"])
def ficha():
    informacoes = request.get_json()
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    personagem = informacoes["personagem"]

    requisicao_dict_pte = requests.get(f'{bd}/personagens/{personagem}/.json')
    dict_pte = requisicao_dict_pte.json()

    val_diminuir_pv, val_diminuir_pe, val_diminuir_sn = informacoes["pv"], informacoes["pe"], informacoes["sn"]
    val_atual_pv, val_atual_pe, val_atual_sn = dict_pte["pv"]["atual"], dict_pte["pe"]["atual"], dict_pte["sn"]["atual"]

    val_final_pv = val_atual_pv - val_diminuir_pv
    val_final_pe = val_atual_pe - val_diminuir_pe
    val_final_sn = val_atual_sn - val_diminuir_sn

    dados_pv = {"atual": val_final_pv}
    requests.patch(f"{bd}/personagens/{personagem}/pv/.json", data=json.dumps(dados_pv))

    dados_pe = {"atual": val_final_pe}
    requests.patch(f"{bd}/personagens/{personagem}/pe/.json", data=json.dumps(dados_pe))

    dados_sn = {"atual": val_final_sn}
    requests.patch(f"{bd}/personagens/{personagem}/sn/.json", data=json.dumps(dados_sn))

    return jsonify({"personagem": personagem, "pv": val_final_pv, "pe": val_final_pe, "sn": val_final_sn})


@app.route("/api_retorna_dados/<string:personagem>", methods=["GET"])
def retorna_dados(personagem):
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    requisita_dados_personagem = requests.get(f"{bd}/personagens/{personagem}/.json")
    dados_personagem = requisita_dados_personagem.json()

    return jsonify(dados_personagem)

@app.after_request
def add_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "")
    response.headers.add(
        "Access-Control_Allow-Headers",
        "Content-Type, Authorization")

    return response


if __name__ == "__main__":
    app.run()
