<template>
  <v-container>
    <!-- Tarjeta resumen global -->
     <v-row>
      <v-col cols="3">
        <v-card append-icon="mdi-cash-check" title="Total por cobrar" class="mx-auto my-2 pa-2" height="140px" color="" variant="outlined" width="100%">
        <v-card-text>
          <h3 class="align-center">
            <strong>{{ formatCurrency(totalPorCobrar) }}</strong>
          </h3>
        </v-card-text>
          


          
        </v-card>

      </v-col>
      <v-col cols="3">
        <v-card title="Total de clientes" append-icon="mdi-account-group-outline" height="140px" class="mx-auto my-2 pa-2" color="" variant="outlined" width="100%">
        <v-card-text>
          <h3 class="align-center">
            <strong>{{ clients.length }}</strong>
          </h3>

        </v-card-text>
        </v-card>
        
      </v-col>
      <v-col cols="3">
        <v-card title="Clientes Activos" height="140px" append-icon="mdi-trending-up" class="mx-auto my-2 pa-2" color="" variant="outlined" width="100%">
         
         <v-card-text>
          <h3 class="align-center">
            <strong>{{ clients.filter(c => c.deuda > 0).length }}</strong>
          </h3>
         </v-card-text>
         
        </v-card>
        
      </v-col>
      <v-col cols="3">
        <v-card title="Clientes Inactivos" append-icon="mdi-trending-down" height="140px" class="mx-auto my-2 pa-2" color="" variant="outlined" width="100%">
         
          <v-card-text>
          <h3 class="align-center">
            <strong>{{ clients.filter(c => c.deuda === 0).length }}</strong>

          </h3>
          </v-card-text>


      
        </v-card>
        
      </v-col>
      <v-col cols="12">

        <v-card variant="outlined" class="mx-auto" width="100%">
          <v-card-text>
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="primary"
              class="mb-4"
            />
    
            <v-text-field
              v-model="search"
              variant="outlined"
              label="Buscar cliente"
              append-icon="mdi-magnify"
              class="mb-4"
            />
    
            <v-data-table
              :headers="headers"
              :items="clients"
              :search="search"
              item-value="id"
              class="bg-white"
              :loading="loading"
              no-data-text="No se encontraron clientes con esos criterios"
            >
              <!-- Columna personalizada para nombre (gris si no debe) -->
              <template #item.nombre="{ item }">
                <span :class="item.deuda === 0 ? 'text-grey' : 'text-high-emphasis'">
                  {{ item.nombre }}
                </span>
              </template>
    
              <!-- Columna personalizada para deuda -->
              <template #item.deuda="{ item }">
                <span :class="item.deuda > 0 ? 'text-red' : 'text-grey'">
                  {{ formatCurrency(item.deuda) }}
                </span>
              </template>
    
              <!-- Columna para botón de acción -->
              <template #item.acciones="{ item }">
                <v-btn
                  @click="verCliente(item.id)"
                  color="primary"
                  variant="outlined"
                  size="small"
                >
                  Ver
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
     </v-row>
   


    <!-- Tarjeta de tabla de clientes -->
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import supabase from '@/supabase.js'
import { router } from '@/router'

const clients = ref([])
const search = ref('')
const loading = ref(false)

const headers = [
  { text: 'Nombre', value: 'nombre' },
  { text: 'Teléfono', value: 'telefono' },
  { text: 'Deuda', value: 'deuda' },
  { text: 'Acciones', value: 'acciones' }
]

// Lógica para navegar a los detalles del cliente
const verCliente = (id) => {
  router.push({ name: 'clientesDetalles', params: { id } })
}

// Lógica para calcular la deuda por cliente
const calcularDeudaCliente = (ventas) => {
  return ventas?.reduce((acc, venta) => {
    if (venta.estatus === 'cancelado') return acc
    const totalPagado = venta.pagos?.reduce((suma, p) => suma + (p.total || 0), 0) || 0
    const deuda = venta.total - totalPagado
    return deuda > 0 ? acc + deuda : acc
  }, 0) || 0
}

// Obtener clientes desde Supabase
const get_clients = async () => {
  loading.value = true
  const { data, error } = await supabase
    .from('clientes')
    .select(`*, ventas(*, pagos(*))`)

  if (error) {
    console.error(error)
  } else {
    clients.value = data.map(client => ({
      id: client.id,
      nombre: client.nombre,
      telefono: client.telefono,
      deuda: calcularDeudaCliente(client.ventas ?? [])
    }))
  }

  loading.value = false
}

// Formatear como moneda mexicana
const formatCurrency = (val) =>
  new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'MXN'
  }).format(val)

// Calcular total por cobrar de todos los clientes
const totalPorCobrar = computed(() =>
  clients.value.reduce((sum, c) => sum + (c.deuda || 0), 0)
)

onMounted(() => {
  get_clients()
})
</script>

<style scoped>
.text-red {
  color: #d32f2f;
}
.text-grey {
  color: #9e9e9e;
}
</style>
