import sqlite3

def init_tables():
		con=sqlite3.connect('database.db')
		cur=con.cursor()
		cur.execute('create table if not exists \
			vehiculos(id integer primary key autoincrement, idsync integer,marca text,modelo text,anio int,importe decimal(10,2));')
		con.commit()
		cur.execute("""select * from vehiculos""")
		if len(cur.fetchall())==0:
			cur.execute("insert into vehiculos (marca,modelo,anio,importe)values('FIAT','PUNTO',1995,1550000),('RENAULT','MEGANE',1998,1750000);")
			con.commit()

		cur.execute('create table if not exists \
			mantenimientos(id integer primary key autoincrement, idsync integer, km integer,proveedor,detalle text,importe decimal(10,2));')
		con.commit()
		cur.execute("""select * from mantenimientos""")
		if len(cur.fetchall())==0:
			cur.execute("insert into mantenimientos (km,detalle,importe)values(10000,'cbio de aceite',4500),(20000,'cbio correa distrib',20000);")
			con.commit()

		cur.execute('create table if not exists \
			empleados(id integer primary key autoincrement, idsync integer, nombre text,apellido text,edad int, domicilio text,localidad text);')
		con.commit()
		cur.execute("""select * from empleados""")
		if len(cur.fetchall())==0:
			cur.execute("insert into empleados (nombre,apellido,edad,domicilio,localidad)values('Diego','Villar',51,'San Martin 1234','Caseros'),('Ana','Aguirre',45,'Hornos 2250','Palomar');")
			con.commit()
		cur.close()
		con.close()