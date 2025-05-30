<template>
    <v-container >
        <snackbar :type="notificationType" :message="notificationMessage" :show="showNotification" />
              <v-card variant="outlined" width="100%" height="100%" class="fill-width d-flex flex-column" style="width: 100% !important;" >
                <v-card-title>
                  <v-row>
                      <v-col cols="6" align="left" class="mb-0 pb-0">
                        <h1 class="text-h5">Venta: #{{ venta.id }}</h1>
                      </v-col>
                      <v-col cols="6" align="right" class="mb-0 pb-0">
                        <h1 class="text-h5">Total: {{ formatCurrency(venta.total) }}</h1>
                      </v-col>
                       <v-col cols="6" align="left" class="mt-0 pt-0">
                        <v-chip
                            v-if="venta.estatus === 'pendiente'"
                            
                            color="orange"
                            label="Pendiente"
                            variant="outlined"
                            prepend-icon="mdi-alert"

                            class="ma-2">
                            {{ venta.estatus }}
                        </v-chip>
                        <v-chip
                            v-if="venta.estatus === 'servicio domicilio'"
                            
                            color="grey"
                            label="servicio a domicilio"
                            variant="outlined"
                            prepend-icon="mdi-moped-outline"

                            class="ma-2">
                            {{ venta.estatus }}
                        </v-chip>
                        <v-chip
                            v-if="venta.estatus === 'cobrado'"
                            
                            color="green"
                            label="cobrado"
                            variant="outlined"
                            prepend-icon="mdi-archive-check"

                            class="ma-2">
                            {{ venta.estatus }}
                        </v-chip>
                      
                        <v-chip

                            v-else-if="venta.estatus === 'activo'"

                            variant="outlined"
                            color="blue"
                            label="Activo"
                            prepend-icon="mdi-check"
                            class="ma-2">
                          
                            {{ venta.estatus }}
                            
                        </v-chip>
                        <v-chip
                            v-else-if="venta.estatus === 'cancelado'"
                            variant="outlined"
                            color="red"
                            label="Pagado"
                            class="ma-2">
                          
                            {{ venta.estatus }}
                            
                        </v-chip>
                        
                      </v-col>
                  </v-row>
                 


                

                            
                </v-card-title>
                <v-card-text class="flex-grow-1 overflow-y-auto" >
                    <v-row>
                <v-col cols="2" >
                  
                  <v-list height="100%" class="bg-red">
                    <v-list-item class="d-flex justify-center pa-3 ">
                      <v-icon @click="page = 1" class="cursor-pointer" size="30" icon="mdi-cart"></v-icon>
                    </v-list-item>
                    <v-list-item class="d-flex justify-center pa-3 ">
                      <v-icon @click="page = 3" class="cursor-pointer" size="30" icon="mdi-account"></v-icon>
                    </v-list-item>
                    
                    <v-list-item class="d-flex justify-center pa-3 ">
                        <v-icon @click="page=4" icon="mdi-multicast" class="cursor-pointer" size="30"></v-icon>
                    </v-list-item>

                  </v-list>
                </v-col>
                <v-col cols="10" >
                
                    <v-card-text v-if="page === 1" class="flex-grow-1 overflow-y-auto">
                      <v-card>
                        <v-card-title class="d-flex justify-center">
                            <h1 class="text-h5">Productos</h1>
                        </v-card-title>
                        <v-data-table height="100%" variant="outlined" class="pa-2 bg-white " :items="order" hide-default-footer >
                        </v-data-table>
                      </v-card>


                    </v-card-text>
    
                    <v-card-text v-if="page === 3" class="flex-grow-1 overflow-y-auto">

                        <!-- <v-card v-if="venta.clientes" variant="outlined bg-white ma-3">
                            <v-card-title class="d-flex justify-center">
                                <h1 class="text-h5">Cliente</h1>
                            </v-card-title>
                            <v-card-text>
                                <v-row>
                                    <v-col cols="12">
                                        <div align="">
                                            {{ venta.clientes.nombre }}
                                        </div>
                                    </v-col>
                                    <v-col cols="6">
                                        <div v-if="venta.clientes.nickname" align="">
                                            {{ (venta.clientes.nickname) }}
                                        </div>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card> -->
                        
                        <aplicarDescuento   @actualizado="refresh" :venta="venta" />
                    
                    </v-card-text>
                 
                    <v-card-text v-if="page === 4" class="flex-grow-1 overflow-y-auto">
                        <v-row>
                            <v-col cols="12">
                                <v-btn color="red" @click="changeStatus('cancelado')" block append-icon="mdi-cancel" variant="outlined">Cancelar</v-btn>
                                </v-col>
                            <v-col cols="12">
                                <v-btn color="warning"  @click="changeStatus('pendiente')" variant="outlined" block append-icon="mdi-alert">Pendiente</v-btn>
                            </v-col>
                            <v-col cols="12">
                                <v-btn color="grey" @click="changeStatus('servicio domicilio')" block append-icon="mdi-moped-outline" variant="outlined">Para entrega</v-btn>
                            </v-col>
                            <v-col>
                                <v-btn color="blue" @click="print = true" block append-icon="mdi-printer" variant="outlined">imprimir</v-btn>
                               <v-dialog persistent v-model="print" max-width="500px">
                                    <printing @close="print = false"  :venta="venta"></printing>
                                </v-dialog>
                            </v-col>
                           
                        </v-row>
                    </v-card-text>
                </v-col>
              </v-row>
                </v-card-text>
            </v-card>
             
    </v-container>

