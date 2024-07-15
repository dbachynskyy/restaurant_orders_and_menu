from app import db
from app import app
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

def update_dessert(id, new_name, new_price, new_calories):
    entry_to_update = Dessert.query.get(id)
    entry_to_update.name = new_name
    entry_to_update.price = new_price
    entry_to_update.calories = new_calories

    db.session.commit()

    return entry_to_update

def update_order_to_completed(id):
    entry_to_update = Order.query.get(id)
    if entry_to_update.status == False:
        entry_to_update.status = True
    db.session.commit()

    return entry_to_update

def delete_dessert(id):
    entry_to_delete = Dessert.query.get(id)
    db.session.delete(entry_to_delete)
    db.session.commit()

if __name__ == "__main__":
    print("Creating database tables...")
    with app.app_context():
        db.create_all()
    print("Done!")