from flask import render_template, request

from models import Dessert, Order, Order_Dessert_Junction, create_dessert, update_dessert, delete_dessert, update_order_to_completed
from app import app


@app.route('/')
def index():

    desserts = Dessert.query.all()

    return render_template('index.html', desserts=desserts)


@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'GET':
        return render_template('add.html')

    dessert_name = request.form.get('name_field')
    dessert_price = request.form.get('price_field')
    dessert_cals = request.form.get('cals_field')

    dessert = create_dessert(dessert_name, dessert_price, dessert_cals)
    return render_template('add.html', dessert=dessert) 

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        dessert_name = request.form.get('name_field')
        dessert_price = request.form.get('price_field')
        dessert_cals = request.form.get('cals_field')

        entry_to_update = update_dessert(id, dessert_name, dessert_price, dessert_cals)
        
        return render_template('update.html', dessert=entry_to_update, alr_updated=True) 
    
    else:
        entry_to_update = Dessert.query.get(id)
        return render_template('update.html', dessert=entry_to_update)
    
@app.route('/delete/<int:id>')
def delete(id):
    delete_dessert(id)
        
    return render_template('delete.html')

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'POST':
        filter_category = request.form.get('filter_category')
        more_or_less = request.form.get('more_or_less')
        number_to_filter_on = request.form.get('number_to_filter_on')


        if filter_category == 'id':
            desserts = Dessert.query.filter(Dessert.id > number_to_filter_on) if more_or_less == 'more' else Dessert.query.filter(Dessert.id < number_to_filter_on)
        elif filter_category == 'price':
            desserts = Dessert.query.filter(Dessert.price > number_to_filter_on) if more_or_less == 'more' else Dessert.query.filter(Dessert.price < number_to_filter_on)
        else:
            desserts = Dessert.query.filter(Dessert.calories > number_to_filter_on) if more_or_less == 'more' else Dessert.query.filter(Dessert.calories < number_to_filter_on)
        
        return render_template('filter.html', desserts=desserts, alr_filtered=True) 
    
    else:
        return render_template('filter.html', alr_filtered=False)

@app.route('/orders')
def orders():
    orders = Order.query.all()
    odj = Order_Dessert_Junction.query.all()
    desserts = Dessert.query.all()
    return render_template('orders.html', orders=orders, odj=odj, desserts=desserts)

@app.route('/update_order/<int:id>')
def update_order(id):
    update_order_to_completed(id)
    orders = Order.query.all()
    odj = Order_Dessert_Junction.query.all()
    desserts = Dessert.query.all()
    return render_template('orders.html', orders=orders, odj=odj, desserts=desserts)

@app.route('/filter_orders')
def filter_orders():
    return render_template('filter_orders.html')

@app.route("/filter_orders/by_id", methods=['GET', 'POST'])
def filter_orders_by_id():
    if request.method == 'POST':
        more_or_less = request.form.get('more_or_less')
        number_to_filter_on = request.form.get('number_to_filter_on')
        odj = Order_Dessert_Junction.query.all()
        desserts = Dessert.query.all()
        orders = Order.query.filter(Order.id > number_to_filter_on) if more_or_less == 'more' else Order.query.filter(Order.id < number_to_filter_on)
        
        return render_template('by_id.html', orders=orders, odj=odj, desserts=desserts, alr_filtered=True) 
    
    else:

        return render_template('by_id.html', alr_filtered=False)

@app.route("/filter_orders/in_ex", methods=['GET', 'POST'])
def filter_orders_in_ex():
    desserts = Dessert.query.all()
    if request.method == 'POST':
        in_or_ex = request.form.get('in_or_ex')
        item = request.form.get('item')
        
        if in_or_ex == "includes":
            odj = Order_Dessert_Junction.query.filter(Order_Dessert_Junction.dessert_id == item)
            ids = list()
            for element in odj:
                ids.append(element.order_id)
            orders = Order.query.filter(Order.id.in_(ids))
                
        else:
            odj = Order_Dessert_Junction.query.filter(Order_Dessert_Junction.dessert_id == int(item))
            ids = list()
            for element in odj:
                ids.append(element.order_id)
            orders = Order.query.filter(~Order.id.in_(ids))
        odj = Order_Dessert_Junction.query.all()
        return render_template('in_ex.html', orders=orders, odj=odj, desserts=desserts, alr_filtered=True) 
    
    else:

        return render_template('in_ex.html', alr_filtered=False, desserts=desserts)

@app.route("/filter_orders/total", methods=['GET', 'POST'])
def filter_orders_total():
    if request.method == 'POST':
        more_or_less = request.form.get('more_or_less')
        number_to_filter_on = request.form.get('number_to_filter_on')
        odj = Order_Dessert_Junction.query.all()
        desserts = Dessert.query.all()
        orders = Order.query.filter(Order.total > number_to_filter_on) if more_or_less == 'more' else Order.query.filter(Order.total < number_to_filter_on)
        
        return render_template('total.html', orders=orders, odj=odj, desserts=desserts, alr_filtered=True) 
    
    else:

        return render_template('total.html', alr_filtered=False)


@app.route("/filter_orders/completion", methods=['GET', 'POST'])
def filter_orders_completion():
    if request.method == 'POST':
        completed = request.form.get('completed')
        odj = Order_Dessert_Junction.query.all()
        desserts = Dessert.query.all()
        if completed == "True":
            orders = Order.query.filter(Order.status == True)
        else:
            orders = Order.query.filter(Order.status == False)
        return render_template('completion.html', orders=orders, odj=odj, desserts=desserts, alr_filtered=True) 
    
    else:

        return render_template('completion.html', alr_filtered=False)
    