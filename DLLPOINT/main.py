from flask import Flask
from flask import render_template
from flask import jsonify
import pymysql.cursors
import collections

app = Flask(__name__)


@app.route('/<tbName>')
@app.route('/<tbName>/<name>')
def index(tbName='wine202', name=None):
    return render_template('index.html', tbName=tbName, name=name)


@app.route('/data/<tbName>/<name>')
def getData(tbName, name):
    connection = pymysql.connect(host='192.168.161.124',
                                 user='dllapi',
                                 password='dllapi',
                                 db='dkc',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "select * from v_{}_dll_depend_all where `dependent_name`=%s or `dependence_name`=%s".format(tbName)
            cursor.execute(sql, (name, name))
            result = cursor.fetchall()
            links = []
            nodes = []
            tmp = set()
            for i in result:
                tmp.add(i['dependent_name'])
                tmp.add(i['dependence_name'])
                links.append({'source': i['dependent_name'], 'target': i['dependence_name'], 'type': '依赖'})
            sql = "select * from v_check_{}_dll_forward_all where `source_dll`=%s or `target_dll`=%s".format(tbName[:4])
            cursor.execute(sql, (name, name))
            result = cursor.fetchall()
            for i in result:
                tmp.add(i['source_dll'])
                tmp.add(i['target_dll'])
                links.append({'source': i['source_dll'], 'target': i['target_dll'], 'type': '转发'})

            # fuck = set()
            # sql = "select * from v_wine202_dll_depend_all"
            # cursor.execute(sql)
            # result = cursor.fetchall()
            # for i in result:
            #     if i['dependent_name'] == name:
            #         fuck.add(i['dependence_name'])
            # for i in result:
            #     if i['dependence_name'] in fuck:
            #         tmp.add(i['dependent_name'])
            #         tmp.add(i['dependence_name'])
            #         links.append({'source': i['dependent_name'], 'target': i['dependence_name'], 'type': '依赖'})
            #
            # fuck = set()
            # sql = "select * from v_check_wine_dll_forward_all"
            # cursor.execute(sql)
            # result = cursor.fetchall()
            # for i in result:
            #     if i['source_dll'] == name:
            #         fuck.add(i['target_dll'])
            # for i in result:
            #     if i['target_dll'] in fuck:
            #         tmp.add(i['source_dll'])
            #         tmp.add(i['target_dll'])
            #         links.append({'source': i['source_dll'], 'target': i['target_dll'], 'type': '转发'})

            for i in tmp:
                nodes.append({"id": i})
    finally:
        connection.close()
    data = {"nodes": nodes, "links": links}
    return jsonify(data)


@app.route('/getNodes/<tbName>')
def getNodes(tbName):
    connection = pymysql.connect(host='192.168.161.124',
                                 user='dllapi',
                                 password='dllapi',
                                 db='dkc',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "select d_name from v_{}_dll".format(tbName)
            cursor.execute(sql)
            result = cursor.fetchall()
            nodes = [i['d_name'] for i in result]
    finally:
        connection.close()
    return jsonify(nodes)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5003)
    # getData('msvcr80.dll.so') # rpcrt4.dll.so
