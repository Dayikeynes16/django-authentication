<template>
    <v-container>
        <v-card variant="outlined" class="pa-5">
            <v-card-tittle>
                Productos con descuento
            </v-card-tittle>
            <v-card-text>
                <v-card variant="outlined" class="pa-5">
                    <v-row  v-for="(producto, index) in productos" :key="index">
                        <v-col cols="12" md="6">
                            <p><strong>Nombre:</strong> {{ producto.productos.nombre }}</p>
                            <p><strong>Precio preferencial:</strong> {{ formatCurrency(producto.precio) }}</p>
                            <p><strong>Precio original:</strong> {{ formatCurrency(producto.productos.precio_de_venta)}}</p>
                        </v-col>
                        
                    </v-row>
                </v-card>
            </v-card-text>
    
        </v-card>
    </v-container>

</template>
<script setup>
import { computed, onBeforeMount, onMounted, ref } from 'vue'
import supabase from '@/supabase.js';
import formatCurrency from '@/composables/formatCurrency';

const props = defineProps({
    productos: {
        type: Array,
        required: true
    }
})
const productos = computed(() => props.productos)
const productosDescuentos = ref([])

console.log(productos.value);



</script>