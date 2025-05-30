<template>
    <v-container>
        <v-card elevation="4" variant="outlined" class="bg-white">
             <v-card-title>
                <p class="h5">
                    Información del cliente 
                </p>
            </v-card-title>
            
            <v-card-text>
                <v-list variant="flat" class="bg-white">
                    <v-list-item prepend-icon="mdi-account" class="bg-white">
                        {{ cliente.nombre }}
                    </v-list-item>
                    <v-list-item prepend-icon="mdi-phone" class="bg-white">
                        {{ cliente.telefono }}
                    </v-list-item>
                     <v-list-item prepend-icon="mdi-map-marker" class="bg-white">
                        {{ cliente.direccion }}
                    </v-list-item>
                </v-list>
            </v-card-text>
        </v-card>

    </v-container>

</template>
<script setup>
import { computed, onBeforeMount, onMounted, ref } from 'vue'
import supabase from '@/supabase.js';

const props = defineProps({
    cliente: {
        type: Object,
        required: true
    }
})

const cliente = computed(() => props.cliente)

console.log(cliente.value);






</script>