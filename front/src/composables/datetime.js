// composables/useTime.js
import dayjs from 'dayjs'
import 'dayjs/locale/es' // 
import utc from 'dayjs/plugin/utc'
import relativeTime from 'dayjs/plugin/relativeTime'
import customParseFormat from 'dayjs/plugin/customParseFormat'

// Configurar plugins
dayjs.extend(utc)
dayjs.extend(relativeTime)
dayjs.extend(customParseFormat)
dayjs.locale('es')

export default function useTime() {
  // Formateos comunes
  const formatos = {
    fechaCorta: 'DD/MM/YYYY',
    fechaLarga: 'DD [de] MMMM [de] YYYY',
    fechaHora: 'DD/MM/YYYY HH:mm',
    horaCorta: 'HH:mm',
    mesAnio: 'MMMM YYYY'
  }
    /**
     * Formatea una fecha con el nombre del día de la semana
     * @param {string} dateStr - Fecha en formato ISO o 'YYYY-MM-DD'
     * @returns {string} Fecha formateada con el día de la semana
     */
    const formatDateWithDay = (dateStr) => {
        const fecha = dayjs(dateStr).utc()
        return fecha.isValid() 
        ? fecha.format('dddd D [de] MMMM [de] YYYY') // Ejemplo: miércoles 12 de marzo de 2025
        : 'Fecha inválida'
    }
  

  /**
   * Formatea una fecha según el formato especificado
   * @param {string} dateStr - Fecha en formato ISO o 'YYYY-MM-DD'
   * @param {string} formato - Formato deseado (puede usar los nombres predefinidos o formato day.js)
   * @returns {string} Fecha formateada
   */
  const formatDate = (dateStr, formato = 'fechaCorta') => {
    const fecha = dayjs(dateStr).utc()
    return fecha.isValid() 
      ? fecha.format(formatos[formato] || formato)
      : 'Fecha inválida'
  }

  /**
   * Tiempo relativo en español mejorado
   * @param {string} dateStr - Fecha en formato ISO
   * @returns {string} Tiempo relativo en español natural
   */
  const getRelativeTime = (dateStr) => {
    const fecha = dayjs(dateStr).utc()
    if (!fecha.isValid()) return 'Fecha inválida'
    
    const ahora = dayjs().utc()
    const minutosDiff = ahora.diff(fecha, 'minute')
    
    // Casos especiales para mayor legibilidad
    if (minutosDiff < 1) return 'hace unos segundos'
    if (minutosDiff < 60) return `hace ${minutosDiff} minuto${minutosDiff > 1 ? 's' : ''}`
    
    const horasDiff = ahora.diff(fecha, 'hour')
    if (horasDiff < 24) {
      const minutosRestantes = minutosDiff % 60
      const tiempo = `hace ${horasDiff} hora${horasDiff > 1 ? 's' : ''}`
      return minutosRestantes > 0 
        ? `${tiempo} y ${minutosRestantes} minuto${minutosRestantes > 1 ? 's' : ''}`
        : tiempo
    }
    
    return fecha.fromNow()
  }

  /**
   * Verifica si una fecha es hoy
   * @param {string} dateStr - Fecha en formato ISO
   * @returns {boolean}
   */
  const isToday = (dateStr) => {
    const fecha = dayjs(dateStr).utc()
    return fecha.isValid() && fecha.isSame(dayjs().utc(), 'day')
  }

  /**
   * Obtiene componentes detallados de una fecha
   * @param {string} dateStr - Fecha en formato ISO
   * @returns {Object} Componentes de la fecha
   */
  const getDateComponents = (dateStr) => {
    const fecha = dayjs(dateStr).utc()
    return {
      año: fecha.year(),
      mes: fecha.month() + 1, // 1-12
      dia: fecha.date(),
      hora: fecha.hour(),
      minuto: fecha.minute(),
      segundo: fecha.second(),
      diaSemana: fecha.day() // 0 (domingo) - 6 (sábado)
    }
  }

  return {
    formatDate,
    getRelativeTime,
    formatDateWithDay,
    isToday,
    getDateComponents,
    formatos // Exportar los formatos predefinidos
  }
}