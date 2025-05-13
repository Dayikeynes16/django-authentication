import supabase from '@/supabase.js'
import { getMexicoLocalString } from '@/composables/localtime.js'
import { ref } from 'vue'
import { no } from 'vuetify/locale'

export const useVentas = () => {

  
  const productos = ref({})
  const productos_ventas = ref([])
  const ventas = ref([])

  const fetchVentasPorFecha = async (fecha = null) => {
    try {

      // Si no pasaron fecha, usar la fecha local de México
      let selectedDate;

      if (!fecha) {
        const mexicoDate = getMexicoLocalString(); // Ejemplo: 2025-05-02 14:00:00
        selectedDate = mexicoDate.split(' ')[0];   // Solo la fecha "2025-05-02"
      } else {
        selectedDate = fecha; // Si mandaron fecha, la usamos tal cual
      }

      const startOfDay = `${selectedDate} 00:00:00`
      const endOfDay = `${selectedDate} 23:59:59`

      const { data, error } = await supabase
        .from('ventas')
        .select(`
            *,
            pagos(*),
            producto_ventas(
              *,
              productos(id, nombre)
            )
          `)
          
        .eq('estatus', 'cobrado')
        .gte('created_at', startOfDay)
        .lte('created_at', endOfDay)
        .limit(5000)


      if (error) {
        console.error('Error al obtener ventas aaaaaa:', error)
        return null

      }

      ventas.value = data
      productos_resumen(data)

      const resumen = {
        totalVendido: 0,
        totalEfectivo: 0,
        totalTarjeta: 0,
        totalTransferencia: 0,
        productos: null,
        totalVentas: data.length,
        ticketPromedio: 0,
        productoMasVendido: null,
        metodoPagoMasUsado: null,
        ventas: data
      }

      const productosVendidos = {}
      const metodosPagoContador = {}

      data.forEach(venta => {
        resumen.totalVendido += venta.total

        if (venta.producto_ventas?.length) {
          venta.producto_ventas.forEach(pv => {
            const nombre = pv.productos?.nombre ?? 'Desconocido'
            productosVendidos[nombre] = (productosVendidos[nombre] || 0) + pv.total
          })
        }

        if (venta.pagos?.length) {
          venta.pagos.forEach(pago => {
            metodosPagoContador[pago.metodo] = (metodosPagoContador[pago.metodo] || 0) + pago.cantidad

            switch (pago.metodo) {
              case 'efectivo':
                resumen.totalEfectivo += pago.total
                break
              case 'tarjeta':
                resumen.totalTarjeta += pago.total
                break
              case 'transferencia':
                resumen.totalTransferencia += pago.total
                break
              default:
                resumen.totalOtros += pago.total
                break
            }
          })
        }
      })

      resumen.ticketPromedio = resumen.totalVentas > 0
        ? resumen.totalVendido / resumen.totalVentas
        : 0

      const productoMasVendido = Object.entries(productosVendidos).sort((a, b) => b[1] - a[1])[0]
      resumen.productoMasVendido = productoMasVendido ? { nombre: productoMasVendido[0], cantidad: productoMasVendido[1] } : null

      const metodoMasUsado = Object.entries(metodosPagoContador).sort((a, b) => b[1] - a[1])[0]
      resumen.metodoPagoMasUsado = metodoMasUsado ? { metodo: metodoMasUsado[0], cantidad: metodoMasUsado[1] } : null
      resumen.productos = productos.value
      return resumen

    } catch (err) {
      console.error('Error inesperado:', err)
      return null
    }
  }

  const productos_resumen =  (ventas) => {
    for (const venta of ventas) {
      for (const producto_venta of venta.producto_ventas) {

        const id = producto_venta.producto_id;
        const nombre = producto_venta.productos?.nombre || "Desconocido";
        const cantidad = producto_venta.peso;
        const total = producto_venta.total;

        if (productos.value[id]) {
          productos.value[id].cantidad += cantidad;
          productos.value[id].total += total;
        } else {
          productos.value[id] = {
            nombre: nombre,
            cantidad: cantidad,
            total: total
          }
        }
      }
      
    }
    
  }


  
  

  return {
    fetchVentasPorFecha
  }
}
