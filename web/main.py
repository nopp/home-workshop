from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

api_url = "http://localhost:8080"

@app.route('/')
def index():
    response = requests.get(api_url+"/products")
    print(response.status_code)
    products = response.json()
    return render_template('index.html', products=products)

@app.route('/product/<int:id>')
def view_product(id):
    response = requests.get(api_url+"/product/"+str(id))
    product = response.json()
    return render_template('product.html', product=product)

@app.route('/product/new', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'cabinet': request.form['cabinet'],
            'shelf': request.form['shelf']
        }
        response = requests.post(api_url+"/product", json=data)
        if response.status_code == 201:
            return redirect('/')
    
    return render_template('create_product.html')

@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    response = requests.get(api_url+"/product/"+str(id))
    product = response.json()

    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'cabinet': request.form['cabinet'],
            'shelf': request.form['shelf']
        }
        response = requests.put(api_url+"/product/"+str(id), json=data)
        if response.status_code == 200:
            return redirect('/')

    return render_template('edit_product.html', product=product)

@app.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    response = requests.delete(api_url+"/product/"+str(id))
    if response.status_code == 204:
        return redirect('/')

if __name__ == '__main__':
    app.run(port=5050,debug=True)
