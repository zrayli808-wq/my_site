import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const showNavBar = ref(true)

  function hideNavBar() {
    showNavBar.value = false
  }

  function showNavBarFn() {
    showNavBar.value = true
  }

  return {
    showNavBar,
    hideNavBar,
    showNavBarFn
  }
})