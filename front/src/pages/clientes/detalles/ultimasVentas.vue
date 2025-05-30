<template>
  <v-container>
    <v-card variant="outlined" elevation="4">
      <v-card-title>
        <v-row>
          <v-col cols="6">
            
              <h2>Últimas compras</h2>

            
          </v-col>
          <v-col cols="6" align="right" />
        </v-row>
      </v-card-title>

      <v-card-text v-if="historial">
        <div style="overflow-x: auto; white-space: nowrap;">
          <v-infinite-scroll
            direction="horizontal"
            :items="ventas"
            @load="load"
          >
            <div class="d-flex flex-row" style="gap: 16px; padding: 8px;">
              <template v-for="(item, index) in ventas" :key="item.id">
                <div style="min-width: 300px; display: inline-block;">
                  <v-card variant="outlined" class="bg-white" elevation="2">

                    <v-row>
                      <v-col cols="6" align="center" class="">
                        <div class="pt-4">
                          <v-row>
                            <v-col cols="3" >
                              <v-icon icon="mdi-calendar"></v-icon>

                            </v-col>
                            <v-col cols="9">
                              <v-card-subtitle align="">
                                {{ formatFechaLargaConSlash(item.created_at) }}
                              </v-card-subtitle>

                            </v-col>
                          </v-row>
                        </div>

                      </v-col>
                      <v-col cols="6" align="center"  >
                        <div class="pt-1">
                          <v-chip
                          
                          v-if="item.estatus === 'pendiente'"
                          color="orange"
                          text-color="white"
                          class="ma-2"
                        >
                          {{ item.estatus }}
                        </v-chip>
                        <v-chip
                          v-if="item.estatus === 'cobrado'"
                          color="green"
                          text-color="white"
                          class="ma-2"
                        >
                          {{ item.estatus }}
                        </v-chip>
                        </div>
                      </v-col>
                    </v-row>
                    <v-card-title>{{ (item.total) }}</v-card-title>
                    
                    <v-card-text>
                      <v-row>
                        <v-col cols="6" align-self="center">Estatus:</v-col>
                        <v-col cols="6" align-self="center">
                        
                        </v-col>
                      </v-row>
                    </v-card-text>
                    <v-card-actions>
                      <v-btn
                        variant="flat"
                        color="black"
                        block
                        @click="especifica(item.id)"
                      >
                        Detalles
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </div>
              </template>
            </div>
          </v-infinite-scroll>
        </div>
      </v-card-text>

      <v-card-text v-else>
        Este cliente no tiene historial de compras
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import supabase from '@/supabase.js'
import formatCurrency from '@/composables/formatCurrency'
import useTime from '@/composables/datetime.js'
import { router } from '@/router'

const { getRelativeTime, formatFechaLargaConSlash, formatHoraCompleta } = useTime()

const props = defineProps({
  id: {
    type: Number,
    required: true
  }
})

const especifica = (id) => {
  router.push({ name: 'ventaEspecifica', params: { id } })
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
      .in('estatus', ['pagado', 'cobrado', 'pendiente'])
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

onMounted(() => {
  if (props.id) {
    historial.value = true
  }
})

watch(() => props.id, (newId) => {
  if (newId) {
    ventas.value = []
    paginate.value.page = 1
    historial.value = true
  }
})
</script>
