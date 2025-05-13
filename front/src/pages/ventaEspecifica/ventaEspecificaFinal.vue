<template>
    
        <v-row class="ma-5">
            <v-col cols="7">
                <venta v-if="showSale" :venta="ventaEspecifica"></venta>
            </v-col>
            <v-col cols="5"> 
                <pagos v-if="showSale" :venta="ventaEspecifica"></pagos>
            </v-col>
        </v-row>
   
    
</template>
<script setup>
import supabase from '@/supabase';
import { ref, onMounted } from 'vue';
import { useRouter,useRoute } from 'vue-router';
import venta from '../ventas/venta.vue';
import pagos from '../ventas/cobrando/pagos.vue';

const router = useRouter();
const route = useRoute();

const ventaEspecifica = ref(null);
const showSale = ref(false);
const id = ref(null);
const pago = ref(null);

onMounted(async () => {
 showSale.value = false;
  id.value = route.params.id;
  console.log('este es el ID:', id.value);
  getSpecificVenta(id.value);
  
});

const getSpecificVenta = async () => {
  const { data, error } = await supabase
    .from('ventas')
    .select(`
        pagos(*), 
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
    .eq('id', id.value)
    .single();

  if (error) {
    console.error('Error al obtener la venta específica:', error);
  } else {
    console.log('hey hey ehye ');
    
    console.log('Venta específica:', data);
    ventaEspecifica.value = data;
    showSale.value = true;
    const pagos = data.pagos;
  }
};

</script>