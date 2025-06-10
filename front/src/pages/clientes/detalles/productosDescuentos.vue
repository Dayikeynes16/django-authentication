<template>
  <v-container>
    <!-- Sin descuentos -->
    <v-card v-if="!productos" variant="outlined" class="pa-5">
      <v-card-title>Productos con descuento</v-card-title>
      <v-card-text>
        Este cliente no cuenta con productos con descuento.
      </v-card-text>
      <v-card-actions class="pt-0">
        <v-btn
          block
          color="green"
          variant="flat"
          prepend-icon="mdi-tag"
          @click="abrirDialog()"
        >
          Nuevo descuento
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Con descuentos -->
    <v-card v-else variant="outlined" class="pa-5">
      <v-card-title>Productos con descuento</v-card-title>
      <v-card-text>
        <v-row v-for="(producto, index) in productos" :key="index">
          <v-card class="mx-2 my-2" width="100%" variant="outlined">
            <v-card-title>
              {{ producto.productos.nombre }}
            </v-card-title>
            <v-card-subtitle>
              <v-row>
                <v-col class="text-left" cols="6">Precio con descuento</v-col>
                <v-col class="text-right" cols="6">Precio normal</v-col>
              </v-row>
            </v-card-subtitle>
            <v-card-text>
              <v-row>
                <v-col class="text-left" cols="6">
                  <strong>{{ formatCurrency(producto.precio) }}</strong>
                </v-col>
                <v-col class="text-right" cols="6">
                  <strong>{{ formatCurrency(producto.productos.precio_de_venta) }}</strong>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-row>
                <v-col cols="6">
                  <v-btn
                    append-icon="mdi-delete"
                    color="red"
                    block
                    variant="flat"
                    @click="eliminarDescuento(producto.id)"
                  >
                    Eliminar
                  </v-btn>
                </v-col>
                <v-col cols="6">
                  <v-btn
                    color="green"
                    append-icon="mdi-pencil"
                    block
                    variant="flat"
                    @click="abrirDialog(producto)"
                  >
                    Editar
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-actions>
          </v-card>
        </v-row>
      </v-card-text>
      <v-card-actions class="pt-0">
        <v-btn
          block
          color="green"
          variant="flat"
          prepend-icon="mdi-tag"
          @click="abrirDialog()"
        >
          Nuevo descuento
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Diálogo para crear/editar -->
    <v-dialog v-model="dialog" max-width="500px">
      <nuevoDescuento
        :cliente_id="cliente.id"
        :descuento="productoSeleccionado"
        @cerrar="cerrarDialog"
        @creado="handleCreado"
      />
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import supabase from '@/supabase'
import formatCurrency from '@/composables/formatCurrency'
import nuevoDescuento from '../nuevoDescuento.vue'

const props = defineProps({
  productos: {
    type: Array,
    required: true
  },
  cliente: {
    type: Object,
    required: true
  }
})

const emits = defineEmits(['creado'])

const dialog = ref(false)
const productoSeleccionado = ref(null)

const abrirDialog = (producto = null) => {
  productoSeleccionado.value = producto
  dialog.value = true
}

const cerrarDialog = () => {
  dialog.value = false
  productoSeleccionado.value = null
}

const handleCreado = () => {
  emits('creado')
  cerrarDialog()
}

const eliminarDescuento = async (id) => {
  const { error } = await supabase
    .from('precio_especials')
    .delete()
    .eq('id', id)

  if (error) {
    console.error('Error al eliminar descuento:', error)
    alert('Error al eliminar el descuento.')
  } else {
    alert('Descuento eliminado correctamente.')
    emits('creado')
  }
}
</script>
