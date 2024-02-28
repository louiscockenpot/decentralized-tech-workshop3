from flask import Flask, request, jsonify, redirect, url_for, render_template
import psycopg2
import os

password_db = os.getenv("PASSWORD")

db_connection = psycopg2.connect(dbname="ecommerce", user="louisecommerce", password=password_db, host="localhost", port="5432")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET', 'POST'])
def get_products():
    if request.method == 'POST':
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO products (name, description, price, category, stock_status) VALUES (%s, %s, %s)", (request.form['name'], request.form['description'], request.form['price'], request.form['category'], request.form['stock_status']))
        db_connection.commit()
        cursor.close()
        return jsonify(name=request.form['name'], description=request.form['description'], price=request.form['price'], category=request.form['category'], stock_status=request.form['stock_status'])
    
    elif request.method == 'GET':
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        #return jsonify(products=products)
        return render_template('products.html', products=products)

@app.route('/products/:id', methods=['GET', 'PUT', 'DELETE'])
def get_product(id):
    if request.method == 'PUT':
        cursor = db_connection.cursor()
        cursor.execute("UPDATE products SET name = %s, description = %s, price = %s , category = %s, stock_status = %s, WHERE id = %s", (request.form['name'], request.form['description'], request.form['price'], request.form['category'], request.form['stock_status'], id))
        db_connection.commit()
        cursor.close()
        return jsonify(name=request.form['name'], description=request.form['description'], price=request.form['price'], category=request.form['category'], stock_status=request.form['stock_status'])
    
    elif request.method == 'DELETE':
        cursor = db_connection.cursor()
        cursor.execute(f"DELETE FROM products WHERE id = {id}")
        db_connection.commit()
        cursor.close()
        return {'status': 'success'}
    
    elif request.method == 'GET':
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT * FROM products WHERE id = {id}")
        product = cursor.fetchone()
        cursor.close()
        return jsonify(product=product)
    
@app.route('/orders', methods=['POST'])
def get_orders():
    if request.method == 'POST':
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO orders (user_id, total_price, status) VALUES (%s, %s, %s)", (request.form['user_id'], request.form['total_price'], request.form['status']))
        db_connection.commit()
        cursor.close()
        return jsonify(product_id=request.form['user_id'], quantity=request.form['total_price'], total=request.form['status'])
    
@app.route('/orders/:userId', methods=['GET'])    
def get_order(user_id):
    if request.method == 'GET':
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT * FROM orders WHERE user_id = {user_id}")
        orders = cursor.fetchall()
        cursor.close()
        return jsonify(orders=orders)
    
@app.route('/cart/:userId', methods=['GET', 'POST'])
def get_cart(userId):
    if request.method == 'POST':
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)", (userId, request.form['product_id'], request.form['quantity']))
        db_connection.commit()
        cursor.close()
        return redirect(url_for('cart/:userId', userId=userId))
    
    elif request.method == 'GET':
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT * FROM cart WHERE user_id = {userId}")
        cart = cursor.fetchall()
        cursor.close()
        return jsonify(cart=cart)
    
@app.route('/cart/:userId/item/:productId', methods=['DELETE'])
def delete_cart_item(userId, productId):
    if request.method == 'DELETE':
        cursor = db_connection.cursor()
        cursor.execute(f"DELETE FROM cart WHERE user_id = {userId} AND product_id = {productId}")
        db_connection.commit()
        cursor.close()
        return redirect(url_for('cart/:userId', userId=userId))

if __name__ == '__main__':
    app.run(debug=True, port=3001)
