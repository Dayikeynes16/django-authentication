<template>
    <v-container>
        <v-card variant="outlined" class="ma-0 ">
          <v-text-field v-model="search" label="Busqueda por id, total u hora" class="ma-3" variant="outlined"></v-text-field>
            <v-data-table-virtual :search="search" :headers="headers"  fixed-header :items="ventas" :height="600">
                <template #item.detalles="{ item }">
                    <v-btn @click="watchSpecific(item)" append-icon="mdi-eye" variant="flat" color="green" >
                        hey
                    </v-btn>
                </template>
            </v-data-table-virtual>
        </v-card>
    </v-container>
    
     
</template>
<script setup>
import { ref, onMounted, onBeforeMount, watch} from 'vue';
import formatCurrency from '@/composables/formatCurrency';
import useTime from "@/composables/datetime.js";
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const watchSpecific = (value) => {
  console.log('ID:', value.id);

  
  router.push({
    name: 'ventaEspecifica',
    params: { id: value.id }
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

const search = ref('')
const props = defineProps({
  ventas: {
    type: Array,
    required: true
  }
});
const headers = [
    { title: 'ID', key: 'id' },
    { title: 'Total', key: 'total', value: (item) => formatCurrency((item.total)) },
    { title: 'Hora', key: 'hora', value: (item) => item.hora },
    { title: 'Fecha', key: 'fecha', value: (item) => formatDate(item.fecha) },
    { title: 'Balanza', key: 'balanza' },
    { title: 'Detalles', key: 'detalles' }
]
const ventas = ref([])

onBeforeMount(() => {
  ventas.value = props.ventas

})

const formatSales = (ventas) => {
    return ventas.map(venta => {
        return {
            id: String(venta.id),
            total: venta.total, // Formateado como texto bonito
            hora: getRelativeTime(venta.created_at),
            fecha: formatDate(venta.created_at),
            balanza: venta.balanza ? String(venta.balanza) : '-'
        }
    })
}



watch(
  () => props.ventas,
  (newValue) => {
    ventas.value = formatSales(newValue)
    
  }
)

</script>