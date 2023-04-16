from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)


@app.route('/alterar/pte', methods=["GET", "POST"])
def ficha():
    informacoes = request.get_json()
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    personagem = informacoes["personagem"]

    requisicao_dict_pte = requests.get(f'{bd}/personagens/{personagem}/.json')
    dict_pte = requisicao_dict_pte.json()

    val_diminuir_pv, val_diminuir_pe, val_diminuir_sn = informacoes["pv"], informacoes["pe"], informacoes["sn"]

    if abs(val_diminuir_pv) > dict_pte["pv"]["maximo"]:
        if val_diminuir_pv < 0:
            val_diminuir_pv = dict_pte["pv"]["maximo"]*-1
        else:
            val_diminuir_pv = dict_pte["pv"]["maximo"]

    if abs(val_diminuir_pe) > dict_pte["pe"]["maximo"]:
        if val_diminuir_pe < 0:
            val_diminuir_pe = dict_pte["pe"]["maximo"]*-1
        else:
            val_diminuir_pe = dict_pte["pe"]["maximo"]

    if abs(val_diminuir_sn) > dict_pte["sn"]["maximo"]:
        if val_diminuir_sn < 0:
            val_diminuir_sn = dict_pte["sn"]["maximo"]*-1
        else:
            val_diminuir_sn = dict_pte["sn"]["maximo"]

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


@app.route("/receber/<string:personagem>", methods=["GET"])
def retorna_dados(personagem):
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    print(personagem)
    requisita_dados_personagem = requests.get(f"{bd}/personagens/{personagem}/.json")
    dados_personagem = requisita_dados_personagem.json()

    return jsonify(dados_personagem)


@app.route("/alterar/anotacoes", methods=["POST"])
def salva_anotacoes():
    informacoes = request.get_json()
    personagem = informacoes["personagem"]
    anotacoes = informacoes["anotações"]

    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    dados = {"anotações": anotacoes}
    requisicao = requests.patch(f"{bd}/personagens/{personagem}/.json", data=json.dumps(dados))

    return jsonify(requisicao.json())


@app.route("/alterar/atributos", methods=["POST"])
def altera_atributos():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    agilidade = informacoes["agi"]
    forca = informacoes["for"]
    intelecto = informacoes["int"]
    presenca = informacoes["pre"]
    vigor = informacoes["vig"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}/atributos"

    dados = {"agi": agilidade, "for": forca, "int": intelecto, "pre": presenca, "vig": vigor,}

    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/classe", methods=["POST"])
def altera_classe():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    classe = informacoes["classe"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"classe": classe}
    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/defesa", methods=["POST"])
def altera_defesa():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    defesa = informacoes["defesa"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"defesa": defesa}
    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/inventario", methods=["POST"])
def altera_inventario():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    inventario = informacoes["inventario"]
    dados = {"inventario": inventario}

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    requisicao_inventario_anterior = requests.get(f"{bd}/inventario/.json")
    inventario_anterior = requisicao_inventario_anterior.json()

    for item in inventario_anterior:
        if item not in dados["inventario"]:
            dados["inventario"][item] = inventario_anterior[item]

    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/nex", methods=["POST"])
def altera_nex():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    nex = informacoes["nex"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"nex": nex}
    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/origem", methods=["POST"])
def altera_origem():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    origem = informacoes["origem"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"origem": origem}
    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/pericias", methods=["POST"])
def altera_pericias():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    pericias = informacoes["pericias"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"pericias": pericias}

    requisicao_pericias_anterior = requests.get(f"{bd}/pericias/.json")
    pericias_anterior = requisicao_pericias_anterior.json()

    for item in pericias_anterior:
        if item not in dados["pericias"]:
            dados["pericias"][item] = pericias_anterior[item]

    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/poderes", methods=["POST"])
def altera_poderes():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    poderes = informacoes["poderes"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"poderes": poderes}

    requisicao_poderes_anterior = requests.get(f"{bd}/poderes/.json")
    poderes_anterior = requisicao_poderes_anterior.json()

    for item in poderes_anterior:
        if item not in dados["poderes"]:
            dados["poderes"][item] = poderes_anterior[item]

    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/rituais", methods=["POST"])
def altera_rituais():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    rituais = informacoes["rituais"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"rituais": rituais}

    requisicao_rituais_anterior = requests.get(f"{bd}/rituais/.json")
    rituais_anterior = requisicao_rituais_anterior.json()

    for item in rituais_anterior:
        if item not in dados["rituais"]:
            dados["rituais"][item] = rituais_anterior[item]

    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/trilha", methods=["POST"])
def altera_trilha():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    trilha = informacoes["trilha"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"trilha": trilha}
    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.after_request
def add_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    # response.headers.add("Access-Control-Allow-Methods", "POST, GET")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')

    return response


if __name__ == "__main__":
    app.run()
