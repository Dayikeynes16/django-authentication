<template>
    <v-container>
        <v-card variant="outlined" class="mx-auto" max-width="800">
            <v-card-text>
                <table class="table table-hover " variant="outlined">
                    <thead>
                        <tr>
                           
                            <th class="pa-6" v-for="header in headers" :key="header.value">
                                {{ header.text }}
                           </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="client in clients" :key="client.id">
                          
                            <td class="pa-4">{{ client.nombre }}</td>
                            <td class="pa-4">{{ client.telefono }}</td>
                            <td class="pa-4">{{ client.direccion }}</td>
                            <td class="pa-4">
                                <v-btn @click="verCliente(client.id)">Ver</v-btn>
                            </td>
                        </tr>
                    </tbody>
                   
                </table>
            </v-card-text>
        </v-card>
    </v-container>

</template>
<script setup>
import { onMounted, ref } from 'vue'
import supabase from '@/supabase.js';
import formatCurrency from '@/composables/formatCurrency';
import snackbar from '@/components/snackbar.vue';
import { router } from '@/router';

const clients = ref([])
const search = ref('')

const verCliente = (id) => {

    console.log('pinche puto');
    
    router.push({ name: 'clientesDetalles', params: { id } });
}

const headers = [
   
    { text: 'Nombre', value: 'nombre' },
    { text: 'Telefono', value: 'telefono' },
    { text: 'Direccion', value: 'direccion' },
    { text: 'Acciones', value: 'acciones', sortable: false }
]   

const get_clients = async () => {
    try {
        const { data, error } = await supabase
            .from('clientes')
            .select(`*`)


        if (error) {
            console.log(error)
        } else {
            clients.value = data.map(client => ({
                ...client,
                dialog: false
            }))
        }
    } catch (error) {
        console.error('Error fetching clients:', error);
    }
}

onMounted(() => {
    get_clients()
})
</script>