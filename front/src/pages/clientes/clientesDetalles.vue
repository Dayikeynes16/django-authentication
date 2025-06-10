<template>
  
        <v-row class="pa-2">
            <v-col cols="4">
                <v-row>
                    <v-col cols="12">
                        <infoCliente :cliente="client"></infoCliente>
                    </v-col>
                    <v-col cols="12">
                        
                       
                        <productosDescuentos @creado="get_clients(id)" :cliente="client"  :productos="client.precio_especials">
                        </productosDescuentos>
                   
                    </v-col>
                
                </v-row>
            </v-col>
            <v-col cols="8">
                <v-row>
                    
                    <v-col cols="12">
                            <v-row>
                                <v-col cols="4" height="150px">
                                    <v-container>
                                        <v-card class="opacity-40" color="red" height="150px">
                                           <v-card-title>Deuda total</v-card-title>
                                           <v-card-text>
                                                 <h1 class="text-h5">
                                                  {{ formatCurrency(resumen.saldoPendiente) }}
                                                </h1>
                                           </v-card-text>
           
                                       </v-card>
                                    </v-container>
                                </v-col>
                                <v-col cols="4">
                                    <v-container>
                                        <v-card variant="outlined" class="opacity-40 bg-green"  height="150px">
                                            <v-card-title color="black" class="">Compras este mes</v-card-title>
                                            <v-card-text>
                                                <h1 class="text-h5">
                                                  {{ formatCurrency(resumen.totalUltimoMes) }}
                                                </h1>
                                            </v-card-text>
                                        </v-card>

                                    </v-container>
                                </v-col>
                                <v-col cols="4">
                                    <v-container>
                                        <v-card class="opacity-40" color="blue" height="150px">
                                            <v-card-title>
                                                Historial Total
                                            </v-card-title>
                                            <v-card-text>
                                                <h1 class="text-h5">
                                                  {{ formatCurrency(resumen.totalVentas) }}
                                                </h1>
                                            </v-card-text>
                                        </v-card>
                                    </v-container>
                                </v-col>
                            </v-row>
                        </v-col>
                    
                    <v-col cols="12">
                        <ultimasVentas :id="client.id"></ultimasVentas>
                    </v-col>
                </v-row>

            </v-col>
        </v-row>
        
</template>
<script setup>
import { onBeforeMount, onMounted, ref, watch } from 'vue'
import supabase from '@/supabase.js';
import { useRoute } from 'vue-router'
import informacionFinanciera from './detalles/informacionFinanciera.vue';
const route = useRoute();
const id = ref(route.params.id);
import infoCliente from './detalles/infoCliente.vue';
import productosDescuentos from './detalles/productosDescuentos.vue';
import ultimasVentas from './detalles/ultimasVentas.vue';
import resumenFinanzas from '@/composables/clientFinances';

import formatCurrency from '@/composables/formatCurrency';

const client = ref({})

const descuentos = ref(false)
const resumen = ref({})

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
                ),
                ventas (
                    *,
                    producto_ventas (
                        *,
                        productos (
                            *
                        )
                    ),
                    pagos (
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
            resumen.value = resumenFinanzas(client.value)

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

watch(()=> {})
onMounted(() => {
    get_clients(id.value)
})
</script>