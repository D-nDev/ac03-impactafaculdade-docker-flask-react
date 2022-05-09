from flask import Flask, jsonify, request, render_template, make_response
from model.product import db
from flask_cors import CORS

from model.product import Product


app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://ac03:123456@postgres:5432/products'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, resources={r"*": {"origins": "*"}})

db.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/list')
def userlist():
    return render_template('list.html')


@app.route('/newproduct', methods=['POST'])
def create_product():
    try:
        db.create_all()
        db.session.commit()

        product_data = request.json

        product_name = product_data['name']
        product_category = product_data['category']
        product_price = product_data['price']

        product = Product(name=product_name, category=product_category,
                    price=product_price)

        db.session.add(product)
        db.session.commit()

        res = make_response(jsonify({"success": "Product created"}), 201)
        return res
    except Exception as e:
        print(e)
        err = make_response(jsonify({"error: ": "An error has occurred"}), 500)
        return err


@app.route('/allproducts', methods=['GET'])
def get_products():
    try:
        all_products = []
        products = Product.query.all()
        for product in products:
            result = {
                "id": product.id,
                "name": product.name,
                "category": product.category,
                "price": product.price,
            }
            all_products.append(result)

        res = make_response(jsonify(all_products), 200)
        return res
    except Exception as e:
        print(e)
        err = make_response(jsonify({"error: ": "An error has occurred"}), 500)
        return err


if __name__ == "__main__":
    app.run(host='0.0.0.0')
