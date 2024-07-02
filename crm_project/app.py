from flask import Flask,request,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,asc
from dbgenerate.db import db,User,Store,Order,Orderitem,Item
from datetime import datetime, timedelta

app = Flask(__name__)
# SQLite 데이터베이스 파일 경로 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/sesac_project/crm_project/dbgenerate/instance/allinfo.db'
db.init_app(app)

def paginate_data(page_number, per_page, data_list):
    start_index = (page_number - 1) * per_page
    end_index = start_index + per_page
    return data_list[start_index:end_index]

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/users')
def user():
    users = User.query.all()
    
    page = request.args.get('page',default=1,type=int)
    search_name = request.args.get('name',default='',type=str) #아무것도 입력 안 한 상태에서 검색을 누르면 홈으로 되돌아 갈 수 있게..
    per_page = request.args.get('per_page',default=10,type=int)
    gender = request.args.get('gender',default='',type=str)

    if gender == 'Female':
        get_user = [user for user in users if (search_name in user.name and user.gender == 'Female')]
    elif str(gender) == 'Male':
        get_user = [user for user in users if (search_name in user.name and user.gender == 'Male')]
    else:
        get_user = [user for user in users if search_name in user.name]
    start_index = (page-1) * per_page
    total_pages = len(get_user) // per_page + (1 if len(get_user) % per_page > 0 else 0)
    current_data = paginate_data(page,per_page,get_user)

    render_dict = {
    'headers':['Index','Id','Name','Gender','Age','Birthday','Address'],
    'users':current_data,
    'total_pages':total_pages,
    'start_index':start_index,
    'page':page,
    'per_page':per_page,
    'search_name':search_name,
    'gender':gender
    }

    return render_template('user.html',**render_dict)


def top_store_item(userid):
    # 고객이 방문한 매장별 방문 횟수를 세는 서브쿼리
    subquery = db.session.query(Order.storeid, func.count(Order.id).label('visit_count')) \
                        .filter(Order.userid == userid) \
                        .group_by(Order.storeid) \
                        .order_by(func.count(Order.id).desc()) \
                        .limit(5) \
                        .subquery()
    # 서브쿼리를 사용하여 매장 정보를 가져오는 메인 쿼리
    top_stores = db.session.query(
                Store,
                subquery.c.visit_count
            ).join(
                subquery, Store.id == subquery.c.storeid
            ).order_by(
                subquery.c.visit_count.desc()
            ).all()
    
    # 고객이 자주 주문한 상품별 주문 횟수를 세는 서브쿼리
    subquery2 = db.session.query(
                    Orderitem.itemid,
                    Item.name,
                    func.count(Orderitem.id).label('order_count')
                ).join(
                    Item, Orderitem.itemid == Item.id
                ).join(
                    Order, Orderitem.orderid == Order.id
                ).filter(
                    Order.userid == userid
                ).group_by(
                    Orderitem.itemid, Item.name
                ).order_by(
                    func.count(Orderitem.id).desc()
                ).limit(5).subquery()

    # 서브쿼리를 사용하여 상품 정보와 주문 횟수를 가져오는 메인 쿼리
    top_items = db.session.query(
                    subquery2.c.name,
                    subquery2.c.order_count
                ).all()

    return top_stores,top_items

@app.route('/user/<uuid>')
def user_detail(uuid):

    #해당 UUID에 해당하는 사용자를 찾아서 데이터 전달
    user = User.query.filter_by(id=uuid).first()
    headers1 = ['Id','Name','Gender','Age','Birthday','Address']
    headers2 = ['Order Id','Purchased Date','Purchased Location']
    orders = Order.query.filter_by(userid=user.id).all()

    top_stores,top_items = top_store_item(user.id)
    for item in top_items:
        print(f"{item[0]} {item[1]}번 주문")
    render_dict = {
        'user':user,
        'headers1':headers1,
        'headers2':headers2,
        'orders':orders,
        'top_stores':top_stores,
        'top_items':top_items
    }
    return render_template('user_detail.html',**render_dict)


@app.route('/orders')
def order():
    orders = Order.query.order_by(asc(Order.orderat)).all()
    page = request.args.get('page',default=1,type=int)
    #주문언제 했는지로 검색?
    order_date = request.args.get('order_date',default='전체',type=str)
    if order_date == '전체':
        get_orders = orders
    else:
        year_month = datetime.strptime(order_date, '%Y-%m')
        start_date = year_month.replace(day=1)
        end_date = year_month.replace(day=1, month=year_month.month + 1) - timedelta(days=1)
        get_orders = Order.query.filter(Order.orderat.between(start_date, end_date)).order_by(Order.orderat).all()

    per_page = request.args.get('per_page',default=10,type=int)
    start_index = (page-1) * per_page
    total_pages = len(get_orders) // per_page + (1 if len(get_orders) % per_page > 0 else 0)
    current_data = paginate_data(page,per_page,get_orders)

    render_dict = {
    'headers':['Index','Id','Ordered At','Store Id','User Id'],
    'orders':current_data,
    'total_pages':total_pages,
    'start_index':start_index,
    'page':page,
    'per_page':per_page,
    'order_date':order_date
    }

    return render_template('order.html',**render_dict)

