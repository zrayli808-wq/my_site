<template>
  <div class="about-page">
    <div class="container">
      <h1 class="page-title">{{ t('about.title') }}</h1>
      <p class="page-sub">{{ t('about.subtitle') }}</p>
      <div class="divider"></div>
      <div class="content">
        <p class="about-text">{{ t('about.text1') }}</p>
        <p class="about-text">{{ t('about.text2') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject } from 'vue'

// ★★★ 注入国际化 ★★★
const i18n = inject('i18n')
const { t } = i18n
</script>

<style scoped>
.about-page {
  min-height: 100vh;
  background: #f8f8f8;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 120px 24px 60px;
}

.container {
  max-width: 720px;
  width: 100%;
}

.page-title {
  font-size: 48px;
  font-weight: 300;
  letter-spacing: 4px;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.page-sub {
  font-size: 18px;
  font-weight: 300;
  color: #888888;
  letter-spacing: 2px;
  margin: 0 0 24px 0;
}

.divider {
  width: 60px;
  height: 1px;
  background: #cccccc;
  margin: 0 0 40px 0;
}

.content {
  background: #ffffff;
  padding: 40px 48px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.04);
}

.about-text {
  font-size: 18px;
  font-weight: 300;
  line-height: 1.8;
  color: #333333;
  margin: 0 0 20px 0;
}

.about-text:last-child {
  margin-bottom: 0;
}
</style>