</template>
<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import supabase from '@/supabase';
import formatCurrency from '@/composables/formatCurrency';
import aplicarDescuento from '../clientes/aplicarDescuento.vue';
import { getMexicoLocalString } from '@/composables/localtime'
import snackbarfrom from '@/components/snackbar.vue';
import printing from './printing.vue';

const print = ref(false);

const showNotification = ref(false);
const notificationType = ref('');
const notificationMessage = ref('');

const emits = defineEmits(['cancel_sale', 'procesarPago', 'finished', 'updateVenta']);


const finish = () => {
    emits('finished');
    showNotification.value = false;
}

const pending  = async () => {
  const { data, error } = await supabase
    .from('ventas')
    .update({ estatus: 'pendiente' })
    .eq('id', venta.value.id)
    .select()
    .single();
  if (error) {
    mostrarNotificacion('error', 'Error al marcar como pendiente');
  } else {
    emits('finished') 
}};


const page = ref(1);

const headers = [
  { text: 'Nombre', value: 'nombre' },
  { text: 'Precio', value: 'precio' },
  { text: 'Peso', value: 'peso' },
  { text: 'Total', value: 'total' }
];



const metodo_de_pago = ref({
  total: 0,
  efectivo: 0,
  tarjeta: 0,
  transferencia: 0
});

const pagado = async () => {
  const { data, error } = await supabase.from('ventas').update({ estatus: 'pagado' }).eq('id', venta.value.id).select().single();
  if (error) {
    mostrarNotificacion('error', 'Error al marcar como pagado');
  } else {
    emits('finished', data);
    mostrarNotificacion(true);
    notificationType.value = 'success';
    notificationMessage.value = 'Venta marcada como pagado';
    get_ventas();
  }
};

const get_sale = async (id) => {
  const { data, error } = await supabase
    .from('ventas')
    .select(
        `*, 
        producto_ventas(
        *, 
        productos(*)),
        pagos(*),
        clientes(*)
        `
    )
    .eq('id', id)
    .single();
    

  if (error) {
    console.error('Error al obtener la venta:', error);
  } else {
    venta.value = data;
    if (data.pagos.length > 0) {
      existingPayments.value = true;
    }
    return data;
  }
};
const props = defineProps({
  venta: {
    type: Object,
    required: true
  }
});

