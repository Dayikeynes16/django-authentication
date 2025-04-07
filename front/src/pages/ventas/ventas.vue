<template>
    <v-container>
   <v-row>
   <v-col cols="6">
   <v-card  height="150px" variant="outlined" v-for="(venta, index) in ventas" :key="venta.id" class="ma-4">
   <v-card-title>Balanza: {{ venta.balanza }} -- # {{ venta.id }}</v-card-title>
   <v-card-text>
   <v-dialog v-model="venta.dialog" max-width="600px">
   <v-card>
   <v-card-text>
   <table class="table table-hover">
   <thead>
    <th>Productos</th>
    <th>Precio</th>
    <th>Peso</th>
    <th>Subtotal</th>
    <th>total</th>
   </thead>
   <tbody>
   <tr v-for="producto in venta.producto_ventas" :key="producto.id">
   <td>{{ producto.productos.nombre }}</td>
   <td>{{ formatCurrency(producto.precio) }}</td>
   <td>{{ producto.peso }}Kg</td>
   <td>{{ formatCurrency(producto.total) }}</td>
   <td></td>
   </tr>
   <tr>
   <td></td>
   <td></td>
   <td></td>
   <td></td>
   <td>{{ formatCurrency(venta.total) }}</td>
   </tr>
   </tbody>
   </table>
   </v-card-text>
   <v-card-actions>
   <v-btn color="red" variant="outlined" @click="bill_sale(venta, 'cancelado')">cancelado</v-btn>
   <v-btn color="grey" variant="outlined" @click="bill_sale(venta, 'pendiente')">pendiente</v-btn>
   <v-spacer></v-spacer>
   <v-btn color="green" variant="outlined" class="" @click="bill_sale(venta, 'cobrado')">Cobrado</v-btn>
   </v-card-actions>
   </v-card>
   </v-dialog>
   </v-card-text>
   <v-card-actions>
   <v-btn class="" variant="outlined" @click="venta.dialog = true">ver productos</v-btn>
   </v-card-actions>
   </v-card>
   </v-col>
   <v-col cols="6">
    <totalVentas height="100px" class="ma-4" ></totalVentas>
    <printing v-if="selected_venta" :venta="selected_venta"></printing>
    <snackbar :type="notificationType" :message="notificationMessage" :show="showNotification"></snackbar>
   </v-col>
 
   </v-row>
   </v-container>
   </template>
   
   <script setup>
   import totalVentas from './totalVentas.vue';
   import { onMounted, ref } from 'vue'
   import supabase from '@/supabase.js';
   import formatCurrency from '@/composables/formatCurrency';
   import printing from './printing.vue';
   import snackbar from '@/components/snackbar.vue';

   const selected_venta = ref(null)
   const showNotification = ref(false);
    const notificationType = ref('');
    const notificationMessage = ref('');

   
   const ventas = ref([])
   
   const get_ventas = async () => {
    try {
        const { data, error } = await supabase
           .from('ventas')
           .select(`
             *,
             producto_ventas (
               total,
               precio,
               peso,
               productos (
                 nombre
               )
             )
           `)
           .eq('estatus', 'activo')
       
            if (error) {
            console.log(error)
            } else {
            ventas.value = data.map(venta => ({
                ...venta,
                dialog: false  
            }))
        }
        
    } catch (error) {
        mostrarNotificacion('error', 'problemas con la conexion a internet')
    }

   }
   
   onMounted(() => {
     get_ventas()
   })
   
   const bill_sale = async (venta, status) => {
     const { data, error } = await supabase
       .from('ventas')
       .update({ estatus: status })
       .eq('id', venta.id)
   
     if (error) {
       console.log(error)
       mostrarNotificacion('error', 'Error al actualizar la venta')
     } else {
       get_ventas()
       if (status === 'cobrado') {
         selected_venta.value = venta
         mostrarNotificacion('success', 'Venta cobrada')
       }
       if (status === 'cancelado') {
         mostrarNotificacion('error', 'Venta cancelada')
       }
       if (status === 'pendiente') {
         mostrarNotificacion('warning', 'Venta pendiente')
     }
   }}

const mostrarNotificacion = (tipo, mensaje) => {
  notificationType.value = tipo;
  notificationMessage.value = mensaje;
  showNotification.value = true;

  setTimeout(() => {
    showNotification.value = false;
  }, 3000);
};

const get_specific = async (id) => {
  const { data, error } = await supabase
    .from('ventas')
    .select(`
      *,
      producto_ventas (
        total,
        precio,
        peso,
        productos (
          nombre
        )
      )
    `)
    .eq('id', id)

  if (error) {
    mostrarNotificacion('error', 'Error al obtener la venta')
  } else {
    mostrarNotificacion('success', 'Nueva venta')
    ventas.value = [...ventas.value, ...data]
  }
}

const channels = supabase.channel('custom-insert-channel')
  .on(
    'postgres_changes',
    { event: 'insert', schema: 'public', table: 'ventas' },
    (payload) => {
      if (payload.new) {
        setTimeout(() => {
          get_specific(payload.new.id)
        }, 1000); 
      }
    }
  )
  .subscribe()


   </script>