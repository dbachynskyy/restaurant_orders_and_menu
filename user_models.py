from user_app import db
from user_app import app
import datetime 


class Dessert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    calories = db.Column(db.Integer)

    def __init__(self, name, price, calories):
        self.name = name
        self.price = price
        self.calories = calories

    def calories_per_dollar(self):
        if self.calories:
            return self.calories / self.price
        
    def __repr__(self):
        return '<User %r>' % self.id

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Boolean, default=False, nullable=False)
    total = db.Column(db.Integer)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    def __init__(self):
        self.status = False
        self.total = 0
        
    def __repr__(self):
        return '<User %r>' % self.id
    
class Order_Dessert_Junction(db.Model):
    order_id = db.Column(
        db.Integer, 
        db.ForeignKey('order.id'),
        primary_key=True, 
        autoincrement=False
    )
    dessert_id = db.Column(
        db.Integer, 
        db.ForeignKey('dessert.id'),
        primary_key=True,
        autoincrement=False
    )
    quantity = db.Column(db.Integer)

    def __init__(self, order_id, dessert_id, quantity):
        self.order_id = order_id
        self.dessert_id = dessert_id
        self.quantity = quantity
        
    def __repr__(self):
        return '<User %r>' % self.order_id



def create_dessert(new_name, new_price, new_calories):
    dessert = Dessert(new_name, new_price, new_calories)


    db.session.add(dessert)

    db.session.commit()

    return dessert

def create_order(list_of_items, list_of_quantity):
    order = Order()
    db.session.add(order)
    db.session.commit()

    for i in range(len(list_of_items)):
        odj = Order_Dessert_Junction(order.id, list_of_items[i], list_of_quantity[i])
        db.session.add(odj)

    desserts = Dessert.query.filter(Dessert.id.in_(list_of_items))
    total = 0
    for i in range(len(list_of_quantity)):
        total = total + desserts[i].price*list_of_quantity[i]
    order.total = total
    db.session.commit()

    return order

if __name__ == "__main__":
    print("Creating database tables...")
    with app.app_context():
        db.create_all()
    print("Done!")