const verify_payment = () => {
    
    
    if (pago.value.cantidad > payment.restante) {
        console.log('pago correcto');
        return true;
        
    } else {
        console.log('pago incorrecto');
        return false;
    }
}

const bill_sale = async () => {
    let liquidacion = verify_payment();
    if (!liquidacion) {
        console.log('pago correcto');
        const { data, error } = await supabase
            .from('pagos')
            .insert({
                created_at: getMexicoLocalString(),
                metodo: pago.value.metodo,
                total: payment.value.restante,
                venta_id: venta.value.id,
                pendiente: 0
            })
            .select()
            .single();
        if (error) {
            console.error('Error al registrar el pago:', error);
        } else {
            console.log('Pago registrado:', data);
            venta.value.pagos.push(data);
            pago.value.cantidad = 0;
            pago.value.metodo = '';
            await update_sale(venta.value);
        }
    } else {
        const { data, error } = await supabase
            .from('pagos')
            .insert({
                created_at: getMexicoLocalString(),
                metodo: pago.value.metodo,
                total: pago.value.cantidad,
                venta_id: venta.value.id,
                pendiente: 0
            })
            .select()
            .single();
    }
};




const update_sale = async (venta) => {
    const { data, error } = await supabase
        .from('ventas')
        .update({
            estatus: 'cobrado'
        })
        .eq('id', venta.id)
        .select()
        .single();
    if (error) {
        console.error('Error al cobrar la venta:', error);
    } else {
        venta.value.estatus = 'cobrado';
    }
};


const changeStatus = async (status) => {
  if(status === 'cancelado'){
    await cancel_sale();
    return;
  }
    const { data, error } = await supabase
        .from('ventas')
        .update({ estatus: status })
        .eq('id', venta.value.id)
        .select(
            `*, 
            producto_ventas(
            *, 
            productos(*)),
            pagos(*),
            clientes(*)`
        )
        .single();
    if (error) {
        console.error('Error al cambiar el estatus de la venta:', error);
    } else {
        showNotification.value = true;
        notificationType.value = 'success';
        notificationMessage.value = `Estatus cambiado a ${status}`;
        console.log('Estatus cambiado:', data);
        venta.value.estatus = status;
        
    }
};


const refresh = () => {
    get_sale(venta.value.id);
    page.value = 1;
    mostrarNotificacion('success', 'Venta actualizada');
};

const payment = computed(() => {
    let pagado=  venta.value.pagos.reduce((acc, pago) => acc + pago.total, 0)
    let restante = venta.value.total - pagado
    let cambio = 0

    return {
        pagado,
        restante,
        cambio
    }
});

const cancel_sale = async () => {
    const { data, error } = await supabase
        .from('ventas')
        .update({
            estatus: 'cancelado'
        })
        .eq('id', venta.value.id)
        .select()
        .single();
    if (error) {
        console.error('Error al cancelar la venta:', error);
    } else {
        console.log('Venta cancelada:', data);
        showNotification.value = true;
        notificationType.value = 'error';
        notificationMessage.value = 'Venta cancelada'; 
        emits('finished');
        get_sale(venta.value.id);

    }
};

const order = computed(() => {
  return venta.value.producto_ventas.map((producto) => ({
    nombre: producto.productos.nombre,
    precio: producto.precio,
    peso: producto.peso,
    total: producto.total
  }));
});

const pago = ref({
    cantidad: 0,
    metodo: '',
}
)

const venta = ref(props.venta);
const existingPayments = ref(false)

onMounted(() => {
  console.log('mounted');
    if(props.venta.pagos.length > 0){
        existingPayments.value = true
    }
});

watch(
  () => props.venta,
  (newValue) => {
    if (newValue) {
      get_sale(newValue.id);
    }
  },
  { immediate: true }
);

</script>