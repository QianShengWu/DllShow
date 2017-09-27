from flask import Flask
from flask import render_template
from flask import jsonify
import pymysql.cursors

app = Flask(__name__)

#v_check_wine_dll_forward_order
#v_check_wine_dll_forward_order_basic_source
#v_check_wine_dll_forward_order_basic_target
@app.route('/<name>')
def index(name):
    return render_template('index.html', name=name)


@app.route('/data/<name>')
def getData(name):
    connection = pymysql.connect(host='192.168.161.124',
                                 user='dllapi',
                                 password='dllapi',
                                 db='dkc',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "select * from {}_weight".format(name)
            cursor.execute(sql)
            result = cursor.fetchall()
            weight = dict()
            for i in result:
                weight[i['target_dll']] = i['count(*)']

            sql = 'select * from ' + name
            cursor.execute(sql)
            result = cursor.fetchall()
            tmp = set()
            for i in result:
                tmp.add(i['source_dll'])
                tmp.add(i['target_dll'])
            nodes = []
            links = []
            for i in tmp:
                nodes.append({'id': i, 'weight':weight.get(i, 0)})
            #print(nodes)
            for i in result:
                links.append({'source': i['source_dll'], 'target': i['target_dll'], 'value': int(i['forward_count'])})
            data = {'nodes': nodes, 'links': links}
    finally:
        connection.close()
    #print(data)
    return jsonify(data)


if __name__ == '__main__':
    # getData()
    app.run(debug=True, host='0.0.0.0')
