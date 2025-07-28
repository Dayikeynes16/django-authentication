<template>
  <v-dialog v-model="dialogInterno" max-width="500" @update:model-value="emit('update:modelValue', $event)">
    <v-card>
      <v-card-title class="text-h6">Editar Pago</v-card-title>

      <v-card-subtitle v-if="pagoEdit.ventas">
        Venta asociada: <strong>#{{ pagoEdit.ventas }}</strong>
      </v-card-subtitle>

      <v-divider class="mb-2" />
      <v-card-text>
        <v-form @submit.prevent="guardarPago">
          <v-switch
            v-model="pagoEdit.anulado"
            label="¿Anular este pago?"
            color="red"
            inset
            class="mb-2"
          />

          <v-text-field
            v-model.number="pagoEdit.total"
            label="Monto"
            type="number"
            :disabled="pagoEdit.anulado"
            prepend-inner-icon="mdi-currency-usd"
            class="mb-3"
            hide-details
          />

          <v-select
            v-model="pagoEdit.metodo"
            :items="['efectivo', 'tarjeta', 'transferencia']"
            label="Método de Pago"
            :disabled="pagoEdit.anulado"
            prepend-inner-icon="mdi-credit-card"
            class="mb-3"
            hide-details
          />

          <v-textarea
            v-model="pagoEdit.comentario"
            label="Comentario"
            rows="2"
            auto-grow
            :disabled="pagoEdit.anulado"
            prepend-inner-icon="mdi-comment-text-outline"
            hide-details
          />
        </v-form>
      </v-card-text>

      <v-divider />

      <v-card-actions>
        <v-spacer />
        <v-btn color="grey" variant="text" @click="emit('update:modelValue', false)">
          Cancelar
        </v-btn>
        <v-btn
          color="primary"
          :loading="cargando"
          :disabled="cargando"
          @click="guardarPago"
        >
          Guardar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch,onMounted } from 'vue'
import { useEditarPago } from '../../../composables/useEditarPago'

// Props
const props = defineProps({
  modelValue: { type: Boolean, required: true }, // Control externo del diálogo
  pago: { type: Object, required: true } // Objeto del pago a editar
})

const emit = defineEmits(['update:modelValue', 'actualizado'])

const dialogInterno = ref(false)
const pagoEdit = ref({})

const { editarPago, cargando, error } = useEditarPago()

// Mantener sincronización con el prop externo
// watch(
//   () => props.modelValue,
//   (val) => {
//     dialogInterno.value = val
//     if (val && props.pago) {
//       pagoEdit.value = JSON.parse(JSON.stringify(props.pago)) // clonado seguro
//     }
//   }
// )

watch(
  () => props.pago,
  (val) => {
    if (val) {
      pagoEdit.value = val // Clonado seguro
      dialogInterno.value = true // Abrir diálogo al recibir un pago
    }
  },
  { immediate: true }
)

async function guardarPago() {
  const resultado = await editarPago(pagoEdit.value)
  if (resultado.ok) {
    emit('actualizado', pagoEdit.value)
    emit('update:modelValue', false) // cerrar
  } else {
    console.error(error.value)
  }
}

onMounted(() => {
  if (props.pago) {
    pagoEdit.value = props.pago // Clonado seguro
    dialogInterno.value = true // Abrir diálogo al montar
    console.log('Editando pago:', pagoEdit.value);
    
  }

})
</script>
