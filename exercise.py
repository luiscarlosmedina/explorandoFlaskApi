from flask import Flask, jsonify, request

app = Flask(__name__) #se crea la aplicacion

from products import products

# reviso que el servidor funcione
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

# optengo el listado de productos registrados
@app.route('/products')
def getProducts():
    # con jsonify retorno un Json en este caso de productos
    return jsonify({'products': products})


# me trae el producto especifico que este escrito en la ruta
@app.route('/products/<string:product_name>')
def getProduct(product_name):
    productsFound = [
        #recorro el listado de productos, y lo comparo con lo que inserto el usuario en minuscula, si no lo encuentra me genera error
        product for product in products if product['name'] == product_name.lower()]
    if (len(productsFound) > 0):
        return jsonify({'product': productsFound[0]})
    return jsonify({'message': 'Product Not found'})

# Creacion de un producto
@app.route('/products', methods=['POST'])
def addProduct():
    # con request envio en formato Json nuevos productos
    new_product = {
        'name': request.json['name'],
        'price': request.json['price'],
        'quantity': 10
    }
    products.append(new_product)
    return jsonify({'products': products})

# Actualizar productos existentes con metodo PUT
@app.route('/products/<string:product_name>', methods=['PUT'])
#en la url coloco el nombre para actualizar para buscarlo por medio del for
def editProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if (len(productsFound) > 0):
        #si encuentro el producto podre enviar el Json con los datos actualizados
        productsFound[0]['name'] = request.json['name']
        productsFound[0]['price'] = request.json['price']
        productsFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            #responde con un mensaje de accion cumplida y el json con los valores actualizados del producto especifico
            'message': 'Product Updated',
            'product': productsFound[0]
        })
    return jsonify({'message': 'Product Not found'})

# elimina un producto con DELETE
@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    #recorro y selecciono el producto buscado
    productsFound = [product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        #cuando lo encuentro elimino el producto y la lista de los productos que quedaron
        products.remove(productsFound[0])
        return jsonify({
            'message': 'Product Deleted',
            'products': products
        })
#conandos para inicializar el servidor
if __name__ == '__main__':
    app.run(debug=True, port=4000)

