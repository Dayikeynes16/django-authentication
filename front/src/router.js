import { createMemoryHistory, createRouter } from 'vue-router'

import HelloWorld from './components/HelloWorld.vue'
import inicio from './pages/inicio.vue'
import pagina2 from './pages/pagina2.vue'
import Login from './components/HelloWorld.vue'  // Asegúrate de importar tu login
import Inventario from './pages/Inventario.vue'
import ventas from './pages/ventas/ventas.vue'
import totalVentas from './pages/ventas/totalVentas.vue'
import ventasBusqueda from './pages/ventas/ventasBusqueda.vue'
import insertarVenta from './pages/ventas/insertarVenta.vue'
import clientes from './pages/clientes/clientes.vue'
import clientesDetalles from './pages/clientes/clientesDetalles.vue'
import ventaEspecifica from './pages/ventaEspecifica/ventaEspecificaFinal.vue'


const routes = [
  { path: '/', redirect: '/ventas' },  // Redirigir a /inicio por defecto
  { path: '/login', component: Login },
  { path: '/inicio', component: inicio, meta: { requiresAuth: true } },  // Ruta protegida
  { path: '/pagina2', component: pagina2, meta: { requiresAuth: true }, name: 'login' }, // Ruta protegida
  { path: '/clientes', component: clientes, meta: { requiresAuth: true }},
  { path: '/ventas', component: ventas, meta: { requiresAuth: true }},
  { path: '/totalVentas', component: ventasBusqueda, meta: { requiresAuth: true }}, 
  { path: '/insertarVenta', component: insertarVenta, meta: { requiresAuth: true }},
  { path: '/clientesDetalles/:id', name: 'clientesDetalles' ,component: clientesDetalles, meta: { requiresAuth: true }}, // Ruta protegida
  { path: '/ventaEspecifica/:id', name: 'ventaEspecifica' ,component: ventaEspecifica, meta: { requiresAuth: true }}, // Ruta protegida


]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

// Guard para proteger rutas
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("access");  // Verifica si hay un token

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');  // Redirigir al login si no está autenticado
  } else {
    next();  // Permitir el acceso
  }
});

export { router };