@app.route('/orders/orderitem-detail/<uuid>')
def orderitem_detail(uuid):
    headers = ['Id','Order Id','Item Id','Item Name']

    #클릭한 uuid의 order정보(order.id,order.orderat,order.storeid,order.userid)
    order = Order.query.filter_by(id=uuid).first()

    #해당 order의 id와 같은 주문템들 정보(orderitem.id,orderitem.orderid,orderitem.itemid)
    oinfo = Orderitem.query.filter_by(orderid=order.id).all()
    onames = []
    for i in range(len(oinfo)):
        itemname = Item.query.filter_by(id=oinfo[i].itemid).first()
        onames.append(itemname.name)

    return render_template('orderitem_detail.html',headers = headers,oinfo=oinfo,onames=onames)

@app.route('/orders/order-detail/<orderid>')
def order_detail(orderid):
    headers = ['Id','Ordered At','Store Id','User Id']
    order = Order.query.filter_by(id=orderid).first()

    return render_template('order_detail.html',headers=headers,order=order)


# 연도와 월별 매출액을 계산하는 함수(아이템)
def calculate_monthly_revenue(year,item):
    monthly_sales = []
    month_2023 = [i for i in range(1,13)]
    month_2024 = [i for i in range(1,7)]
    if year == 2023:
        list = month_2023
    else:
        list = month_2024
    for month in list:
        # 해당 연도와 월의 첫날과 마지막 날 계산
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year,month,31,23,59,59)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
        monthly_revenue = db.session.query(func.sum(Item.unitprice)) \
                                    .join(Orderitem, Item.id == Orderitem.itemid) \
                                    .join(Order, Orderitem.orderid == Order.id) \
                                    .filter(Order.orderat.between(start_date,end_date)) \
                                    .filter(Item.name == item)\
                                    .scalar() or 0
        
        monthly_sales_date = db.session.query(func.count()) \
                                    .select_from(Item) \
                                    .join(Orderitem, Item.id == Orderitem.itemid) \
                                    .join(Order, Orderitem.orderid == Order.id) \
                                    .filter(Order.orderat.between(start_date,end_date)) \
                                    .filter(Item.name == item)\
                                    .scalar() or 0
        # 월별 매출액을 딕셔너리에 저장
        monthly_sales.append([f"{year}-{month:02d}",monthly_revenue,monthly_sales_date])

    return monthly_sales

@app.route('/orders/item-detail/<itemid>')
def item_detail(itemid):
    headers1 = ['Name','Unit Price']
    item = Item.query.filter_by(id=itemid).first()
    item_name = item.name
    headers2 = ['Month','Total Revenue','Item Count']

    revenue_2023 = calculate_monthly_revenue(2023,item_name)
    revenue_2024 = calculate_monthly_revenue(2024,item_name)

    render_dict = {
        'headers1':headers1,
        'headers2':headers2,
        'item':item,
        'item_name':item_name,
        'revenue_2023':revenue_2023,
        'revenue_2024':revenue_2024
    }
    return render_template('item_detail.html',**render_dict)


@app.route('/order-items')
def order_item():
    orderitems = Orderitem.query.all()

    page = request.args.get('page',default=1,type=int)
    per_page = request.args.get('per_page',default=10,type=int)

    start_index = (page-1) * per_page
    total_pages = len(orderitems) // per_page + (1 if len(orderitems) % per_page > 0 else 0)
    current_data = paginate_data(page,per_page,orderitems)
    
    render_dict = {
    'headers':['Index','Id','Order Id','Item Id'],
    'orderitems':current_data,
    'total_pages':total_pages,
    'start_index':start_index,
    'page':page,
    'per_page':per_page
    }

    return render_template('orderitem.html',**render_dict)

@app.route('/items')
def item():
    items = Item.query.all()

    page = request.args.get('page',default=1,type=int)
    per_page = request.args.get('per_page',default=10,type=int)
    item_type = request.args.get('item_type',default='',type=str)
    get_item = [item for item in items if item_type in item.type]

    start_index = (page-1) * per_page
    total_pages = len(get_item) // per_page + (1 if len(get_item) % per_page > 0 else 0)
    current_data = paginate_data(page,per_page,get_item)
    
    render_dict = {
    'headers':['Index','Id','Type','Name','Unit Price'],
    'items':current_data,
    'total_pages':total_pages,
    'start_index':start_index,
    'page':page,
    'per_page':per_page,
    'item_type':item_type
    }


    return render_template('item.html',**render_dict)

@app.route('/stores')
def store():
    stores = Store.query.all()
    
    page = request.args.get('page',default=1,type=int)
    search_store = request.args.get('name',default='',type=str) #아무것도 입력 안 한 상태에서 검색을 눌러도 작동
    per_page = request.args.get('per_page',default=10,type=int)

    get_stores = [store for store in stores if search_store in store.name]
    start_index = (page-1) * per_page
    total_pages = len(get_stores) // per_page + (1 if len(get_stores) % per_page > 0 else 0)
    current_data = paginate_data(page,per_page,get_stores)

    render_dict = {
    'headers':['Index','Id','Type','Name','Address'],
    'stores':current_data,
    'total_pages':total_pages,
    'start_index':start_index,
    'page':page,
    'per_page':per_page,
    'search_store':search_store
    }

    return render_template('store.html',**render_dict)


