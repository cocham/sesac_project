from flask import Flask,render_template, request
import random

app = Flask(__name__)
user = ['김민희','김승은','안새미','이효림','정여원','김민서','윤석인','황조현','박수형','*']

@app.route('/',methods=['GET'])
def main():
    random_reque = request.args.get('random')
    if random_reque:
        random_user = user[:]
        random.shuffle(random_user)
        return render_template('seat.html',random_user=random_user)
    else:
        # 'random' 파라미터가 없는 경우 초기 상태의 테이블을 보여줌
        return render_template('seat.html', random_user=None)


if __name__ == "__main__":
    app.run(debug=True)