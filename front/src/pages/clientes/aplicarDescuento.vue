<template>
  <v-container>

  <template  v-if="switchClient">
    <v-card  width="100%" class="pa-2" variant="outlined">
      <v-card-text>
        <v-row>
          <v-col cols="12" align="center">
            <v-icon icon="mdi-account-circle" size="50" color="black"></v-icon>
          </v-col>

          <v-divider></v-divider>

          <v-col cols="6">
            <div align="left" class="text-body-1">Cliente:</div>
          </v-col>
          <v-col cols="5">
            <div align="right">{{ venta.clientes?.nombre || '' }}</div>
          </v-col>

          <v-col cols="6">
            <div align="left">Teléfono:</div>
          </v-col>
          <v-col cols="5">
            <div align="right">{{ venta.clientes?.telefono || '' }}</div>
          </v-col>

          <v-divider></v-divider>

          <v-col cols="12">
            <div align="center" class="text-h6">
              <v-btn @click="switchClient = !switchClient" variant="flat" color="black" class="ma-2">
                Cambiar cliente
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </template>

  <template v-else>
    <v-card width="100%" variant="outlined" class="pa-2">
      <v-card-text>
        <v-row>
          <v-col cols="12">
            <v-autocomplete
              variant="outlined"
              label="Clientes"
              v-model="cliente"
              :items="clientes"
              item-title="nombre"
              item-value="id"
            ></v-autocomplete>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn block color="green" variant="flat" @click="JustAsociate">Asociar</v-btn>
      </v-card-actions>
    </v-card>
  </template>
  </v-container>


  <snackbar v-if="showNotification" :type="notificationType" :message="notificationMessage" />
</template>

<script setup>
import { ref, onMounted, watch, defineEmits } from 'vue'
import supabase from '@/supabase.js'
import snackbar from '@/components/snackbar.vue'

const showNotification = ref(false)
const notificationType = ref('')
const notificationMessage = ref('')

const mostrarNotificacion = (tipo, mensaje) => {
  notificationType.value = tipo
  notificationMessage.value = mensaje
  showNotification.value = true
  setTimeout(() => (showNotification.value = false), 3000)
}

const props = defineProps({
  venta: {
    type: Object,
    required: true,
  },
})

const emits = defineEmits(['actualizado'])

const cliente = ref(null)
const clientes = ref([])
const venta = ref(props.venta)
const descuentos = ref([])
const switchClient = ref(false)

onMounted(() => {
  getClientes()
  if (venta.value.clientes) {
      switchClient.value = true
    } else {
      switchClient.value = false

    }
})

const getClientes = async () => {
  const { data, error } = await supabase.from('clientes').select(`*`)
  if (error) {
    console.error('Error al cargar clientes:', error)
  } else {
    clientes.value = data
  }
}

const asociateSale = async () => {
  console.log('venta', venta.value, 'cliente', cliente.value);
  
  const { error, data } = await supabase
    .from('ventas')
    .update({ cliente_id: cliente.value })
    .eq('id', venta.value.id)
    .select()

  if (error) {
    return false
  }
  if(data){
    console.log('aqui estou');
    mostrarNotificacion('succes', 'venta asociada correctamente')
    emits('actualizado')
    switchClient.value = !switchClient.value
    console.log('aqui estuve');
    
    return data
  }
}

const JustAsociate = async () => {
  console.log('hey');
  
  if (!cliente.value) {
    mostrarNotificacion('error', 'Selecciona un cliente primero')
    return
  }
  console.log('segundo hey');
  
  const response = await asociateSale()
  console.log('tercer gey', response);
  
  if(response){
    mostrarNotificacion('succes', 'venta asociada correctamente')
    emits('actualizado')
    
  }
}

const applyDiscount = async () => {
  try {
    const cliente_id = cliente.value
    const productosVenta = venta.value.producto_ventas

    const asociado = await asociateSale()

    if (!asociado) {
      mostrarNotificacion('error', 'Error al asociar venta')
      return
    }

    descuentos.value = await getDescuentosCliente(cliente_id)

    if (descuentos.value.length === 0) {
      mostrarNotificacion('success', 'Venta asociada correctamente')
      emits('actualizado')
      return
    }

    await updateProductosVenta(productosVenta, descuentos.value)
    mostrarNotificacion('success', 'Descuentos aplicados correctamente')
  } catch (error) {
    console.error('Error en applyDiscount:', error)
    mostrarNotificacion('error', 'Ocurrió un error al aplicar los descuentos')
  }
}

const getDescuentosCliente = async (cliente_id) => {
  const { data, error } = await supabase
    .from('precio_especials')
    .select('*, productos(*)')
    .eq('cliente_id', cliente_id)

  if (error) {
    console.error('Error obteniendo descuentos:', error)
    return []
  }
  return data
}

const updateProductosVenta = async (productosVenta, descuentos) => {
  let totalVenta = 0

  for (const producto of productosVenta) {
    const descuento = descuentos.find(d => d.producto_id === producto.producto_id)
    const precioNuevo = descuento ? descuento.precio : producto.precio
    const totalNuevo = precioNuevo * producto.peso

    const { error } = await supabase
      .from('producto_ventas')
      .update({ precio: precioNuevo, total: totalNuevo })
      .eq('id', producto.id)

    if (error) {
      console.error(`Error actualizando producto ${producto.id}:`, error)
    } else {
      totalVenta += totalNuevo
    }
  }

  const final = await supabase
    .from('ventas')
    .update({ total: totalVenta })
    .eq('id', venta.value.id)
    .select()
    .single()

  if (final.error) {
    console.error('Error actualizando total de venta:', final.error)
  } else {
    emits('actualizado')
  }
}

watch(() => props.venta, (newValue) => {
  if (newValue){
    venta.value = newValue
    console.log('hey');
    if (venta.value.clientes) {
      switchClient.value = true
    } else {
      switchClient.value = false

    }
  } 

  
})


</script>
