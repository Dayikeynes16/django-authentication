<template>
    <v-container>
      <v-card variant="outlined" class="mx-auto" max-width="800">
        <v-card-text>
          <v-text-field
            v-model="search"
            variant="outlined"
            label="Buscar cliente"
            append-icon="mdi-magnify"
          />
          <v-data-table
            :headers="headers"
            :items="clients"
            :search="search"
            item-value="id"
            class="bg-white"
          >
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
    </v-container>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import supabase from '@/supabase.js'
  import { router } from '@/router'
  
  const clients = ref([])
  const search = ref('')
  
  const headers = [
    { text: 'Nombre', value: 'nombre' },
    { text: 'Teléfono', value: 'telefono' },
    { text: 'Acciones', value: 'acciones' }
  ]
  
  const verCliente = (id) => {
    router.push({ name: 'clientesDetalles', params: { id } })
  }
  
  const get_clients = async () => {
    const { data, error } = await supabase.from('clientes').select('*')
    if (error) {
      console.error(error)
    } else {
        clients.value = data.map((client) => ({
        nombre: client.nombre,
        telefono: client.telefono,
        id: client.id,
        acciones: '' 
        }))

    }
  }
  
  onMounted(() => {
    get_clients()
  })
  </script>
  