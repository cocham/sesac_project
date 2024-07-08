from flask import Flask, request, render_template, jsonify, redirect, url_for
from sqlalchemy import func, asc
from dbgenerate.db import db, Admin, User  # Import your SQLAlchemy models here
from datetime import datetime, timedelta
import bcrypt
import os

app = Flask(__name__)
app.secret_key = 'my_admin_page'

# SQLite 데이터베이스 파일 경로 설정(버그 안나게 상대경로 설정하기 )
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'dbgenerate', 'instance', 'allinfo.db').replace('\\','/'))
print(f"SQLite 데이터베이스 경로: {app.config['SQLALCHEMY_DATABASE_URI']}")
db.init_app(app)

def paginate_data(page_number, per_page, data_list):
    start_index = (page_number - 1) * per_page
    end_index = start_index + per_page
    return data_list[start_index:end_index]


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        id = request.form['userid']
        pw = request.form['userpw']

        admin = Admin.query.filter_by(id=id).first()
        print(admin)
        if admin and bcrypt.checkpw(pw.encode('utf-8'),admin.password):
            return redirect(url_for('user'))
        else:
            print('사용자 로그인 실패')
    
    return app.send_static_file('login.html')

@app.route('/users')
def user():
    return app.send_static_file('user.html')

@app.route('/api/users', methods=['GET'])
def api_users():
    users = User.query.all()
    search_name = request.args.get('name', default='', type=str)
    per_page = request.args.get('per_page', default=10, type=int)
    gender = request.args.get('gender', default='All', type=str)
    page = request.args.get('page', default=1, type=int)

    # 필터링 적용
    if gender == 'Female':
        filtered_users = [user for user in users if user.gender == 'Female']
    elif gender == 'Male':
        filtered_users = [user for user in users if user.gender == 'Male']
    else:
        filtered_users = users

    if search_name:
        filtered_users = [user for user in filtered_users if search_name in user.name]

    total_pages = len(filtered_users) // per_page + (1 if len(filtered_users) % per_page > 0 else 0)
    paginated_users = paginate_data(page, per_page, filtered_users)

    serialized_users = []
    for user in paginated_users:
        serialized_users.append({
            'id': user.id,
            'name': user.name,
            'gender': user.gender,
            'age': user.age,
            'birthday': user.birthday.strftime('%Y-%m-%d'),  # 날짜 포맷 변경
            'address': user.address
        })

    return jsonify({
        'users': serialized_users,
        'total_pages': total_pages,
        'start_index': (page - 1) * per_page
    })

if __name__ == "__main__":
    app.run(debug=True)

