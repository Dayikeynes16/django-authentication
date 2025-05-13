<template>
    <v-container>
        <v-card elevation="4" variant="flat">
            <v-row>
                <v-col cols="8">
                  <v-card-title>
                    Información del cliente 
                  </v-card-title>
                </v-col>
            </v-row>
            <v-card-text>
                <v-row>
                    <v-col cols="12" md="6">
                        <p><strong>Nombre:</strong> {{ cliente.nombre }}</p>
                        <p  v-if="cliente.nickname">  <strong>Apodo:</strong> {{ cliente.nickname }}</p>
                        <p><strong>Telefono:</strong> {{ cliente.telefono }}</p>
                        <p><strong>Direccion:</strong> {{ cliente.direccion }}</p>
                    </v-col>
                    <v-col cols="12" md="6">
                    </v-col>
                </v-row>
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