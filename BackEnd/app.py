from flask import Flask, render_template, request, jsonify,session, request, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS #importing the cors to avoid policy errors against the safety
from datetime import datetime, timedelta #importing time
from sqlalchemy.orm import joinedload
import json #importing the json to convert into the jsonify response
from flask import Flask, request, jsonify, current_app, send_file
import jwt #importing the jwt to generate the jwt token 
import redis #import redis for backend
# from functools import wraps
from flask_caching import Cache #importing the Cache from flask_Caching
from tasks import export_csv #import export_csv from the funcs to create triggered celery job
from models import Product,User,Category,Order #importing the models and used in respective places
from database import db #importing db from the database


app = Flask(__name__)

app.config['SECRET_KEY'] = 'iitm@usha' #secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' #database used


redis_client = redis.Redis(host='localhost', port=6379, db=0) #redis_Client assigning
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client}) #assigining app to Cache class
CORS(app, origins='*') #wrapping cors to the app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #tracking the modifications in the app

@app.route('/signup', methods=['POST']) #signup api call using method post
def signup():
    data = request.get_json() #data object consists username,password,role,name,email
    username = data['username']
    password = data['password']
    role=data['role']
    name=data['name']
    email=data['email']
    if role=='manager':
        status='pending' #set to pending
    else:
        status='approved'

    if User.query.filter_by(username=username).first():
        return jsonify({'flash_message': 'Username already exists'}), 200 #user already exists
    
    user = User(name=name,username=username, password=password, role=role,status=status,email=email,cart=json.dumps({})) #cart init
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201 #user created and response  sent to frontend   
    
@app.route('/login', methods=['POST']) #login api for logging and based on role user admin mangager
def login():
    session["user_id"] = None
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        role=data['role']
        print(username,password,role) #if a manager who is not approved by admin tries to login sends flash message
        user1 = User.query.filter_by(username=username, password=password,role=role,status='pending').first()
        if user1:
            return jsonify({"flash_message":"Please wait till admin approves "}),200
        user = User.query.filter_by(username=username, password=password,role=role,status='approved').first()
        print(user)
        if user:
            print("user found") #user found
            expiration = datetime.utcnow() + timedelta(minutes=30)
            
            expiration_timestamp = int(expiration.timestamp())
            # Generate JWT token
            token = jwt.encode({
                'user': username,
                'exp': expiration_timestamp
            }, app.config['SECRET_KEY'], algorithm='HS256')
            session.permanent = True
            session["user_id"]=user.id 
            print(type(token))
             
            cart_list=[]
            if role=="user":
                cart=json.loads(user.cart)
                for i in cart.values():
                    for j in i:
                        cart_list.append(j)
                print(cart_list)
            return jsonify({'token':  token,'role':user.role ,'id':user.id ,'username':user.username,"cart_list":cart_list}),201
        else:
            return jsonify({'flash_message': 'Credentials Mismatch'}), 202 #credentials matched
    except Exception as e:
     
        print('Error:', str(e))
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/store_requests', methods=['GET']) #store requests if manager signs into it it is sent as request to the admin they are fetched and accessed in the adminHome
# @cache.cached(timeout = 3600)
def store_requests():
    store_manager = User.query.filter_by(role='manager', status='pending').all()
    
    if not store_manager:
        return jsonify({'message': 'No requests for Approval are available'}), 201 #no requests are avaialble to send
    print(store_manager)
    # print(type(store_manager))
    final_array=[]
    for i in store_manager:
        newobject = {
            'name':i.name,
            'username':i.username,
            'id':i.id,
        }
        final_array.append(newobject) 
    return jsonify({'storemanagers':final_array}),202 #the araray of store managers are sent 

@app.route('/deleteProducts', methods=['GET']) #fetching the  products which are setted delete by the status by the manager
# @cache.cached(timeout = 3600)
def deleteProducts():
    
    # print(token)
    product_list = Product.query.filter_by(status="delete").all()
    if not product_list:
        return jsonify({'message': 'No requests for deletion are available'}), 202
    delete_plist=[]
    for i in product_list:
        category_id =i.category_id
        store_manager=i.store_manager_id
        category = Category.query.get(category_id)
        manager=User.query.get(store_manager)
        print(manager.username)
        obj={"product_id":i.product_id,"product_name":i.product_name,"category_name":category.category_name,"manager_name":manager.username}
        delete_plist.append(obj)
    return jsonify({'deleteProducts':delete_plist}),201

