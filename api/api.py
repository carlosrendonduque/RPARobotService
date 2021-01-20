import flask
from flask import request, jsonify
import sqlite3
import pyodbc
import json
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def get_data(emp, ano, mes, id_con_cco, tope):    
    server = '172.17.7.26' 
    database = 'Adv_Condor_soporte' 
    username = 'usuariodms' 
    password = 'Usu2017*dms' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    SQL = "execute GetCnsValidacionJornadasTope " + emp + ", " + ano + ", " + mes + ", " + id_con_cco + ", " + tope + ""
    # print(SQL)
    cursor.execute("execute GetCnsValidacionJornadasTope " + emp + ", " + ano + ", " + mes + ", " + id_con_cco + ", " + tope + "")
    cursor.close()
    cursor = cnxn.cursor()
    cursor.execute('select * from rpa_cns_liquidacion')
    cursor_list = cursor.fetchall()
    results = json.dumps(cursor_list.find())
    
    return  results
    



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>RPA Validation Report</h1>
<p>A prototype API for RPA Validation Report.</p>'''


@app.route('/api/v1/resources/jobs_validation/all', methods=['GET'])
def get_all_jobs_report():    
    server = '172.17.7.26' 
    database = 'Adv_Condor_soporte' 
    username = 'usuariodms' 
    password = 'Usu2017*dms' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    # cnxn.row_factory = dict_factory
    # cursor = cnxn.cursor()
    # emp = '3'   
    # ano = '2021'    
    # mes = '1' 
    # id_con_cco  = '994'
    # tope  = '60'
    # SQL = "execute GetCnsValidacionJornadasTope " + emp + ", " + ano + ", " + mes + ", " + id_con_cco + ", " + tope + ""
    # # print(SQL)
    # cursor.execute("execute GetCnsValidacionJornadasTope " + emp + ", " + ano + ", " + mes + ", " + id_con_cco + ", " + tope + "")
    # cursor.close()



    cursor = cnxn.cursor()
    result =cursor.execute('select * from RPA_GetCnsValidacionJornadasTope')
    items=[]
    for row in result:
        d = collections.OrderedDict()
        d['emp'] = row[0]
        d['ano'] = row[1]
        d['mes'] = row[2]
        d['id_con_cco'] = row[3]
        d['tope'] = row[4]
        items.append(d)

    # r = [dict((cursor.description[i][0], value) \
    #               for i, value in enumerate(row)) for row in cursor.fetchall()]
    # json_output = json.dumps(r)
    
    json_output = json.dumps(items)
    return  json_output

    # cnxn.row_factory = dict_factory
    # cur = cnxn.cursor()
    # all_jobs = cur.execute('select * from rpa_cns_liquidacion').fetchall()

    # return jsonify(all_jobs)


@app.route('/api/v1/resources/bots_validation/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()