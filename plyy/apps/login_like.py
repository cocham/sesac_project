from functools import wraps
from flask import Flask, session, request, render_template, redirect, url_for, jsonify
import sqlite3
from uuid import uuid4
import os

app = Flask(__name__)
app.secret_key = 'plyy_page'

def connect_db():
    database_path = os.path.join(os.path.dirname(__file__), 'plyy.db')
    conn = sqlite3.connect(database_path)
    # conn = sqlite3.connect('plyy.db')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    return conn, cur

def curator_info(id):

    curator_info = []
    curator_tags = []
    conn,cur = connect_db()

    cur.execute('SELECT * FROM CURATOR WHERE c_uuid = ?',(id,))                     
    curator = cur.fetchone()
    curator_info.extend([curator[i] for i in range(len(curator))])
    
    cur.execute('''
                SELECT TAG.tag_name
                FROM CURATOR
                JOIN TAG_CURATOR ON CURATOR.c_uuid = TAG_CURATOR.c_uuid
                JOIN TAG ON TAG_CURATOR.tag_uuid = TAG.tag_uuid
                WHERE CURATOR.c_uuid = ?
                ''',(id,))
    
    ctags = cur.fetchall()
    conn.close()

    curator_tags.extend([ctags[i]['tag_name'] for i in range(len(ctags))])

    curator_info.append(curator_tags)

    return curator_info

def cu_plyy_tag(id,pid):
    plyy_tags = []

    conn,cur = connect_db()
    
    cur.execute('''
                SELECT TAG_GENRE.gtag_name
                FROM TAG_GENRE
                JOIN PLYY ON PLYY.gtag_uuid = TAG_GENRE.gtag_uuid
                WHERE PLYY.c_uuid = ? and PLYY.plyy_uuid = ?
                ''',(id,pid))
    
    cu_pgtag = cur.fetchall()
    for pgtag in cu_pgtag:
        plyy_tags.append(pgtag['gtag_name'])

    cur.execute('''    
            SELECT tag.tag_name
            FROM PLYY
            JOIN TAG_PLYY ON PLYY.plyy_uuid = TAG_PLYY.plyy_uuid
            JOIN TAG ON TAG_PLYY.tag_uuid = TAG.tag_uuid
            WHERE PLYY.c_uuid = ? and PLYY.plyy_uuid = ?''',(id,pid))
    
    cu_ptag = cur.fetchall()
    conn.close()

    for t in cu_ptag:
        plyy_tags.append(t['tag_name'])

    return plyy_tags



def cu_plyy(id):
    plyy_list = []

    conn,cur = connect_db()

    cur.execute('SELECT * FROM PLYY WHERE c_uuid = ?',(id,))
    plyy = cur.fetchall()
    conn.close()

    for p in plyy: #플리 객체
        each_plyy = []
        for i in range(len(p)): 
            each_plyy.append(p[i])
        each_plyy.append(cu_plyy_tag(id,each_plyy[0]))
        plyy_list.append(each_plyy)

    return plyy_list


@app.route('/main',methods=['get','post'])
def main():
    print(session)
    return render_template('main.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/myPage')
def mypage():
    return render_template('mypage.html')

@app.route('/login',methods=['GET','POST'])
def login():
    # print(session)
    if request.method == 'POST':

        conn,cur = connect_db()
        id = request.form['userid']
        pw = request.form['userpw']

        cur.execute('''
                        SELECT u_email, u_pw
                        FROM USER
                        WHERE u_email = ? and u_pw = ?
                    ''',(id,pw))

        user = cur.fetchone()
        conn.close()

        if user:
            session['id'] = id
            return redirect(url_for('main'))
        
        else:
            session['id'] = None
    
    return render_template('login.html')


@app.route('/curator/<c_uuid>')
def curator(c_uuid):
    # print(session)
    return render_template('test5.html')