@app.route('/accept', methods=['POST']) #accepting the credentials of the manager
def accept():
    data = request.get_json()
    id = data['id']
    print(id)
    User.query.filter_by(id=id).update({"status": 'approved'})
    db.session.commit()
    return jsonify({'message': 'Manager approved successfully'}), 201



@app.route('/reject', methods=['POST'])  #rejecting  the credentials of the manager and deleting from the database
def reject():
    data = request.get_json()
    id = data['id']
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return jsonify({'message': 'Manager Rejected successfully'}), 201
    
@app.route('/deleteProduct', methods=['POST'])  #on admin clicks the delete button in the delete product section this triggers
def deleteProduct():
    data = request.get_json()
    id = data['id']
    product = Product.query.filter_by(product_id=id).first()
    db.session.delete(product)
    users=User.query.all()
    for i in users:
        if i.role=="user":
            cart = json.loads(i.cart)
            for j in cart.values():
                if id in j:
                    j.remove(id)
            i.cart = json.dumps(cart)            
    db.session.commit()
    return jsonify({'message': 'Product Deleted successfully'}), 201

@app.route('/undeleteProduct', methods=['POST']) #on admin clicks the reject button in the delete product section this triggers
def undeleteProduct():
    data = request.get_json()
    id = data['id']
    product = Product.query.filter_by(product_id=id).first()
    product.status="ok"
    db.session.delete(product)           
    db.session.commit()
    return jsonify({'message': 'Product Deletion Rejected successfully'}), 201

@app.route("/add_category", methods=["GET", "POST"]) #used to add the category only accessed by the admin
def add_category():
    data = request.get_json()
    categoryName = data['categoryName']
    print(categoryName)
    if Category.query.filter_by(category_name=categoryName).first():
        return jsonify({'message': 'Category already exists'}), 400
    
    category = Category(category_name=categoryName)
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category Added Succcesfully'}), 201

@app.route("/edit_category", methods=["POST", "GET"]) #used to edit  the category only accessed by the admin
# @cache.cached(timeout = 3600)
def edit_category():
    data = request.get_json()
    oldName = data['oldName']
    newName = data['newName']
    check_category = Category.query.filter_by(category_name=oldName).first()
    if check_category is not None:
        check_category.category_name = newName
        db.session.commit()
        return jsonify({"message":"OK"}),202
    else:
        return jsonify({"message":"not ok"}),201

@app.route("/getCategories", methods=["POST", "GET"]) #used to get the categories only accessed by the admin
# @cache.cached(timeout = 3600)
def getCategories():
    list=[]
    #category_list = Category.query.all()
    category_list = Category.query.with_entities(Category.category_id, Category.category_name).all()
    # print(category_list)
    for i in category_list:
        obj={"category_id":i.category_id,"category_name":i.category_name}
        list.append(obj)
    #print(list)
    return jsonify({'categories':list}) 

@app.route('/deleteCategory', methods=['POST']) #used to delete the category only accessed by the admin
def deleteCategory():
    data = request.get_json()
    id = data['id']
    print(id)
    category = Category.query.filter_by(category_id=id).first()
    #category = Category.query.filter_by(category_id=id).with_entities(Category.category_id, Category.category_name).first()
    product = Product.query.filter_by(category_id = id).all()
    for i in product:
        db.session.delete(i) 
    print(category)
    users = User.query.all()
    for i in users:
        if i.role=="user":
            cart = json.loads(i.cart)
            if str(id) in cart.keys():
                cart.pop(str(id)) #on deleting the category it is also removed from the cart of all the users also
            cart = json.dumps(cart)
            i.cart=cart
    
    print('Helloworld')
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category Deleted successfully'}), 201
    

