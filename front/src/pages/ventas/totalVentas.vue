<template>
    <div>
        <v-card variant="outlined" class="ma-4">
            <v-card-title>Ventas totales</v-card-title>
            <v-card-text>

                vendido durante el dia: {{ formatCurrency(totalVentas) }}
            </v-card-text>
        </v-card>
      
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import supabase from '@/supabase.js';
  import formatCurrency from '@/composables/formatCurrency';
  import useTime from '@/composables/datetime.js';
  const ventas = ref([])

  const { 
  formatDate,
  formatDateWithDay,
  getRelativeTime,
  isToday,
  getDateComponents,
  formatos
} = useTime()



  
  const get_ventas = async () => {
    try {
      // Calculate the timestamp for 8 hours ago
      const eighthHoursAgo = new Date(Date.now() - 12 * 60 * 60 * 1000 - (6 * 60 * 60 * 1000)).toISOString()      
      // // const eighthHoursAgo = new Date(Date.now() - 9 * 60 * 60 * 1000).toISOString()
 
      
      const { data, error } = await supabase
        .from('ventas')
        .select(`
          *,
          producto_ventas (
            total,
            precio,
            peso,
            productos (
              nombre
            )
          )
        `)
        .eq('estatus', 'cobrado')
        .gte('created_at', eighthHoursAgo)
    
      if (error) {
        console.error('Error fetching sales:', error)
        return
      }
   
      totalVentas.value = data.reduce((acc, venta) => acc + venta.total, 0)
      
      
      // Add a dialog property to each venta for potential use in UI
      ventas.value = data.map(venta => ({
        ...venta,
        dialog: false  
      }))
      
    } catch (error) {
      console.error('Unexpected error:', error)
    }
  }
  
  const totalVentas = ref(0)

  const CalculateTotalVentas = () => {
    totalVentas.value = ventas.value.reduce((acc, venta) => acc + venta.total, 0)
  }

  // Call the function when the component is mounted
  onMounted(get_ventas)
  </script>