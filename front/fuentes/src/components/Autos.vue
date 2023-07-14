<template>
  <div class="container mt-4">
    <div class="row">
      <div class="col-sm-10">
		<div style="display:flex;justify-content:space-between;align-items:center">
			<div><h1>{{nombre}}</h1></div>
			<div>
          <button
          style="float:right"
        	type="button" 
        	class="btn btn-success btn-sm"
        	@click="toggleAddAutoModal($event,-1)">
        	+{{nombre}}
			</button></div>
		</div>
        <hr><br>
        <alert :message="message" v-if="showMessage"></alert>
        <table class="table table-hover">
          <thead>
            <tr>
				<th v-for="colTitulo in autosCol" >{{colTitulo}}</th>
				<th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(auto, index) in autos" :key="index" @click="envioid(auto.id)">
				<td v-for="campo in Object.values(auto)">{{campo}}</td>
              <td>
                <div class="btn-group" role="group">
                  <button 
                  type="button" 
                  class="btn btn-warning btn-sm" 
                  @click="toggleAddAutoModal($event,index)">
                  Actualiza</button>
                  <button 
                  type="button" 
                  class="btn btn-danger btn-sm"
                  @click="eliminaAuto($event,index)">
                  Borra</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
              <!-- add new book modal -->
<div
  ref="addAutoModal"
  class="modal fade"
  :class="{ show: activeAddAutoModal, 'd-block': activeAddAutoModal }"
  tabindex="-1"
  role="dialog">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{formmodo<0?'Agrega':'Modifica'}} {{nombre}}</h5>
        <button
          type="button"
          class="close"
          data-dismiss="modal"
          aria-label="Close"
          @click="toggleAddAutoModal($event)">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <form>
			<div v-for="campo in Object.keys(addAutoForm)">
				<div class="mb-3">
					<label :for="'addAuto'+campo" class="form-label">{{campo}}:</label>
					<input
					type="text"
					class="form-control"
					:id="'addAuto'+campo"
					v-model="addAutoForm[campo]"
					:placeholder="'Ingrese '+ campo">
				</div>
			</div>
          <div class="btn-group" role="group">
            <button
              type="button"
              class="btn btn-primary btn-sm"
              @click="handleAddEnvio">
              Enviar
            </button>
            <button
              type="button"
              class="btn btn-danger btn-sm"
              @click="handleAddReset">
              Reset
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
<div v-if="activeAddAutoModal" class="modal-backdrop fade show"></div>

  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  props:['ruta','nombre','idSync'],
  data() {
    return {
      activeAddAutoModal: false,
      addAutoForm:{
      },	
      formmodo:-1,
      autos: [],
      autosCol:[],
      message: '',
      showMessage: false,
    };
  },
  watch:{
    idSync(id){
      this.getAutos();
    }
  },
  components:{
  	alert:Alert,
  },
  methods: {
	eliminaAuto(event,indice){
      event.stopPropagation();
      const path = this.ruta+this.autos[indice].id;
      axios.delete(path)
        .then((res) => {
          this.message=res.data.mensaje;
          this.showMessage=true;
          setTimeout(()=>this.showMessage=false,3000);
          this.getAutos();
        })
        .catch((error) => {
          console.log(error);
          this.getAutos();
        });
	},
	updateAuto(payload){
      const path = this.ruta+this.autos[this.formmodo].id;
      axios.put(path, this.addAutoForm)
        .then((res) => {
          this.message=res.data.mensaje;
          this.showMessage=true;
          setTimeout(()=>this.showMessage=false,3000);
          this.getAutos();
        })
        .catch((error) => {
          console.log(error);
        });
	},
    addAuto() {
      const path = this.ruta;
        let payload = {}
        Object.assign(payload,this.addAutoForm);
        Object.defineProperty(payload,'idsync',{writable: true,enumerable: true,value: this.idSync})
        axios.post(path, payload)
        .then((res) => {
          this.message=res.data.mensaje;
          this.showMessage=true;
          setTimeout(()=>this.showMessage=false,3000);
          this.getAutos();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getAutos() {
      const path = this.ruta+(this.idSync&&this.idSync!==0?this.idSync:'');

      axios.get(path)
        .then((res) => {
          this.autos = res.data.vehiculos;
          if (this.autos.length==1&&this.autos[0].id==0)
            this.autos.pop();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleAddReset() {
      this.initForm();
    },
    handleAddEnvio() {
      this.toggleAddAutoModal();	
      if (this.formmodo<0){
		    this.addAuto();
      } else {
		    this.updateAuto();
	    }
    },
    initForm() {
	    if (this.formmodo!==undefined){
		    if (this.formmodo<0){
			    for (const propiedad in this.addAutoForm){
				    if (typeof(propiedad)=='number') this.addAutoForm[propiedad]=0;
				    if (typeof(propiedad)=='string') this.addAutoForm[propiedad]='';
			    }
		    } else {
			    for (const propiedad in this.addAutoForm){
				    this.addAutoForm[propiedad]=this.autos[this.formmodo][propiedad];
			    }
		    }
      }
    },
    toggleAddAutoModal(event,modo) {
	    if (modo !== undefined){
        event.stopPropagation();	
		    this.formmodo=modo;
		    this.initForm();
	    }
      const body = document.querySelector('body');
      this.activeAddAutoModal = !this.activeAddAutoModal;
      if (this.activeAddAutoModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
	    }
    },
    envioid(auto_id){
      this.$emit('rId',auto_id);
    }
  },
  created() {
      const path = this.ruta+(this.idSync&&this.idSync!==0?this.idSync:'');
      console.log(this.idSync);
      axios.get(path)
        .then((res) => {
          this.autos = res.data.vehiculos;
          this.autosCol=Object.keys(this.autos[0]);
          for (const [clave,valor] of Object.entries(this.autos[0])){
			      if (clave.indexOf('id')>0||clave.indexOf('id')<0)
				      Object.defineProperty(this.addAutoForm, clave,{enumerable:true, value:valor, writable:true});
          }
          if (this.autos.length==1&&this.autos[0].id==0)
            this.autos.pop();
        })
        .catch((error) => {
          console.error(error);
        });
  },
};
</script>
