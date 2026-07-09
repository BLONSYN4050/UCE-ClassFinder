from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Cargar JSON
def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


# Cargar archivos
aulas = cargar_json("data/aulas.json")
entradas = cargar_json("data/entradas.json")
nodos = cargar_json("data/nodos.json")
print("TOTAL NODOS:", len(nodos))
print("ULTIMO NODO:", list(nodos.keys())[-1])
grafo = cargar_json("data/grafo.json")
destinos = cargar_json("data/destinos.json")


@app.route("/")
def inicio():
    return render_template("index.html", aulas=aulas.keys())


@app.route("/ruta", methods=["POST"])
def ruta():

    destino = request.form.get("destino")

    if destino not in aulas:
        return {
            "ok": False
        }

    return {
        "ok": True,
        "destino": destino,
        "edificio": aulas[destino]["edificio"],
        "piso": aulas[destino]["piso"]
    }


@app.route("/mapa")
def mapa():

    lat = request.args.get("lat", -0.2105)
    lon = request.args.get("lon", -78.4890)
    destino = request.args.get("destino", "")
    print("DESTINO RECIBIDO:", destino)

    return render_template(
        "mapa.html",
        lat=lat,
        lon=lon,
        destino=destino,
        nodos=nodos,
        grafo=grafo,
        destinos=destinos,
        entradas=entradas
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)