import { createApp } from 'vue'
import App from './App.vue'
import components from '@/components/UI';
import directives from '@/directives';
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'

loadFonts()

const app = createApp(App)

components.forEach(component => {
  app.component(component.name, component)
})

directives.forEach(directive => {
  app.directive(directive.name, directive)
})

app
  .use(router)
  .use(store)
  .use(vuetify)
  .mount('#app')