@app.route('/addProduct',methods=['POST']) #used to add the product only accessed by the  storemanagers
def addProduct():
    data = request.get_json()
    product = Product()
    print(data)
    another_product = Product.query.filter_by(product_name = data["productName"]).first()
    if another_product:
        return jsonify({"flash_message":"product already exits with this name"}),202
    product.product_name = data["productName"]
    product.rate=data["price"]
    product.quantity=data["quantity"]
    product.category_id = data["category"]
    product.units = data["units"]
    store_manager= data['store_manager_id']
    product.status='ok'
    product.store_manager_id = store_manager 
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product Added successfully'}), 201

@app.route('/editProduct',methods=['POST']) #used to edit  the product only accessed by the  storemanagers
def editProduct():
    data = request.get_json()
    print(data)
    old_product_name = data["editProductName"]
    product = Product.query.filter_by(product_name=old_product_name).first()
    # print(product.product_name,product.product_id)
    store_manager= data['store_manager_id']
    print(type(store_manager))
    if product:
        if int(store_manager)==product.store_manager_id:
            print("hi")
            product.product_name = data["editNewProductName"]
            product.rate=data["editPrice"]
            product.quantity=data["quantity"]
            product.category_id = data["category"]
            product.units = data["unit"]
            db.session.commit()
            return jsonify({'message': 'Product Edited successfully'}),200
        else:
            return jsonify({'flash_message':"UnAuthorized Access to edit ,Contact admin for more details"}),202
    else:
        return jsonify({"flash_message":'No product Found with this name'}),201
        

@app.route("/getcategories_products",methods=["GET"]) #used to get  the  categories and products  
# @cache.cached(timeout = 3600)
def getcategories_products():
    categories_product=[]
    category_list = Category.query.all()
    product_list=[]
    for i in category_list:
        products = Product.query.filter_by(category_id=i.category_id).all()
        for j in products:
            details={"category_name":i.category_name,"product_name":j.product_name,"price":j.rate,"units":j.units,"Quantity":j.quantity}
            categories_product.append(details)
    print(categories_product)
    return jsonify({"category_products":categories_product})


@app.route("/orderTable",methods=["POST"]) #used to retrive the data and get the data in the orders table 
def orderTable():
    data=request.get_json()
    user_id=data['user_id']
    orders_list=[]
    order = Order.query.filter_by(user_id=user_id).all()
    if order:
        for i in order:
            details={"product_name":i.name,"price":i.price,"amount":i.amount,"Quantity":i.quantity}
            orders_list.append(details)
        print(orders_list)
        return jsonify({"orders_list":orders_list}),201
    else:
        return jsonify({"message":"no orders "}),202


@app.route('/allproducts',methods=["GET"]) #used to retrive the prodcuts  and get the data in the products table 
# @cache.cached(timeout = 3600)
def allproducts():
    product_list=[]
    products = Product.query.all()
    for i in range(len(products)):
        product = {"product_name":products[i].product_name,"price":products[i].rate,"Quantity":products[i].quantity,"units":products[i].units}
        product_list.append(product)
    print(product_list)
    return jsonify({"products":product_list})


@app.route("/add_to_cart",methods=["POST"]) #used to add the products into the cart
def add_to_cart():
    data=request.get_json()
    p_name=data["product_name"]
    user_id = data["user_id"]
    product = Product.query.filter_by(product_name=p_name).first()
    cat_id = product.category_id
    user = User.query.filter_by(id=user_id).first()
    cart = user.cart
    if cart is None:
        print("Hi")
        cart=json.dumps({})
    cart = json.loads(cart)
    if str(cat_id) in cart.keys():
        print("Ho")
        cart[str(cat_id)].append(product.product_id)
    else:
        print("Hi")
        cart[(str(cat_id))] = [product.product_id]
    cart = json.dumps(cart)
    user.cart = cart 
    db.session.commit()
    return jsonify({"message":"Added to Cart succesfully"})
        
@app.route("/remove_from_cart",methods=["POST"]) #used to remove the products from the cart
def remove_from_cart():
    data=request.get_json()
    p_name=data["product_name"]
    user_id = data["user_id"]
    product = Product.query.filter_by(product_name=p_name).first()
    cat_id = product.category_id
    user = User.query.filter_by(id=user_id).first()
    cart = user.cart
    cart = json.loads(cart)
    print("renove from cart :hello")
    for i in cart.keys():
        print(i)
        for j in cart[i]:
            if int(j) == product.product_id:
                print("Hi")
                cart[i].remove(j)
                break
    cart = json.dumps(cart)
    user.cart = cart 
    db.session.commit()
    return jsonify({"message":"Deleted from Cart succesfully"})
    
