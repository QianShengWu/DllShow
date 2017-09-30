from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Blueprint
import pymysql.cursors
import collections
import json

dllapi = Blueprint('dllapi', __name__,
                        template_folder='templates')

@dllapi.route('/<tbName>/<flag>')
@dllapi.route('/<tbName>/<flag>/<dllName>/<apiName>')
def index(tbName=None, flag=1,dllName=None, apiName=None):
    return render_template('dllapi/index.html', tbName=tbName, flag=flag, dllName=dllName,apiName=apiName)


@dllapi.route('/data/<tbName>/<flag>/<dllName>/<apiName>')
def data(tbName=None, flag=1, dllName=None, apiName=None):
    return jsonify(getData(tbName, dllName, apiName, int(flag)))


@dllapi.route("/getNodes/<tbName>/<flag>")
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
