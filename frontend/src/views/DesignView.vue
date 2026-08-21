<template>
  <div
    class="fullscreen-view"
    @mousedown="startDrag"
    @wheel.prevent="onWheel"
    :class="{ 'is-dragging': isDragging }"
  >
    <button class="close-btn" @click="closeDetail">{{ t('design.close') }}</button>

    <div class="gallery-wrapper" ref="wrapperRef">
      <div class="gallery-track" :style="trackStyle" ref="trackRef">
        <div
          v-for="(img, idx) in images"
          :key="idx"
          class="gallery-slide"
        >
          <img
            :src="img"
            :alt="'作品 ' + (idx + 1)"
            draggable="false"
            @load="onImageLoad"
          />
        </div>
      </div>
    </div>

    <div class="bottom-nav">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, inject } from 'vue'
import { useRouter } from 'vue-router'

// ★★★ 注入国际化 ★★★
const i18n = inject('i18n')
const { t } = i18n

const router = useRouter()

// ===== 图片数据 =====
const images = [
  '/designs/design1/Cover1.png',
  ...Array.from({ length: 25 }, (_, i) => `/designs/design1/P${i + 2}.png`)
]

// ===== 画廊状态 =====
const wrapperRef = ref(null)
const trackRef = ref(null)

const isDragging = ref(false)
const startX = ref(0)
const startScrollX = ref(0)
const scrollX = ref(0)

const wrapperWidth = ref(0)
const totalWidth = ref(0)
let imagesLoaded = 0

const maxScroll = computed(() => {
  return Math.max(0, totalWidth.value - wrapperWidth.value)
})

const progressPercent = computed(() => {
  if (maxScroll.value === 0) return 0
  return (scrollX.value / maxScroll.value) * 100
})

const trackStyle = computed(() => {
  return {
    transform: `translateX(-${scrollX.value}px)`,
    transition: 'none'
  }
})

// ===== 关闭 =====
function closeDetail() {
  router.push('/?scroll=design')
}

// ===== 拖拽 =====
function startDrag(e) {
  isDragging.value = true
  startX.value = e.clientX
  startScrollX.value = scrollX.value
  document.body.style.cursor = 'grabbing'
  document.body.style.userSelect = 'none'
}

function onDrag(e) {
  if (!isDragging.value) return
  const diff = startX.value - e.clientX
  let newScrollX = startScrollX.value + diff
  newScrollX = Math.max(0, Math.min(newScrollX, maxScroll.value))
  scrollX.value = newScrollX
}

function endDrag() {
  if (!isDragging.value) return
  isDragging.value = false
  document.body.style.cursor = ''
  document.body.style.userSelect = ''
}

// ===== 滚轮 =====
function onWheel(e) {
  const delta = e.deltaY || e.deltaX
  let newScrollX = scrollX.value + delta
  newScrollX = Math.max(0, Math.min(newScrollX, maxScroll.value))
  scrollX.value = newScrollX
}

// ===== 图片加载 =====
function onImageLoad() {
  imagesLoaded++
  if (imagesLoaded >= images.length) {
    calculateTotalWidth()
  }
}

// ===== 计算总宽度 & 居中第一张 =====
async function calculateTotalWidth() {
  await nextTick()
  if (!trackRef.value) return
  const slides = trackRef.value.querySelectorAll('.gallery-slide')
  if (slides.length === 0) return

  wrapperWidth.value = wrapperRef.value?.offsetWidth || window.innerWidth

  let total = 0
  slides.forEach((slide) => {
    total += slide.offsetWidth || 0
  })
  totalWidth.value = total

  const firstSlide = slides[0]
  if (firstSlide) {
    const slideWidth = firstSlide.offsetWidth
    if (slideWidth > 0) {
      const paddingLeft = Math.max(0, (wrapperWidth.value - slideWidth) / 2)
      trackRef.value.style.paddingLeft = paddingLeft + 'px'
    }
  }

  if (scrollX.value > maxScroll.value) {
    scrollX.value = Math.max(0, maxScroll.value)
  }
}

// ===== 窗口变化 =====
function handleResize() {
  calculateTotalWidth()
}

// ===== 键盘 =====
function handleKeydown(e) {
  if (e.key === 'Escape') closeDetail()
}

// ===== 生命周期 =====
onMounted(() => {
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', endDrag)
  window.addEventListener('resize', handleResize)
  window.addEventListener('keydown', handleKeydown)

  setTimeout(() => {
    calculateTotalWidth()
  }, 300)
})

onBeforeUnmount(() => {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* ===== 全屏画廊 ===== */
.fullscreen-view {
  position: fixed;
  inset: 0;
  background: #2E1F14;
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  cursor: grab;
}
.fullscreen-view.is-dragging {
  cursor: grabbing;
}

.gallery-wrapper {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
}

.gallery-track {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 0 0 0;
  will-change: transform;
  gap: 0;
}

.gallery-slide {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 0 10px;
  box-sizing: border-box;
}

.gallery-slide img {
  max-height: 85vh;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
  background: rgba(0, 0, 0, 0.1);
  user-select: none;
  -webkit-user-drag: none;
  pointer-events: none;
}

/* ===== 底部进度条 ===== */
.bottom-nav {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  width: 50%;
  max-width: 360px;
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
  z-index: 10;
}

.progress-bar {
  width: 100%;
  height: 1px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 1px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: rgba(255, 255, 255, 0.5);
  transition: width 0.1s ease-out;
}

/* ===== 关闭按钮 ===== */
.close-btn {
  position: fixed;
  top: 24px;
  right: 28px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  font-size: 18px;
  cursor: pointer;
  z-index: 20;
  transition: color 0.3s, transform 0.3s;
}
.close-btn:hover {
  color: rgba(255, 255, 255, 0.8);
  transform: rotate(90deg);
}

/* ===== 响应式 ===== */
@media (max-width: 820px) {
  .bottom-nav { width: 70%; bottom: 20px; }
  .close-btn { top: 16px; right: 18px; font-size: 16px; }
  .gallery-slide img { max-height: 75vh; }
  .gallery-slide { padding: 0 6px; }
}
@media (max-width: 480px) {
  .bottom-nav { width: 80%; bottom: 16px; }
  .close-btn { top: 12px; right: 14px; font-size: 14px; }
  .gallery-slide img { max-height: 65vh; }
  .gallery-slide { padding: 0 4px; }
}
</style>