# 연도와 월별 매출액을 계산하는 함수(스토어)
def store_monthly_revenue(year,storeid):
    monthly_sales = []
    month_2023 = [i for i in range(1,13)]
    month_2024 = [i for i in range(1,7)]
    if year == 2023:
        list = month_2023
    else:
        list = month_2024
    for month in list:
        # 해당 연도와 월의 첫날과 마지막 날 계산
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year,month,31,23,59,59)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
        monthly_revenue = db.session.query(func.sum(Item.unitprice))\
                            .join(Orderitem, Item.id == Orderitem.itemid)\
                            .join(Order, Orderitem.orderid == Order.id)\
                            .filter(Order.storeid == storeid, 
                                    Order.orderat.between(start_date, end_date))\
                            .scalar() or 0

        monthly_items_sold = db.session.query(
                                func.count(Orderitem.id)) \
                                .join(Order, Orderitem.orderid == Order.id)\
                                .filter(Order.storeid == storeid,
                                        Order.orderat.between(start_date, end_date))\
                                .scalar() or 0
        
        # 월별 매출액을 딕셔너리에 저장
        monthly_sales.append([f"{year}-{month:02d}",monthly_revenue,monthly_items_sold])

    return monthly_sales

def often_user(storeid):
    # store_id에 해당하는 고객들을 가져오는 쿼리
    top_frequent_customers = db.session.query(
                                        User.id,
                                        User.name,
                                        func.count(Order.id).label('order_count'))\
                                        .join(Order, User.id == Order.userid).\
                                        filter(Order.storeid == storeid).\
                                        group_by(User.id, User.name).\
                                        order_by(func.count(Order.id).desc()).\
                                        limit(10)  # 상위 10명만 선택
    
    return top_frequent_customers.all()

@app.route('/store-detail/<uuid>')
def store_detail(uuid):
    store = Store.query.filter_by(id=uuid).first()
    headers1 = ['Name','Type','Address']
    headers2 = ['Month','Revenue','Count']
    headers3 = ['User_Id','Name','Frequency']
    revenue_2023 = store_monthly_revenue(2023,store.id)
    revenue_2024 = store_monthly_revenue(2024,store.id)
    top_users = often_user(store.id)

    render_dict = {
        'store':store,
        'storeid':store.id,
        'headers1':headers1,
        'headers2':headers2,
        'headers3':headers3,
        'revenue_2023':revenue_2023,
        'revenue_2024':revenue_2024,
        'top_users':top_users
    }

    return render_template('store_detail.html',**render_dict)


# 연도와 월별 매출액을 계산하는 함수(스토어)
def store_monthdetail_revenue(year,storeid,month):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year, month, 31, 23, 59, 59)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
    
    monthly_sales = db.session.query(
        func.strftime('%Y-%m-%d', Order.orderat).label('day'),
        func.sum(Item.unitprice).label('revenue'),
        func.count(Orderitem.id).label('count')
    ).join(
        Orderitem, Order.id == Orderitem.orderid
    ).join(
        Item, Orderitem.itemid == Item.id
    ).filter(
        Order.storeid == storeid,
        Order.orderat.between(start_date, end_date)
    ).group_by(
        func.strftime('%Y-%m-%d', Order.orderat)
    ).order_by(
        func.strftime('%Y-%m-%d', Order.orderat)
    ).all()

    return monthly_sales


def often_monthly_user(year,month,storeid,limit):
    # 월별 고객별 주문 횟수를 계산하는 쿼리
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year, month, 31, 23, 59, 59)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)

    # store_id에 해당하는 고객들을 가져오는 쿼리
    top_frequent_customers = db.session.query(
                                        User.id,
                                        User.name,
                                        func.count(Order.id).label('order_count'))\
                                        .join(Order, User.id == Order.userid).\
                                        filter(Order.storeid == storeid,
                                                Order.orderat.between(start_date, end_date)).\
                                        group_by(User.id, User.name).\
                                        order_by(func.count(Order.id).desc()).\
                                        limit(limit).all()  # 상위 10명만 선택

    return top_frequent_customers

@app.route('/store-detail/<uuid>/<month>')
def store_detail_month(uuid,month):
    store = Store.query.filter_by(id=uuid).first()
    year = int(month[:4])
    month = int(month[-1])
    headers1 = ['Name','Type','Address']
    headers2 = ['Month','Revenue','Count']
    headers3 = ['User_Id','Name','Frequency']

    month_sales = store_monthdetail_revenue(year,store.id,month)
    month_users = often_monthly_user(year,month,store.id,len(month_sales))
    render_dict = {
        'store':store,
        'headers1':headers1,
        'headers2':headers2,
        'headers3':headers3,
        'month_sales':month_sales,
        'month_users':month_users
    }

    return render_template('store_month_detail.html',**render_dict)



if __name__ == "__main__":
    app.run(debug=True)