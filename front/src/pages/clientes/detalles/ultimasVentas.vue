<template>
    <v-container>
        <v-list>
            <v-list-item-group v-for="(venta, index) in ventas" :key="index">
                <v-list-item>
                    <v-list-item-content>
                        <v-list-item-title>
                            <v-row>
                                <v-col cols="3">
                                    Fecha: {{ formatDate(venta.created_at) }}
                                </v-col>
                                <v-col cols="3">
                                    Total: {{ formatCurrency(venta.total) }}
                                </v-col>
                                <v-col cols="3">
                                    {{ venta.producto_ventas.length }}
                                </v-col>
                            </v-row>
                        </v-list-item-title>
                        <v-list-item-subtitle>
                           
                        </v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action>
                        
                    </v-list-item-action>
                </v-list-item>
            </v-list-item-group>
        </v-list>

    </v-container>

</template>
<script setup>
import { computed, onMounted, ref } from 'vue'
import supabase from '@/supabase.js';
import formatCurrency from '@/composables/formatCurrency';
import  useTime  from '@/composables/datetime.js'

const { 
  formatDate,
  formatDateWithDay,
  getRelativeTime,
  isToday,
  getDateComponents,
  formatos
} = useTime()
const props = defineProps({
    id: {
        type: Number,
        required: true
    }
})

const id = computed(() => props.id)

const ventas = ref([])

const get_ventas = async (id) => {
    try {
        const { data, error } = await supabase
            .from('ventas')
            .select(` 
                *,
                producto_ventas (
                    *,
                    productos (
                        *
                    )
                    
                )
                `)
            .eq('cliente_id', id)
            .order('created_at', { ascending: false })

        if (error) {
            console.log(error)
        } else {
            console.log(data)
            ventas.value = data.map(venta => ({
                ...venta,
                dialog: false
            }))
        }
    } catch (error) {
        console.error('Error fetching ventas:', error);
    }
}

onMounted(() => {
    get_ventas(id.value)
    console.log(id, ' esto es el id') ;
    
})


</script>