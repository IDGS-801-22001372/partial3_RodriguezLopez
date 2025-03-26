from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
import json

ventas_bp = Blueprint('ventas', __name__)

# Función para calcular el precio
def calcular_precio(tamano, ingredientes, num_pizzas):
    precios = {"chica": 40, "mediana": 80, "grande": 120}
    precio_base = precios.get(tamano, 0)
    precio_ingredientes = len(ingredientes) * 10  # $10 por ingrediente extra
    return (precio_base + precio_ingredientes) * num_pizzas

# Ruta para mostrar y agregar pedidos
@ventas_bp.route("/ventas", methods=["GET", "POST"])
@login_required
def ventas():
    try:
        with open('carrito.txt', 'r', encoding='utf-8') as file:
            data = json.load(file)
            pedidos = data.get('pedidos', [])
            ultimo_id = data.get('ultimo_id', 1)  # Obtener el último ID usado
    except (FileNotFoundError, json.JSONDecodeError):
        pedidos = []
        ultimo_id = 1  # Iniciar el contador de IDs en 1 si no existe el archivo

    if pedidos:
        nombre = pedidos[0]["nombre"]
        direccion = pedidos[0]["direccion"]
        telefono = pedidos[0]["telefono"]
    else:
        nombre = direccion = telefono = ""

    if request.method == "POST":
        nuevo_nombre = request.form.get("nombre")
        nuevo_direccion = request.form.get("direccion")
        nuevo_telefono = request.form.get("telefono")
        tamano = request.form.get("tamano")
        ingredientes = request.form.getlist("ingredientes[]")
        num_pizzas = request.form.get("num_pizzas")

        if not nuevo_nombre:
            nuevo_nombre = nombre
        if not nuevo_direccion:
            nuevo_direccion = direccion
        if not nuevo_telefono:
            nuevo_telefono = telefono

        if not nuevo_nombre or not nuevo_direccion or not nuevo_telefono or not tamano or not num_pizzas:
            flash("Por favor, completa todos los campos", "error")
            return redirect(url_for("ventas.ventas"))

        try:
            num_pizzas = int(num_pizzas)
        except ValueError:
            flash("El número de pizzas debe ser un número entero", "error")
            return redirect(url_for("ventas.ventas"))

        subtotal = calcular_precio(tamano, ingredientes, num_pizzas)

        pedido = {
            "id": ultimo_id,
            "nombre": nuevo_nombre,
            "direccion": nuevo_direccion,
            "telefono": nuevo_telefono,
            "tamano": tamano,
            "ingredientes": ingredientes,
            "num_pizzas": num_pizzas,
            "subtotal": subtotal
        }

        pedidos.append(pedido)
        ultimo_id += 1

        with open('carrito.txt', 'w', encoding='utf-8') as file:
            json.dump({"pedidos": pedidos, "ultimo_id": ultimo_id}, file, ensure_ascii=False, indent=4)

        flash("Pedido agregado correctamente", "success")
        return redirect(url_for("ventas.ventas"))

    return render_template("venta.html", pedidos=pedidos)

# Ruta para eliminar un pedido
@ventas_bp.route("/eliminar_pedido/<int:pedido_id>", methods=["POST"])
@login_required
def eliminar_pedido(pedido_id):
    try:
        with open('carrito.txt', 'r', encoding='utf-8') as file:
            data = json.load(file)
            pedidos = data.get('pedidos', [])
            ultimo_id = data.get('ultimo_id', 1)
    except (FileNotFoundError, json.JSONDecodeError):
        pedidos = []
        ultimo_id = 1

    pedidos = [p for p in pedidos if p["id"] != pedido_id]

    with open('carrito.txt', 'w', encoding='utf-8') as file:
        json.dump({"pedidos": pedidos, "ultimo_id": ultimo_id}, file, ensure_ascii=False, indent=4)

    return redirect(url_for("ventas.ventas"))
