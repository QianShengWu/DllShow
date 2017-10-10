from flask import Flask
from flask import render_template
from dllpoint.dllpoint import dllpoint
from dllapi.dllapi import dllapi
from dllforward.dllforward import dllforward
from dllgraph.dllgraph import dllgraph

app = Flask(__name__, template_folder='templates')

app.register_blueprint(dllpoint, url_prefix='/dllpoint')
app.register_blueprint(dllapi, url_prefix='/dllapi')
app.register_blueprint(dllforward, url_prefix='/dllforward')
app.register_blueprint(dllgraph, url_prefix='/dllgraph')

@app.route('/')
def index():
	return render_template('dllshow/index.html')
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('dllshow/404.html'), 404
	
if __name__=='__main__':
  app.run(debug=True, host='0.0.0.0')
