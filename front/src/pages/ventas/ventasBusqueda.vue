<template>
  <v-row>
    <v-col cols="7">
      <scrollerVentas :ventas="ventas"></scrollerVentas>
    </v-col>
    <v-col cols="5">
      <totalVentas></totalVentas>

    </v-col>
  </v-row>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import supabase from '@/supabase.js'
import formatCurrency from '@/composables/formatCurrency'
import useTime from '@/composables/datetime.js';
import totalVentas from './totalVentas.vue';
import scrollerVentas from './scrollerVentas.vue';
const getTime = (isoString) => {
  const date = new Date(isoString)
  return date.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true // cambia a false si quieres formato 24h
  })
}


const { 
  formatDate,
  formatDateWithDay,
  getRelativeTime,
  isToday,
  getDateComponents,
  formatos
} = useTime()

const ventas = ref([])

const get_ventas = async () => {
  try {
    const eighthHoursAgo = new Date(Date.now() - 15 * 60 * 60 * 1000 - (6 * 60 * 60 * 1000)).toISOString()

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
      .eq('estatus', 'cobrado')
      .gte('created_at', eighthHoursAgo)
      .order('created_at', { ascending: false })

    if (error) {
      console.error('Error fetching sales:', error)
      return
    }

    // Agregamos el campo `dialog` para cada venta
    ventas.value = data.map(venta => ({
      ...venta,
      dialog: false
    }))
  } catch (error) {
    console.error('Unexpected error:', error)
  }
}

onMounted(() => {
  get_ventas()
})
</script>
