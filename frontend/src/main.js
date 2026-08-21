import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'

// 全局样式
import './styles/variables.css'
import './styles/reset.css'
import './styles/globals.css'

// 组件样式
import './styles/components/player.css'
import './styles/components/playlist.css'
import './styles/components/album-detail.css'

// 页面样式
import './styles/views/music.css'
import './styles/views/work.css'

import App from './App.vue'
import router from './router'
import RainEffect from './components/RainEffect.vue'

// ★★★ 导入国际化工具 ★★★
import { useI18n } from './composables/useI18n'

const app = createApp(App)

// 全局注册雨特效组件
app.component('RainEffect', RainEffect)

// ★★★ 全局提供国际化 ★★★
const i18n = useI18n()
i18n.initLang()
app.provide('i18n', i18n)

app.use(router)
app.use(createPinia())
app.mount('#app')