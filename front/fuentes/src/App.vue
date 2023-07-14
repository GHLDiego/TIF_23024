<template>
<div class="container">
    <div class="row">
		<h1 class="text-center">LA API REST EN FLASK</h1>
		<p>En este primer bloque de codigo se declaran las tablas que se van a exponer en la API</p>
<p><b>campos={'tabla':'vehiculos','columnas':{'marca':'','modelo':'','anio':0,'importe':0.0}}<br>
manten={'tabla':'mantenimientos','columnas':{'detalle':'','importe':0.0}}<br>
empl={'tabla':'empleados','columnas':{'nombre':'','apellido':'','domicilio':'','localidad':''}}</b><br></p>
<p>En este codigo se toma el nombre de la tabla se lo transforma en singular y se lo capitaliza de forma que se puedan formar los respectivos mensajes 'Vehiculo agregado!', 'Vehiculo eliminado!' y asi sucesivamente con el resto</p>
<p><b>tabla_campos_cap=campos['tabla'][&#58;len(campos['tabla'])-1].capitalize()</b></p>

<p>De aca en adelante se declaran cada una de las rutas y los metodos de acceso a la api y todos son relativos al nombre de la tabla arriba declarada<br>Cabe destacar que el nombre de la variable que almacena la descripcion de la tabla, '<b>campos</b>' en este ejemplo, forma parte de los nombres de todas las variables y funciones que definen cada ruta de la API, permitiendonos hacer un copiar y pegar para la siguiente tabla solo reemplazando la palabra <b>campo</b> por la palabra <b>manten</b> en el codigo duplicado y asi obtenemos todas las rutas para la tabla mantenimientos por ejemplo segun las declaraciones arriba expuestas </p>
<p><b>@app.route('/'+campos['tabla']+'/&lt;auto_id&gt;', methods=['GET'])<br>
def especif_campos(auto_id):<br>
<span style="margin-left:50px">response_object = {'estado': 'exito'}</span><br>
<span style="margin-left:50px">response_object['vehiculos']=query_select(campos, auto_id)</span><br>
<span style="margin-left:50px">return jsonify(response_object)</span><br>
</b></p><br><br>
<p>Todas las instrucciones SQL se arman concatenando los campos declarados arriba, quiere decir que sacar una columna en la declaracion de la tabla hace que que se ajusten todos los comandos SQL y ya ese campo no sea incluido<br></p>
<h1 class="text-center">EL CLIENTE EN VUEjs</h1>
<p>
Cada CRUD de cada tabla expuesta en la api se ajusta automaticamente sin configurar ni declarar absolutamente nada y lo hace valiendose solamente del json recivido ajustando todos los campos de los formularios de altas y bajas como asi tambien los campos exhibidos en la tabla<br><br>

Los CRUD pueden ser totalmente independientes unos de otros o se pueden sincronizar en una relacion de uno a muchos de forma tal que la tabla hija exhiba solamente los registros que solo le corresponden al registro seleccionado en la tabla padre<br><br>
<b>&lt;autos :idSync="id_sync_auto" nombre="Vehiculos" ruta=" https://villarroeldiego.pythonanywhere.com/vehiculos/" /&gt;</b><br>
<b>&lt;autos :idSync="id_sync_mant" nombre="Mantenimientos" ruta=" https://villarroeldiego.pythonanywhere.com/mantenimientos/" /&gt;</b><br>
<b>&lt;autos :idSync="id_sync_empl" nombre="Empleados" ruta=" https://villarroeldiego.pythonanywhere.com/empleados/" /&gt;</b><br>
</p>
<h1 class="text-center">EJEMPLO DE TABLAS INSTANCIADAS SIN RELACION</h1>
	</div>
</div>
	<autos :idSync="id_sync_auto" nombre="Vehiculos" ruta=" https://villarroeldiego.pythonanywhere.com/vehiculos/"/>
	<autos :idSync="id_sync_mant" nombre="Mantenimientos" ruta=" https://villarroeldiego.pythonanywhere.com/mantenimientos/" />
	<autos :idSync="id_sync_empl" nombre="Empleados" ruta=" https://villarroeldiego.pythonanywhere.com/empleados/" />

<h1 class="text-center mt-4">EJEMPLO DE TABLAS CON RELACION UNO A VARIOS</h1>
<h4 class="text-center">Hacer click en cada auto para ver sus respectivos mantenimientos</h4>
<autos :idSync="id_sync_aut2" nombre="Vehiculos" ruta=" https://villarroeldiego.pythonanywhere.com/vehiculos/" @rId="recivoId"/>
<autos :idSync="id_sync_man2" nombre="Mantenimientos" ruta=" https://villarroeldiego.pythonanywhere.com/mantenimientos/" />
</template>

<script>
import Autos from './components/Autos.vue'

export default{
	components:{
		autos: Autos,
	},
	data(){
		return {
			id_sync_aut2:0,
			id_sync_man2:-1
		}
	},
	methods:{
		recivoId(regId){
			this.id_sync_man2=regId;
		}
	}
};

</script>

<style></style>
