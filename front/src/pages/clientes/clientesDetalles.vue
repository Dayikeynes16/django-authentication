<template>
    <v-container>
        <v-row>
            <v-col cols="6">
                <infoCliente :cliente="client">
                </infoCliente>
              
            </v-col>
            <v-col cols="6">
                <productosDescuentos :productos="client.precio_especials">

                </productosDescuentos>
                
                
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <v-card variant="outlined" class="pa-5">
                    <v-card-title>
                        Ultimas ventas
                    </v-card-title>
                    <v-card-text>
                        <ultimasVentas :id="client.id"></ultimasVentas>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

    </v-container>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import supabase from '@/supabase.js';
import { useRoute } from 'vue-router'
const route = useRoute();
const id = ref(route.params.id);
import infoCliente from './detalles/infoCliente.vue';
import productosDescuentos from './detalles/productosDescuentos.vue';
import ultimasVentas from './detalles/ultimasVentas.vue';

import formatCurrency from '@/composables/formatCurrency';

const client = ref({})

const get_clients = async (id) => {
    try {
        const { data, error } = await supabase
            .from('clientes')
            .select(` 
                *,
                precio_especials (
                    *,
                    productos (
                        *
                    )
                )
                `
            )
            .eq('id', id)
            .single()

        if (error) {
            console.log(error)
        } else {
            client.value = data

        }
    } catch (error) {
        console.error('Error fetching clients:', error);
    }
}

onMounted(() => {
    get_clients(id.value)
})
</script>