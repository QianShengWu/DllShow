from flask import Flask
from flask import render_template
from flask import jsonify
import pymysql.cursors
import collections

app = Flask(__name__)


@app.route('/all/<tbName>')
def all(tbName):
    return render_template('all.html', tbName=tbName)


@app.route('/getAllData/<tbName>')
def getAllData(tbName):
    connection = pymysql.connect(host='192.168.161.124',
                                 user='dllapi',
                                 password='dllapi',
                                 db='dkc',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    data = dict()
    nodes = []
    links = []
    try:
        with connection.cursor() as cursor:
            sql = "select * from v_{}_dll_depend_weight".format(tbName)
            cursor.execute(sql)
            result = cursor.fetchall()
            weight = dict()
            for i in result:
                weight[i['dependence_name']] = i['count(*)']
            sql = "select * from v_{}_dll".format(tbName)
            cursor.execute(sql)
            result = cursor.fetchall()
            node = dict()
            for i in result:
                node[i['d_name']] = {'group': i['d_suffix'], 'weight': weight.get(i['d_name'], 0)}

            sql = "select * from v_{}_dll_depend".format(tbName)
            cursor.execute(sql)
            result = cursor.fetchall()

            node_use = set()
            for i in result:
                link = dict()
                link['source'] = i['dependent_name']
                link['target'] = i['dependence_name']
                links.append(link)
                node_use.add(i['dependent_name'])
                node_use.add(i['dependence_name'])

            for i in node_use:
                nodes.append({'id': i, 'group': node[i]['group'], 'weight': node[i]['weight']})
    finally:
        connection.close()
    data['nodes'] = nodes
    data['links'] = links
    return jsonify(data)


@app.route('/<tbName>')
@app.route('/<tbName>/<name>')
def index(tbName=None, name=None):
    return render_template('index.html', tbName=tbName, name=name)


@app.route('/data/<tbName>/<name>')
def getData(tbName, name):
    nodes = dict()
    links = collections.defaultdict(list)
    connection = pymysql.connect(host='192.168.161.124',
                                 user='dllapi',
                                 password='dllapi',
                                 db='dkc',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "select * from v_{}_dll".format(tbName)
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                nodes[i['d_name']] = {'depth': i['d_level'], 'group': i['d_suffix']}
                if tbName == 'wine202': nodes[i['d_name']]['replace_option'] = i['replace_option']

            sql = "select * from v_{}_dll_depend".format(tbName)
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                links[i['dependent_name']].append(i['dependence_name'])
        nodes_n = []
        links_n = collections.defaultdict(list)
        # links = {'A':['B','C','D'],'B':['C','D','E'],'C':['D'],'E':['F']}
        # name = 'A'
        search_name(links, name, nodes_n, links_n)
        # print(nodes_n)
        # print(links_n)
        links_r = []
        nodes_r = []
        for k, v in links_n.items():
            for vi in v:
                links_r.append({'source': k, 'target': vi})
        # print(nodes_n)
        for i in nodes_n:
            tmp = {'id': i, 'group': nodes[i]['group'], 'depth': nodes[i]['depth']}
            if tbName == 'wine202': tmp['replace_option'] = nodes[i]['replace_option']
            nodes_r.append(tmp)
        # print(nodes_r)
        # print(links_r)
        data = {'nodes': nodes_r, 'links': links_r}
        # print(data)
    finally:
        connection.close()
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


def search_name(links, name, nodes_n, links_n):
    if name not in nodes_n:
        nodes_n.append(name)
    for i in links.get(name, []):
        links_n[name].append(i)
        if i not in nodes_n:
            search_name(links, i, nodes_n, links_n)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
    # getData('actxprxy.dll')
