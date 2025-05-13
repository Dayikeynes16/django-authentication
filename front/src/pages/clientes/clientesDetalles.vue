<template>
    <v-container>
        <v-row>
            <v-col cols="4">
                <infoCliente :cliente="client">
                </infoCliente>
              
            </v-col>
              <v-col cols="8">
                <v-container>
                    <v-card variant="outlined" class="pa-5">
                        <v-card-title>
                            Ultimas ventas
                        </v-card-title>
                        <v-card-text >
                            <ultimasVentas :id="client.id"></ultimasVentas>
                        </v-card-text>
                    </v-card>
                </v-container>
            </v-col>
            
        </v-row>
        <v-row>
            <v-col cols="8">
                <productosDescuentos v-if="descuentos === true"  :productos="client.precio_especials">
                </productosDescuentos>
                    <div v-else>
                        <v-container>
                            <v-card variant="outlined" class="pa-5">
                                <v-card-title>
                                    Productos con descuento
                                </v-card-title>
                                <v-card-text>
                                    Este cliente no cuenta productos con descuento
                                </v-card-text>
                            </v-card>
                        </v-container>
                    </div>
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

const descuentos = ref(false)

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
            if(data.precio_especials.length){
                descuentos.value = true
            }else{
                descuentos.value = false
            }
            
        }
    } catch (error) {
        console.error('Error fetching clients:', error);
    }
}

onMounted(() => {
    get_clients(id.value)
})
</script>