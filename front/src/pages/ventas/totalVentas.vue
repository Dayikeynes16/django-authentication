<template>
  <div>
    <v-card variant="outlined"  class="ma-4">
      <v-card-title>El Puebla     </v-card-title>
      <v-card-subtitle>
        Ventas del dia {{ formatDateWithDay(getMexicoLocalString()) }}
      </v-card-subtitle>
      <v-card-text>
        <v-row>
          <v-col cols="4">
            <v-card variant="outlined" height="100%">
              <v-card-title>
                <p>
                  Total Ventas
                </p>
              </v-card-title>
              <v-card-text>
                <v-icon color="blue" size="40" icon="mdi-cart"></v-icon>
                <p>
                   <br> 
                  <strong>
                    {{ formatCurrency(resumen?.totalVendido || 0) }}
                  </strong>
                </p>
              </v-card-text>
            </v-card>

          </v-col>
          <v-col cols="4">
            <v-card variant="outlined"  height="100%">
              <v-card-text>
                <v-icon color="green" size="40" icon="mdi-cash"></v-icon>
                <p>
                  Ticket promedio <br> 
                  <strong>
                    {{ formatCurrency(resumen?.ticketPromedio || 0) }}
                  </strong>
                </p>
              </v-card-text>
            </v-card>

          </v-col>
          <v-col cols="4">
            <v-card variant="outlined"  height="100%">
              <v-card-text>
                <v-icon color="brown" size="40" icon="mdi-invoice-list"></v-icon>
                <p>N. Ventas <br>
                  <strong>
                    {{ resumen.ventas?.length || 0 }}
                  </strong>
                  </p>              
              </v-card-text>
            </v-card>

          </v-col>

        </v-row>
        <v-row>
          <v-col cols="7">
            <v-card variant="outlined">
              <v-card-title>
                Metodos de pago
              </v-card-title>
              <v-card-text  >
                <v-list variant="outlined">
                  <v-list-item>
                    <v-icon color="green" icon="mdi-cash"></v-icon>
                    <p>Efectivo <strong>{{ formatCurrency(resumen?.totalEfectivo || 0) }}</strong></p>
                  </v-list-item>
                  <v-list-item>
                    <v-icon color="blue" icon="mdi-credit-card"></v-icon>
                    <p>Tarjeta <strong>{{ formatCurrency(resumen?.totalTarjeta || 0) }}</strong></p>
                  </v-list-item>
                  <v-list-item>
                    <v-icon color="purple" icon="mdi-bank-transfer"></v-icon>
                    <p>Transferencia <strong>{{ formatCurrency(resumen?.totalTransferencia || 0) }}</strong></p>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="5">
            <v-card  variant="outlined">
              <v-card-title>
                Producto estrella
              </v-card-title>
              <v-card-text>
                {{ resumen?.productoMasVendido?.nombre || 'No hay ventas' }}
                <br>
                {{ formatCurrency(resumen?.productoMasVendido?.cantidad || 0) }} 
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
       
    </v-card>
  </div>
</template>

<script setup>
import { useVentas } from '@/composables/calculateSales.js'
import {  onMounted, ref } from 'vue'
import supabase from '@/supabase.js'
import { getMexicoLocalString } from '../../composables/localtime.js';
import useTime from "@/composables/datetime.js";

const { 
  formatDate,
  formatDateWithDay,
  getRelativeTime,
  isToday,
  getDateComponents,
  formatos
} = useTime()

const { fetchVentasPorFecha } = useVentas()

import formatCurrency  from '@/composables/formatCurrency.js'

const ventas = ref([])
const totalVentas = ref(0)


const resumen = ref({})




const getVentas = async () => {
  try {
    // Obtener la fecha de inicio del día en hora local de México (00:00:00)
    const mexicoDate = getMexicoLocalString()
    const startOfDay = mexicoDate.split(' ')[0] + ' 00:00:00'

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
      .gte('created_at', startOfDay)

    if (error) {
      console.error('Error al obtener ventas:', error)
      return
    }

    ventas.value = data

    // Calcular el total de ventas
    totalVentas.value = ventas.value.reduce((acc, venta) => acc + venta.total, 0)



  } catch (err) {
    console.error('Error inesperado:', err)
  }
}
onMounted(async ()  => {
  resumen.value =  await fetchVentasPorFecha()
  console.log('resumen.value', resumen.value);
  
})

</script>