# 좋아요 추가 함수
def curator_like(c_uuid, u_uuid):
    conn, cur = connect_db()

    cl_uuid = str(uuid4())
    try:
        # WHERE 조건으로 존재 여부 확인
        cur.execute('''
            SELECT * FROM CURATOR_LIKE
            WHERE u_uuid = ? AND c_uuid = ?
        ''', (u_uuid, c_uuid))

        row = cur.fetchone()

        if not row:
            cur.execute('''
                INSERT INTO CURATOR_LIKE (cl_uuid, u_uuid, c_uuid)
                VALUES (?, ?, ?)
            ''', (cl_uuid, u_uuid, c_uuid))
            conn.commit()  # INSERT 후에 커밋

        conn.close()
        return True
    
    except Exception as e:
        print(f"Error inserting like: {e}")
        conn.rollback()
        conn.close()
        return False

# 좋아요 추가 API 엔드포인트
@app.route('/plyy/api/like/<u_id>/<c_uuid>', methods=['POST'])
def like_curator(u_id, c_uuid):
    conn,cur = connect_db()
    cur.execute('SELECT u_uuid FROM USER WHERE u_email = ?',(u_id,))
    u_uuid = cur.fetchone()['u_uuid']
    conn.close()

    # print(u_uuid)
    success = curator_like(c_uuid, u_uuid)

    # print(success)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

def curator_unlike(c_uuid, u_uuid):
    conn, cur = connect_db()

    cl_uuid = str(uuid4())
    try:
        # WHERE 조건으로 존재 여부 확인
        cur.execute('''
            SELECT * FROM CURATOR_LIKE
            WHERE u_uuid = ? AND c_uuid = ?
        ''', (u_uuid, c_uuid))

        row = cur.fetchone()

        if row:
            cur.execute('''
                DELETE FROM CURATOR_LIKE
                WHERE u_uuid = ? AND c_uuid = ?
            ''', (u_uuid, c_uuid))
            conn.commit()  # DELETE 후에 커밋

        conn.close()
        return True
    
    except Exception as e:
        print(f"Error inserting like: {e}")
        conn.rollback()
        conn.close()
        return False
    
# 좋아요 취소 API 엔드포인트
@app.route('/plyy/api/unlike/<u_id>/<c_uuid>', methods=['DELETE'])
def unlike_curator(u_id, c_uuid):
    # 해당 유저와 큐레이터에 대한 좋아요 정보를 삭제
    conn,cur = connect_db()
    cur.execute('SELECT u_uuid FROM USER WHERE u_email = ?',(u_id,))
    u_uuid = cur.fetchone()['u_uuid']
    conn.close()

    # print(u_uuid)
    success = curator_unlike(c_uuid, u_uuid)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

#큐레이터 좋아요 상태 확인 함수
def curatorlike_status(c_uuid,u_uuid):
    conn,cur = connect_db()

    cur.execute('SELECT * FROM CURATOR_LIKE WHERE c_uuid = ? and u_uuid = ?',(c_uuid,u_uuid))
    likes = cur.fetchone()
    conn.close()
    if likes:
        return True
    else:
        return False
    
#플리 좋아요 상태 확인 함수
def plyylike_status(pidlist,u_uuid)


@app.route('/plyy/api/curator/<c_uuid>', methods = ['get'])
def api_curator(c_uuid):
    play_lists = []
    c_info = curator_info(c_uuid)
    c_plyy = cu_plyy(c_uuid)
    
    for plyy in c_plyy:
        plyy_data = {
                'pid':plyy[0],
                'ptitle':plyy[1],
                'pimg':plyy[2],
                'pgen':plyy[3],
                'pupdate':plyy[4],
                'pcmt':plyy[5],
                'ptag':plyy[8]
        }
        play_lists.append(plyy_data)

    pidlist = [play_lists[i]['pid'] for i in range(len(play_lists))]

    if session:
        if session['id'] != None:
            conn,cur = connect_db()
            cur.execute('SELECT u_uuid from user where u_email = ?',(session['id'],))
            u_uuid = cur.fetchone()['u_uuid']

            c_isliked = curatorlike_status(c_uuid,u_uuid) #True/False
            
            p_isliked = plyylike_status(pidlist,u_uuid)

            conn.close()
    else:
        c_isliked = None



    return jsonify({
        'curator':{
            'c_info':{
            'c_id':c_info[0],
            'c_name':c_info[1],
            'c_img':c_info[2],
            'c_intro':c_info[3],
            'c_tags':c_info[4],
            'c_liked': c_isliked
            },
            'plyy':play_lists
        }
    })



if __name__ == "__main__":
    app.run(debug=True)