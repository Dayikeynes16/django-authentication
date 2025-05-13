<template>
        
        
      <v-card-text v-if="historial">
        <v-infinite-scroll
          height="300px"
          :items="ventas"
          @load="load"
        >
          <template v-for="(item, index) in ventas" :key="item.id">
            <div class="pa-2">
              <v-card variant="outlined">
                <v-card-title>{{ formatCurrency(item.total) }}</v-card-title>
                <v-card-subtitle>{{ getRelativeTime(item.created_at) }}</v-card-subtitle>
                <v-card-text>
                  <v-row>
                  <v-col cols="6"></v-col>
                  <v-col cols="6"></v-col>
                  </v-row>
                </v-card-text>
                <v-card-actions>
                  <v-btn >Ver detalles</v-btn>
                  <!-- <v-btn @click="item.dialog = true">Ver detalles</v-btn>
                  <v-dialog 
                        v-model="item.dialog"
                        max-width="900px"
                        :close-on-content-click="false">
                        <ventaEspecifica
                        @close="item.dialog = false" 
                        :venta = "item"
                        ></ventaEspecifica>
                    </v-dialog> -->


                </v-card-actions>

              </v-card>
            </div>
          </template>
        </v-infinite-scroll>
      </v-card-text>
  
      <v-card-text v-else>
        Este cliente no tiene historial de compras
      </v-card-text>

      

  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import supabase from '@/supabase.js'
  import formatCurrency from '@/composables/formatCurrency'
  import useTime from '@/composables/datetime.js'
  import ventaEspecifica from './ventaEspecifica.vue'

  
  const { getRelativeTime } = useTime()
  
  const props = defineProps({
    id: {
      type: Number,
      required: true
    }
  })

  const especifica = (id) => {
    console.log('ID de venta:', id);
    
   
  }
  
  const historial = ref(false)
  const ventas = ref([])
  
  const paginate = ref({
    page: 1,
    pageSize: 5
  })
  
  const load = async ({ side, done }) => {
  try {
    const from = (paginate.value.page - 1) * paginate.value.pageSize
    const to = (paginate.value.page * paginate.value.pageSize) - 1

    const { data, error } = await supabase
      .from('ventas')
      .select(`
        *,
        pagos (*),
        producto_ventas (
          *,
          productos (
            *
          )
        )
      `)
      .eq('cliente_id', props.id)
      .order('created_at', { ascending: false })
      .range(from, to)

    if (error) {
      console.error('Error al obtener ventas:', error)
      done('error')
    } else {
      if (data.length === 0) {
        done('empty')
        return
      }

      ventas.value.push(...data.map(venta => ({
        ...venta,
        dialog: false
      })))

      historial.value = true
      paginate.value.page++
      done('ok')
    }
  } catch (error) {
    console.error('Error en load:', error)
    done('error')
  }
}
  
  // Al montar, realiza primer intento de carga
  onMounted(() => {
    if (props.id) {
      historial.value = true
    }
  })
  
  // Si cambia el cliente, reinicia scroll
  watch(() => props.id, (newId) => {
    if (newId) {
      ventas.value = []
      paginate.value.page = 1
      historial.value = true
    }
  })
  </script>