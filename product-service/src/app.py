from flask import Flask, jsonify, request
from db import db
from Product import Product
import logging.config
from sqlalchemy import exc
import configparser

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
log = logging.getLogger(__name__)


def get_database_url():
    config = configparser.ConfigParser()
    config.read('db.ini')
    database_configuration = config['mysql']
    host = database_configuration['host']
    username = database_configuration['username']
    password = database_configuration['password']
    database = database_configuration['database']
    database_url = f'mysql://{username}:{password}@{host}/{database}'
    log.info(f'Connecting to db: {database_url}')
    return database_url


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
db.init_app(app)


@app.route('/products')
def get_products():
    log.debug('Get /products')
    try:
        products = [product.json for product in Product.find_all()]
        return jsonify(products)
    except exc.SQLAlchemyError:
        log.exception('An exception occurred while retrieving all products')
        return 'An exception occurred while retrieving all products', 500


@app.route('/product/<int:id>')
def get_product(id):
    log.debug(f'GET /product/{id}')
    product = Product.find_by_id(id)
    if product:
        return jsonify(product.json)
    return f'Product with id {id} not found', 404


@app.route('/product', methods=['POST'])
def post_product():
    log.debug('POST /product:' + str(request.json))
    request_product = request.json
    new_product = Product(None, request_product['name'])
    new_product.save_to_db()
    return jsonify(new_product.json), 201


@app.route('/product/<int:id>', methods=['PUT'])
def put_product(id):
    log.debug(f'Editing Product with id {id}')
    existing_product = Product.find_by_id(id)
    if(existing_product):
        updated_product = request.json
        existing_product.name = updated_product['name']
        existing_product.save_to_db()
        return jsonify(existing_product.json), 200

    return f'Product with id {id} not found', 404


@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    log.debug('Deleting product with id {id}')
    existing_product = Product.find_by_id(id)
    if(existing_product):
        existing_product.delete_from_db()
        return jsonify({
            'message': f'Deleted Product with id {id}'
        }), 200

    return f'Product with id {id} not found', 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