@app.route("/getcart",methods=["POST"]) #used to get  the products from the cart
def getcart():
    data=request.get_json()
    user_id = data["user_id"]
    print(user_id)
    user=User.query.get(user_id)
    cart=json.loads(user.cart)
    product_ids=[]
    finalCartList=[]
    for i in cart.values():
        for j in i:
            product_ids+=[int(j)]
    product_ids=list(set(product_ids))
    print(product_ids)
    if product_ids:
        for i in product_ids:
            print(i)
            product = Product.query.filter_by(product_id=i).first()
            print(product)
            category = Category.query.filter_by(category_id = product.category_id).first()
            details={"product_id":product.product_id,"category_name":category.category_name,"product_name":product.product_name,"price":product.rate,"units":product.units,"Quantity":product.quantity}
            finalCartList.append(details)
        print(finalCartList)
        return jsonify({"cartList":finalCartList})
    else:
        return jsonify({"message":"No products in your cart "}),201
    
        
        
                    
    
    
@app.route('/setDeleteProduct',methods=["POST"]) #set the prodcut status to delete on admin clicks the delete button it trgiigers only accessed by admin
def setDeleteProduct():
    data = request.get_json()
    product_name = data['product_name']
    product = Product.query.filter_by(product_name=product_name).first()
    product.status="delete"
    db.session.commit()
    return jsonify({"message":"Sent to ADMIN for Confirmation to Delete Product"}) ,201
         

@app.route("/filterProducts",methods=["POST"]) #used in filtering of the products
def filterProducts():
    categories_product=[]
    data = request.get_json()
    category_id = data['category']
    print(category_id)
    f=1
    print(type(category_id))
    if(type(category_id)==str):
        category_id=int(category_id)
    if category_id==0:
        category_list = Category.query.all()
    else:
        f=0
        category_list=Category.query.filter_by(category_id=category_id).first()
    product_list=[]
    if f!=0:
        for i in category_list:
            print('hi')
            products = Product.query.filter_by(category_id=i.category_id).all()
            for j in products:
                details={"category_name":i.category_name,"product_name":j.product_name,"price":j.rate,"units":j.units,"Quantity":j.quantity}
                categories_product.append(details)
    else:
        products = Product.query.filter_by(category_id=category_list.category_id).all()
        for j in products:
            details={"category_name":category_list.category_name,"product_name":j.product_name,"price":j.rate,"units":j.units,"Quantity":j.quantity}
            categories_product.append(details)
    print(categories_product)
    return jsonify({"category_products":categories_product})


@app.route("/orders",methods=["POST"]) #used in adding   the products into orders table on clicked 
def orders():
    data = request.get_json()
    print(data)
    quantity =data['quantity']
    amount=data['amount']
    user_id=data['user_id']
    print(user_id)
    print(type(quantity),type(amount))
    print(quantity)
    print(amount)
    for key,value in quantity.items():
        order=Order()
        product = Product.query.filter_by(product_id = key).first()
        order.user_id =user_id
        order.product_id = key
        order.quantity = value
        order.price =  product.rate
        order.name=product.product_name
        order.amount = amount[key]
        order.status = "success"
        Product.query.filter_by(product_id = key).update({"quantity":Product.quantity-value})
        db.session.add(order)
    User.query.filter_by(id=user_id).update({"cart": json.dumps({})})
    # print(user.cart)
    db.session.commit()
    return jsonify({"message":"ordered succesfully"})

@app.route('/export_products/<int:user_id>/', methods=['GET']) #this is a trigger job on manager clicking the download button it downloads csv
# @cache.cached(timeout = 3600)
def export_products(user_id):
    print(user_id)
 
    try:        
        csv_data = export_csv.apply_async((user_id,)).get()
        print("Hello world")
        response = make_response(csv_data)
        response.headers["Content-Disposition"] = "attachment; filename=product_report.csv"
        response.headers["Content-type"] = "text/csv"
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
 







db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5050)
