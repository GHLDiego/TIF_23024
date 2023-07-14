import sqlite3
import init_tables
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from os.path import exists
					 
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

init_tables.init_tables()

campos={'tabla':'vehiculos','columnas':{'marca':'','modelo':'','anio':0,'importe':0.0}}
manten={'tabla':'mantenimientos','columnas':{'detalle':'','importe':0.0}}
empl={'tabla':'empleados','columnas':{'nombre':'','apellido':'','domicilio':'','localidad':''}}
# sanity check route

@app.route('/')
def home():
	return render_template('index.html')

tabla_campos_cap=campos['tabla'][:len(campos['tabla'])-1].capitalize()
@app.route('/'+campos['tabla']+'/<auto_id>', methods=['GET'])
def especif_campos(auto_id):
	response_object = {'estado': 'exito'}
	response_object['vehiculos']=query_select(campos, auto_id)
	return jsonify(response_object)
@app.route('/'+campos['tabla']+'/', methods=['GET', 'POST'])
def all_campos():	
	response_object = {'estado': 'exito'}
	if request.method == 'POST':
		data_insert=query_insert(request.get_json(),campos)
		response_object['mensaje'] = tabla_campos_cap+' agregado!'
	else:
		response_object['vehiculos']=query_select(campos,auto_id=0)
	return jsonify(response_object)
@app.route('/'+campos['tabla']+'/<auto_id>', methods=['PUT','DELETE'])
def act_campos(auto_id):
	response_object = {'status': 'success'}
	if request.method == 'PUT':
		data_put=query_put(request.get_json(),campos,auto_id)
		response_object['mensaje'] = tabla_campos_cap+' actualizado!'
		return jsonify(response_object)
	else:
		data_delete=query_delete(campos,auto_id)
		response_object['mensaje'] = tabla_campos_cap+' eliminado!'
		return jsonify(response_object)

tabla_empl_cap=empl['tabla'][:len(empl['tabla'])-1].capitalize()
@app.route('/'+empl['tabla']+'/<auto_id>', methods=['GET'])
def especif_empl(auto_id):
	response_object = {'estado': 'exito'}
	response_object['vehiculos']=query_select(empl, auto_id)
	return jsonify(response_object)
@app.route('/'+empl['tabla']+'/', methods=['GET', 'POST'])
def all_empl():	
	response_object = {'estado': 'exito'}
	if request.method == 'POST':
		data_insert=query_insert(request.get_json(),empl)
		response_object['mensaje'] = tabla_empl_cap+' agregado!'
	else:
		response_object['vehiculos']=query_select(empl,auto_id=0)
	return jsonify(response_object)
@app.route('/'+empl['tabla']+'/<auto_id>', methods=['PUT','DELETE'])
def act_empl(auto_id):
	response_object = {'status': 'success'}
	if request.method == 'PUT':
		data_put=query_put(request.get_json(),empl,auto_id)
		response_object['mensaje'] = tabla_empl_cap+' actualizado!'
		return jsonify(response_object)
	else:
		data_delete=query_delete(empl,auto_id)
		response_object['mensaje'] = tabla_empl_cap+' eliminado!'
		return jsonify(response_object)

tabla_manten_cap=manten['tabla'][:len(manten['tabla'])-1].capitalize()
@app.route('/'+manten['tabla']+'/<auto_id>', methods=['GET'])
def especif_manten(auto_id):
	response_object = {'estado': 'exito'}
	response_object['vehiculos']=query_select(manten, auto_id)
	return jsonify(response_object)
@app.route('/'+manten['tabla']+'/', methods=['GET', 'POST'])
def all_manten():	
	response_object = {'estado': 'exito'}
	if request.method == 'POST':
		data_insert=query_insert(request.get_json(),manten)
		response_object['mensaje'] = tabla_manten_cap+' agregado!'
	else:
		response_object['vehiculos']=query_select(manten,auto_id=0)
	return jsonify(response_object)
@app.route('/'+manten['tabla']+'/<auto_id>', methods=['PUT','DELETE'])
def act_manten(auto_id):
	response_object = {'status': 'success'}
	if request.method == 'PUT':
		data_put=query_put(request.get_json(),manten,auto_id)
		response_object['mensaje'] = tabla_manten_cap+' actualizado!'
		return jsonify(response_object)
	else:
		data_delete=query_delete(manten,auto_id)
		response_object['mensaje'] = tabla_manten_cap+' eliminado!'
		return jsonify(response_object)

"""**********************************************************************"""

