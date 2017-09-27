from flask import Flask
from flask import render_template
from flask import jsonify
import pymysql.cursors
import collections
import json

app = Flask(__name__)

@app.route('/<tbName>/<flag>')
@app.route('/<tbName>/<flag>/<dllName>/<apiName>')
def index(tbName=None, flag=1,dllName=None, apiName=None):
    return render_template('index.html', tbName=tbName, flag=flag, dllName=dllName,apiName=apiName)


@app.route('/data/<tbName>/<flag>/<dllName>/<apiName>')
def data(tbName=None, flag=1, dllName=None, apiName=None):
    return jsonify(getData(tbName, dllName, apiName, int(flag)))


@app.route("/getNodes/<tbName>/<flag>")
def getNodes(tbName=None, flag=1):
    return jsonify(getNodesData(tbName, int(flag)))


# def getData(dllName, apiName):
#     data = dict()
#     connection = pymysql.connect(host='192.168.161.124',
#                                  user='dllapi',
#                                  password='dllapi',
#                                  db='dkc',
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT CONCAT(dllname1,'->',apiname1) as node1, CONCAT(dllname2,'->',apiname2) as node2" \
#                   " FROM `v_check_wine_api_forward_2` WHERE `dllname1`=%s and `apiname1`=%s"
#             cursor.execute(sql, (dllName, apiName))
#             result = cursor.fetchone()
#             data['nodes'] = [{'id': result['node1']}, {'id': result['node2']}]
#             data['links'] = [{'source': result['node1'], 'target': result['node2']}]
#     finally:
#         connection.close()
#     return data


def getData(tbName, dllName, apiName, flag=1):
    connection = pymysql.connect(host='192.168.161.124',
                                 user='dllapi',
                                 password='dllapi',
                                 db='dkc',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `v_check_{}_api_forward_%s` WHERE `dllname1`=%s and `apiname1`=%s".format(tbName[:4])
            cursor.execute(sql, (flag, dllName, apiName))
            result = cursor.fetchone()
            nodes = []
            links = []
            tmp = list([] if not result else result.values())
            for i in range(0, len(tmp), 2):
                nodes.append({'id': tmp[i] + '->' + tmp[i + 1]})
            #print(nodes)
            tmp = [i['id'] for i in nodes]
            for i in range(len(tmp) - 1):
                links.append({'source': tmp[i], 'target': tmp[i + 1]})
            data = {'nodes': nodes, 'links': links}

    finally:
        connection.close()
    return data

def getNodesData(tbName, flag=1):
    connection = pymysql.connect(host='192.168.161.124',
                                 user='dllapi',
                                 password='dllapi',
                                 db='dkc',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT dllname1,apiname1 FROM `v_check_{}_api_forward_%s`".format(tbName[:4])
            cursor.execute(sql, (flag,))
            result = cursor.fetchall()
            data = []
            nodes = collections.defaultdict(list)
            for i in result:
                nodes[i['dllname1']].append(i['apiname1'])
            for k, v in nodes.items():
                data.append({'dllName':k,'apiName':[vi for vi in v]})
    finally:
        connection.close()
    return data


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
    # print(getData('api-ms-win-core-string-l1-1-0.dll', 'CompareStringEx', 1))
    # print(getData('imagehlp.dll', 'SymMatchString', 2))
    # print(getData('api-ms-win-crt-string-l1-1-0.dll', 'strcat', 3))
    # data = getNodesData(1)
    # with open('tmp.json', 'w') as f:
    #     json.dump(data, fp=f, indent=4)