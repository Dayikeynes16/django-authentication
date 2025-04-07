<template>
    <v-container>
        <snackbar  :type="notificationType" :message="notificationMessage" :show="showNotification"></snackbar>
        <v-row>
            <v-col cols="6">
                <v-card variant="outlined">
                    <v-card-title>
                        Nueva Venta
                    </v-card-title>
                    <v-card-text>
                        <v-select 
                            :items="productos" 
                            v-model="select" 
                            item-value="id" 
                            item-title="nombre" 
                            label="Selecciona un producto">
                        </v-select>

                        <v-row>
                            <v-col cols="12">
                                
                            </v-col>
                            <v-col cols="6">
                                <v-text-field 
                                    label="Peso del producto" 
                                    v-model="selectedProducto.peso" 
                                    type="number"
                                    
                                    min="0">
                                </v-text-field>
                            </v-col>
                            <v-col cols="6" >
                                Peso: {{ parseFloat(selectedProducto.peso).toFixed(2) }} KG
                            </v-col>
                            <v-col cols="6">
                                <v-text-field 
                                    :disabled="selectedProducto.disabled"
                                    v-model="selectedProducto.precio_de_venta"  
                                    label="Precio" 
                                    type="number"
                                    min="0">
                                </v-text-field>
                            </v-col>
                            <v-col cols="2">
                                <V-icon icon="mdi-pencil" @click="toggleDisabled" ></V-icon>
                            </v-col>
                            <v-col cols="4">
                                total: {{ formatCurrency((selectedProducto.peso * selectedProducto.precio_de_venta).toFixed(2)) }}
                            </v-col>


                        </v-row>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="green" variant="outlined" @click="addProducto">Añadir Producto</v-btn>
                        <v-btn color="red" variant="outlined" @click="limpiarCampos">Cancelar</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
            <v-col cols="6">
                <v-card variant="outlined">
                    <v-card-title>
                        Productos de la venta total: {{ formatCurrency(get_total()) }}    
                    </v-card-title>
                    <v-card-text>
                      <table  class="table table-hover table-borderless" >
                        <thead>
                            <tr>
                                <th>Producto</th>
                                <th>Peso</th>
                                <th>Precio</th>
                                <th>Total</th>
                                <th>Eliminar</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(producto, index) in productosVenta" :key="index">
                                <td>{{ producto.nombre }}</td>
                                <td>{{ producto.peso }} KG</td>
                                <td>{{ formatCurrency(producto.precio_de_venta) }}</td>
                                <td>{{ formatCurrency(producto.total) }}</td>
                                <td class="align-center">
                                    
                                    <v-icon  icon="mdi-delete-alert" color="red"   @click="productosVenta.splice(index, 1)"></v-icon>
                                </td>
                            </tr>
                        </tbody>
                      </table>
                    </v-card-text>
                    <v-card-actions class="">
                        <v-btn color="green" variant="outlined" @click="AgregarVenta">Finalizar</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>
<script setup>
import { onMounted, ref, shallowRef, watch } from 'vue'
import formatCurrency from '@/composables/formatCurrency'
import supabase from '@/supabase.js'
import snackbar from '@/components/snackbar.vue'
import { getMexicoLocalString } from '@/composables/localtime'
const piezas = ref(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
const productosVenta = ref([])
const showNotification = ref(false);
const notificationType = ref('');
const notificationMessage = ref('');

const headers = [
    { text: 'Producto', value: 'nombre' },
    { text: 'Peso', value: 'peso' },
    { text: 'Precio', value: 'precio_de_venta' },
    { text: 'Total', value: 'total' }
]

const NewVenta = ref()



const productos = ref([])
const select = shallowRef(null)

const get_ventas = async () => {
    const { data, error } = await supabase
        .from('productos')
        .select('*')
    if (error) {
        console.error(error)
    } else {
        productos.value = data
    }
}

const toggleDisabled = () => {
    selectedProducto.value.disabled = !selectedProducto.value.disabled;
};

watch(productosVenta, (nuevoProducto) => {
    if (nuevoProducto) {
        get_total()
    }
})

const get_total = () => {
    let total = 0
    productosVenta.value.forEach(producto => {
        total += producto.total
    })
    
    return total
}


const addProducto = async () => {
    try {
        const producto_venta = {
            nombre: selectedProducto.value.nombre,
            peso: parseFloat(selectedProducto.value.peso),
            precio_de_venta: parseFloat(selectedProducto.value.precio_de_venta),
            total: parseFloat(selectedProducto.value.peso) * parseFloat(selectedProducto.value.precio_de_venta),
            producto_id: selectedProducto.value.id
        }
    
        productosVenta.value.push(producto_venta)
        showNotification.value = true
        notificationType.value = 'success'
        notificationMessage.value = 'Producto añadido correctamente'
        limpiarCampos()
        console.log("Producto añadido:", productosVenta.value);
        
        
    } catch (error) {
        
    }



}


const selectedProducto = ref({
    peso: 0,
    precio_de_venta: 0,
    disabled: true
})

const newVenta = ref({
    peso: 0,
    precio_de_venta: 0,
    total: 0
})

const AgregarVenta = async () => {
    try {
        // Insertar la venta en la tabla 'ventas'
        const { data: ventaData, error: ventaError } = await supabase
            .from('ventas')
            .insert({
                created_at: getMexicoLocalString(),
                balanza: '0',
                total: parseFloat(get_total()),
                estatus: 'activo'
            })
            .select();
        
        if (ventaError) {
            console.error("Error al registrar la venta:", ventaError);
            return;
        }

        // Obtener el ID de la venta recién creada
        const ventaId = ventaData[0].id;

        // Preparar los productos para la inserción masiva
        const productosParaInsertar = productosVenta.value.map((producto) => ({
            created_at: getMexicoLocalString(),
            peso: parseFloat(producto.peso),
            precio: parseFloat(producto.precio_de_venta),
            total: parseFloat(producto.total),
            venta_id: ventaId,
            producto_id: producto.producto_id
        }));

        // Insertar los productos en la tabla 'producto_ventas'
        const { data: productosData, error: productosError } = await supabase
            .from('producto_ventas')
            .insert(productosParaInsertar)
            .select();

        if (productosError) {
            console.error("Error al registrar los productos:", productosError);
            return;
        }

        console.log("Venta y productos registrados correctamente:", ventaData, productosData);

        // Notificación de éxito
        showNotification.value = true;
        notificationType.value = 'success';
        notificationMessage.value = 'Venta registrada correctamente';
        
        // Limpiar campos y lista de productos
        productosVenta.value = [];
        limpiarCampos();
        
    } catch (error) {
        console.error("Error en el proceso de registro de la venta:", error);
    }
};



const limpiarCampos = () => {
    newVenta.value.peso = 0
    newVenta.value.precio_de_venta = 0
    select.value = null
    
}

onMounted(() => {
    get_ventas()
})

watch(select, (nuevoProducto) => {
    if (nuevoProducto) {
        selectedProducto.value = productos.value.find(producto => producto.id === nuevoProducto);
        selectedProducto.value.precio_de_venta = productos.value.find(producto => producto.id === nuevoProducto).precio_de_venta;
        selectedProducto.value.peso = 0
        selectedProducto.value.disabled = false;


    }
})
</script>
