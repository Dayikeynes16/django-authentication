<template>
    <v-card variant="outlined">
      <v-card-text>
        <v-select
          variant="outlined"
          label="Clientes"
          v-model="cliente"
          :items="clientes"
          item-title="nombre"
          item-value="id"
        ></v-select>
      </v-card-text>
      <v-card-actions>
        <v-btn block color="green" variant="flat" @click="applyDiscount">Aplicar descuento</v-btn>
      </v-card-actions>
    </v-card>
    <snackbar :type="notificationType" :message="notificationMessage" :show="showNotification" />
  </template>
  
  <script setup>
  import { ref, onMounted, watch, defineEmits } from 'vue'
  import supabase from '@/supabase.js'
  import snackbar from '@/components/snackbar.vue'


  const mostrarNotificacion = (tipo, mensaje) => {
  notificationType.value = tipo;
  notificationMessage.value = mensaje;
  showNotification.value = true;
  setTimeout(() => showNotification.value = false, 3000);
};
  const showNotification = ref(false)
  const notificationType = ref('')
  const notificationMessage = ref('')

  const props = defineProps({
    venta: {
      type: Object,
      required: true
    }
  })

  const emits = defineEmits(['actualizado'])
  
  const cliente = ref(null)
  const clientes = ref([])
  const venta = ref(props.venta)
  const descuentos = ref([])
  
  onMounted(() => {
    getClientes()
  })
  
  const getClientes = async () => {
    const { data, error } = await supabase
      .from('clientes')
      .select(`
        *
      `)
  
    if (error) {
      console.error('Error al cargar clientes:', error)
    } else {
      clientes.value = data
    }
  }
  
  // Asociar venta al cliente
  const asociateSale = async () => {
    const { error } = await supabase
      .from('ventas')
      .update({ cliente_id: cliente.value })
      .eq('id', venta.value.id)
  
    if (error) {
      console.error('Error asociando venta:', error)
      return false
    }
    return true
  }

  const applyDiscount = async () => {
    try {
      const cliente_id = cliente.value
      const venta_id = venta.value.id
      const productosVenta = venta.value.producto_ventas
  
      const asociado = await asociateSale()

      if (!asociado){
        return alert('Error al asociar venta')
      }
  
      descuentos.value = await getDescuentosCliente(cliente_id)
      console.log('Descuentos obtenidos:', descuentos.value);
      
        if (descuentos.value.length === 0) {
          
            mostrarNotificacion('succes', 'Venta asociada correctamente')
            emits('actualizado')
        } 
      const ejemplo  = await updateProductosVenta(productosVenta, descuentos.value)

  
      mostrarNotificacion('success', 'Descuentos aplicados correctamente')
        
    } catch (error) {
      console.error('Error en applyDiscount:', error)
      alert('Ocurrió un error al aplicar los descuentos')
    }
  }
  
  // Obtener precios especiales del cliente
  const getDescuentosCliente = async (cliente_id) => {
    const { data, error } = await supabase
      .from('precio_especials')
      .select('*, productos(*)')
      .eq('cliente_id', cliente_id)
  
    if (error) {
      console.error('Error obteniendo descuentos:', error)
      return []
    }
    console.log('esta es la data', data);
    return data
  }

  
//   // Actualizar productos con descuentos
  const updateProductosVenta = async (productosVenta, descuentos) => {
    console.log('este es el descuento hehewhw', descuentos);
    
    let totalVenta = 0
  
    for (const producto of productosVenta) {

      const descuento = descuentos.find(d => d.producto_id === producto.producto_id)
      console.log('este es el descuento...', descuento);
      console.log('este es el producto', producto);
      
      const precioNuevo = descuento ? descuento.precio : producto.precio
      const totalNuevo = precioNuevo * producto.peso
  
      const { data, error,  } = await supabase
            .from('producto_ventas')
            .update({
            precio: precioNuevo,
            total: totalNuevo
            })
            .eq('id', producto.id)
            
  
      if (error) {
        console.error(`Error actualizando producto ${producto.id}:`, error)
      } else {
        totalVenta += totalNuevo
        console.log('este es el total de la venta', totalVenta);
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
    }
  }


  
  watch(() => props.venta, (newValue) => {
  if (newValue) {
    venta.value = newValue
  }
})

  </script>
  