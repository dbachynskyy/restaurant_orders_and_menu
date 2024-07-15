from flask import render_template, request

from user_models import Dessert, Order, Order_Dessert_Junction, create_order
from user_app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    desserts = Dessert.query.all()
    if request.method == 'POST':
        list_of_items = list()
        list_of_quantity = list()
        for i in range(len(desserts)):
            target = str(desserts[i].id) + '_quantity'
            quantity = int(request.form.get(target))
            if quantity > 0:
                list_of_items.append(desserts[i].id)
                list_of_quantity.append(quantity)
        if len(list_of_items) > 0:
            create_order(list_of_items, list_of_quantity)
        return render_template('user_index.html', desserts=desserts, alr_added=True)
    else: 
        return render_template('user_index.html', desserts=desserts, alr_added=False)