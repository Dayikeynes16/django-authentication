<template>
  <v-virtual-scroll :items="ventas">
    <template #default="{ item }">
      <v-list >
        <v-list-item  class="d-flex align-center" >
          <v-card variant="outlined" width="900px" class="mb-4">
            <v-card-title>
              <v-row>
                <v-col cols="4" >
                  <p  class="ma-2 font-size-20">
                   
                    {{ getRelativeTime(item.created_at) }}
                  </p>
                </v-col>
                <v-col cols="4"  >
                  <p class="ma-2">
                    {{ getTime(item.created_at) }}
                  </p>
                </v-col>
                <v-col cols="3"  >
                  <p class="ma-2">

                    {{ formatCurrency(item.total) }}
                  </p>
                </v-col>
              </v-row>
            </v-card-title>
            <v-card-text>
              <v-expansion-panels accordion>
                <v-expansion-panel>
                  <v-expansion-panel-title>
                    productos
                  </v-expansion-panel-title>
                  <v-expansion-panel-text v-for="producto in item.producto_ventas">
                    {{ producto.productos.nombre }} - {{ formatCurrency(producto.precio) }} - {{ producto.peso }}Kg - {{ formatCurrency(producto.total) }}
                  </v-expansion-panel-text>

                </v-expansion-panel>
                
              </v-expansion-panels>

            </v-card-text>
          </v-card>
        </v-list-item>
      </v-list>
    </template>

  </v-virtual-scroll>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import supabase from '@/supabase.js'
import formatCurrency from '@/composables/formatCurrency'
import useTime from '@/composables/datetime.js';

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
