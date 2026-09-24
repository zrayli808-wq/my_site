<template>
  <header class="navbar">
    <router-link to="/" class="brand">
      <img src="/logo.png" alt="ZRay" class="brand-logo" />
    </router-link>
    <nav class="nav-links">
      <router-link to="/?scroll=design">{{ t('nav.design') }}</router-link>
      <router-link to="/?scroll=music">{{ t('nav.music') }}</router-link>
      <router-link to="/?scroll=career">{{ t('nav.about') }}</router-link>
    </nav>
    <div class="language-selector">
      <select v-model="lang">
        <option value="zh">中文</option>
        <option value="en">English</option>
      </select>
    </div>
  </header>
</template>

<script setup>
import { computed, inject } from 'vue'

// ★★★ 注入国际化 ★★★
const i18n = inject('i18n')
const { t, setLang, currentLang } = i18n

// 语言选择器绑定
const lang = computed({
  get: () => currentLang.value,
  set: (value) => setLang(value)
})
</script>

<style scoped>
.navbar {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 64px;
  z-index: 100;
  background: transparent !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  border-bottom: none;
  box-shadow: none !important;
  display: flex;
  align-items: center;
  padding: 0 32px 0 28px;
  box-sizing: border-box;
}

.brand {
  flex-shrink: 0;
  text-decoration: none;
  display: flex;
  align-items: center;
  line-height: 1;
  margin-left: 16px;
}

.brand-logo {
  height: 56px;
  width: auto;
  display: block;
  transition: opacity 0.3s ease;
}

.brand:hover .brand-logo {
  opacity: 0.8;
}

.nav-links {
  display: flex;
  gap: 40px;
  align-items: center;
  margin-left: auto;
  margin-right: 32px;
}

.nav-links a {
  font-family: 'Georgia', 'Times New Roman', serif;
  color: #e5d4a0;
  text-decoration: none;
  font-size: 18px;
  font-weight: 300;
  letter-spacing: 3px;
  padding: 4px 0;
  white-space: nowrap;
  transition: none;
}

.nav-links a:hover,
.nav-links a.router-link-active,
.nav-links a.router-link-exact-active {
  color: #e5d4a0;
}

.language-selector {
  flex-shrink: 0;
  margin-left: 0;
}
.language-selector select {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  font-size: 14px;
  font-weight: 300;
  letter-spacing: 1px;
  padding: 4px 6px;
  cursor: pointer;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  font-family: 'Georgia', 'Times New Roman', serif;
  transition: none;
}
.language-selector select:hover {
  color: rgba(255, 255, 255, 0.7);
}
.language-selector select option {
  background: #1a1a1a;
  color: #e8c84e;
}

@media (max-width: 820px) {
  .navbar { height: 56px; padding: 0 16px; }
  .brand { margin-left: 12px; }
  .brand-logo { height: 46px; }
  .nav-links { gap: 24px; margin-right: 16px; }
  .nav-links a { font-size: 15px; letter-spacing: 2px; }
}

@media (max-width: 600px) {
  .navbar { height: 50px; padding: 0 12px; }
  .brand { margin-left: 8px; }
  .brand-logo { height: 38px; }
  .nav-links { gap: 14px; margin-right: 12px; }
  .nav-links a { font-size: 12px; letter-spacing: 1px; }
  .language-selector select { font-size: 12px; }
}

@media (max-width: 480px) {
  .navbar { height: 44px; padding: 0 10px; }
  .brand { margin-left: 4px; }
  .brand-logo { height: 30px; }
  .nav-links { gap: 10px; margin-right: 8px; }
  .nav-links a { font-size: 10px; letter-spacing: 0.5px; }
  .language-selector select { font-size: 10px; }
}
</style>