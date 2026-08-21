import { ref, computed } from 'vue'

import zh from '../locales/zh.js'
import en from '../locales/en.js'

const locales = { zh, en }
const currentLang = ref('zh')

export function useI18n() {
  function setLang(lang) {
    if (locales[lang]) {
      currentLang.value = lang
      localStorage.setItem('lang', lang)
    }
  }

  const t = computed(() => {
    return locales[currentLang.value] || locales.zh
  })

  function translate(key) {
    const keys = key.split('.')
    let result = t.value
    for (const k of keys) {
      if (result && result[k] !== undefined) {
        result = result[k]
      } else {
        console.warn(`Translation key not found: ${key}`)
        return key
      }
    }
    return result
  }

  function initLang() {
    const saved = localStorage.getItem('lang')
    if (saved && locales[saved]) {
      currentLang.value = saved
    } else {
      currentLang.value = 'zh'
    }
  }

  return {
    currentLang,
    setLang,
    t: translate,
    initLang
  }
}