def query_insert(fn_post_data,fn_campos):
		datos=[]
		prev=0
		query_par=''
		query_insert='insert into '+fn_campos['tabla']+' ('
		query_campos=''
		# insert into vehiculos (campo,campo,campo) values (?,?,?)
		for tmp_campo in  fn_campos['columnas']:
			if isinstance(fn_campos['columnas'][tmp_campo],(str)):
				datos.append(fn_post_data.get(tmp_campo))
			if isinstance(fn_campos['columnas'][tmp_campo],(int)):
				datos.append(int(fn_post_data.get(tmp_campo)))
			if isinstance(fn_campos['columnas'][tmp_campo],(float)):
				datos.append(float(fn_post_data.get(tmp_campo)))
			query_par+=','if prev>0 else ''
			query_campos+=','if prev>0 else ''
			query_campos+=tmp_campo
			query_par+='?'
			prev=1			
		if fn_post_data.get('idsync') is not None:
			datos.append(int(fn_post_data.get('idsync')))
			query_campos+=',idsync'
			query_par+=',?'
		query_insert+=query_campos+')values('+query_par+')'
		print(query_insert)
		#insert into vehiculos (marca,modelo,anio,importe)values(?,?,?,?)',(tuple(datos)))
		try:
			with sqlite3.connect('database.db') as con:
				cur=con.cursor()
				cur.execute(query_insert,tuple(datos))
				con.commit()
				cur.close()
		except:
			con.rollback()
		finally:
			con.close()
		return({'query':query_insert,'params':tuple(datos)})

def query_put(fn_post_data,fn_campos,id_col):
		datos=[]
		prev=0
		queryPut='update '+fn_campos['tabla']+' set '
		for tmp_campo in  fn_campos['columnas']:
			if isinstance(fn_campos['columnas'][tmp_campo],(str)):
				datos.append(fn_post_data.get(tmp_campo))
			if isinstance(fn_campos['columnas'][tmp_campo],(int)):
				datos.append(int(fn_post_data.get(tmp_campo)))
			if isinstance(fn_campos['columnas'][tmp_campo],(float)):
				datos.append(float(fn_post_data.get(tmp_campo)))
			queryPut+= ', 'if prev>0 else ''
			queryPut+=tmp_campo+'=?'
			prev=1
		datos.append(id_col)
		queryPut+=' where id=?'
		print('query put:',queryPut)
		try:
			with sqlite3.connect('database.db') as con:
				cur=con.cursor()
				cur.execute(queryPut, tuple(datos))
				con.commit()
				cur.close()
		except:
			con.rollback()
		finally:
			con.close()
		return({'query':queryPut,'params':tuple(datos)})

def query_delete(fn_campos,id_col):
		queryDelete='delete from '+fn_campos['tabla']+' where id=?'
		print(queryDelete,type(int(id_col)))
		try:
			with sqlite3.connect('database.db') as con:
				cur=con.cursor()
				cur.execute(queryDelete,(int(id_col),))
				con.commit()
				cur.close()
		except:
			con.rollback()
		finally:
			con.close()	

def query_select(fn_campos,auto_id):
		AUTOS = []
		query_select='select id'
		prev=0
		for tmp_campo in  fn_campos['columnas']:
			query_select+=','+tmp_campo
		query_select+=' from '+fn_campos['tabla']
		if int(auto_id)!=0:
			query_select+=' where idsync='+auto_id
		con=sqlite3.connect('database.db')
		cur=con.cursor()
		cur.execute(query_select)
		filas=cur.fetchall()
		print(query_select)
		print(filas)
		#select id,marca,modelo,importe,anio from vehiculos
		if len(filas)>0:
			for auto in filas:
				indice=0
				campos_select={}
				campos_select['id']=auto[indice]
				for tmp_campo in  fn_campos['columnas']:
					indice+=1
					campos_select[tmp_campo]=auto[indice]
				AUTOS.append(campos_select)	
		else:
			campos_select={}
			campos_select['id']=0
			for tmp_campo in  fn_campos['columnas']:
				if isinstance(fn_campos['columnas'][tmp_campo],(str)):
					campos_select[tmp_campo]=''
				if isinstance(fn_campos['columnas'][tmp_campo],(int)):
					campos_select[tmp_campo]=0
				if isinstance(fn_campos['columnas'][tmp_campo],(float)):
					campos_select[tmp_campo]=0.0
			AUTOS.append(campos_select)
		cur.close()
		con.close()
		return (AUTOS)


if __name__ == '__main__':
    app.run()

