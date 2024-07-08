import csv
from flask import Flask
from db import db,Admin,User,Store,Order,Orderitem,Item
from datetime import datetime
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///allinfo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def load_csv_data(filename):
    with open(filename,'r',newline='',encoding='utf-8') as file:
        reader = csv.DictReader(file)
        if filename == 'users.csv':
            for row in reader:
                user = User(
                    id=row['Id'], 
                    name=row['Name'],
                    gender=row['Gender'],
                    age=int(row['Age']),
                    birthday= datetime.strptime(row['Birthday'], '%Y-%m-%d').date(),
                    address=row['Address']
                )
                db.session.add(user)
            db.session.commit()

        elif filename == 'stores.csv':
            for row in reader:
                store = Store(
                    id=row['Id'],  
                    name=row['Name'],
                    type=row['Type'],
                    address=row['Address']
                )
                db.session.add(store)
            db.session.commit()

        elif filename == 'orders.csv':
            for row in reader:
                order = Order(
                    id=row['Id'],  
                    orderat=datetime.strptime(row['OrderAt'], '%Y-%m-%d %H:%M:%S'),
                    storeid=row['StoreId'],
                    userid=row['UserId']
                )
                db.session.add(order)
            db.session.commit()

        elif filename == 'orderitems.csv':
            for row in reader:
                orderitem = Orderitem(
                    id=row['Id'],  
                    orderid=row['OrderId'],
                    itemid=row['ItemId'],
                )
                db.session.add(orderitem)
            db.session.commit()

        elif filename == 'items.csv':
            for row in reader:
                item = Item(
                    id=row['Id'],  
                    name=row['Name'],
                    type=row['Type'],
                    unitprice=int(row['UnitPrice'])
                )
                db.session.add(item)
            db.session.commit()


if __name__=="__main__":
    with app.app_context():
        db.create_all()

        #Admin 데이터 추가
        admin_id = 'kimmeme'
        admin_password = 'ncdasfje328'
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

        new_admin = Admin(id=admin_id, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

        load_csv_data('users.csv')
        load_csv_data('stores.csv')
        load_csv_data('orders.csv')
        load_csv_data('orderitems.csv')
        load_csv_data('items.csv')

