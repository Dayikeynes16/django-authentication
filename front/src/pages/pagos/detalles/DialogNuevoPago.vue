<template>
  <v-dialog v-model="visibleLocal" max-width="600px" persistent>
    <v-card>
      <v-card-title class="text-h6">Registrar nuevo pago</v-card-title>

      <v-card-text>
        <v-form @submit.prevent="emitirGuardar" ref="formRef">
          <v-text-field
            v-model="form.total"
            label="Monto pagado"
            type="number"
            required
          />

          <v-select
            v-model="form.metodo"
            :items="['efectivo', 'tarjeta', 'transferencia']"
            label="Método de pago"
            required
          />

          <v-autocomplete
            v-model="form.cliente_id"
            :items="clientes"
            item-title="nombre"
            item-value="id"
            label="Cliente (opcional)"
            clearable
          />

          <v-text-field
            v-model="form.venta_id"
            label="ID de venta (opcional)"
            type="text"
            clearable
          />

          <v-textarea
            v-model="form.comentario"
            label="Comentario (opcional)"
            rows="2"
            auto-grow
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn text @click="cancelar">Cancelar</v-btn>
        <v-btn color="primary" @click="emitirGuardar">Guardar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  visible: Boolean,
  clientes: Array, // [{ id, nombre }]
})

const emit = defineEmits(['update:visible', 'guardar'])

const visibleLocal = ref(props.visible)

watch(() => props.visible, (val) => {
  visibleLocal.value = val
})
watch(visibleLocal, (val) => {
  emit('update:visible', val)
})

const form = ref({
  total: null,
  metodo: null,
  cliente_id: null,
  venta_id: null,
  comentario: ''
})

const formRef = ref(null)

const emitirGuardar = () => {
  if (!form.value.total || !form.value.metodo) return

  emit('guardar', { ...form.value })
  limpiar()
  visibleLocal.value = false
}

const cancelar = () => {
  limpiar()
  visibleLocal.value = false
}

const limpiar = () => {
  form.value = {
    total: null,
    metodo: null,
    cliente_id: null,
    venta_id: null,
    comentario: ''
  }
}
</script>
