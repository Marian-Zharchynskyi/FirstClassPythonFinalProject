from flask import Flask, request, send_file
from electronics_store import Electronics_store
from electronic import Electronic

app = Flask(__name__)

electronics_store = Electronics_store()
electronics_store.read_file()


@app.route("/get-electronics", methods=["GET"])
def get_all_products():
    return electronics_store.get_all_electronics()


@app.route("/get-electronic/<id>", methods=["GET"])
def get_some_product(id: str):
    return electronics_store.get_some_electronic(id)


@app.route("/create-electronic", methods=["POST"])
def add_product():
    rqst_json = request.json
    return electronics_store.add_electronic(
        Electronic(rqst_json['name'], rqst_json['id'], rqst_json['price'], rqst_json['released_at'], rqst_json['manufacturer'],
                   rqst_json['guarantee']))


@app.route("/update-electronic/<id>", methods=["PUT"])
def update_product(id: str):
    rqst_json = request.json
    return electronics_store.update_electronic(Electronic(rqst_json['name'], id, rqst_json['price'], rqst_json['released_at'], rqst_json['manufacturer'], rqst_json['guarantee']))


@app.route("/delete-electronic/<id>", methods=["DELETE"])
def delete_product(id: str):
    return electronics_store.delete_electronic(id)


@app.route("/get-products_in_some_period", methods=["GET"])
def get_products_in_some_period():
    borders = request.json
    return electronics_store.get_electronics_in_some_period(borders["from"], borders["to"])


@app.route("/get-most-expensive-products", methods=["GET"])
def get_most_expensive_products():
    return electronics_store.get_most_expensive_electronics()


@app.route('/graph', methods=['GET'])
def generate_graph():
    electronics_store.most_expensive_diagram()
    return send_file('The_most_expensive_electronic_by_the_company.png', mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)

