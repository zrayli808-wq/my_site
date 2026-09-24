<template>
  <div
    class="fullscreen-view"
    @pointerdown="startDrag"
    @wheel.prevent="onWheel"
    :class="{ 'is-dragging': isDragging }"
  >
    <button class="close-btn" @click="closeDetail">
      {{ t('design.close') }}
    </button>

    <div class="gallery-wrapper" ref="wrapperRef">
      <div
        class="gallery-track"
        :style="trackStyle"
        ref="trackRef"
      >
        <div
          v-for="(img, idx) in visibleImages"
          :key="img"
          class="gallery-slide"
        >
          <img
            :src="img"
            :alt="'作品 ' + (idx + 1)"
            decoding="async"
            draggable="false"
            @load="onImageLoad"
            @error="onImageError(img)"
          />
        </div>
      </div>
    </div>

    <div class="bottom-nav">
      <div class="progress-bar">
        <div
          class="progress-fill"
          :style="{ width: progressPercent + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  computed,
  onMounted,
  onBeforeUnmount,
  nextTick,
  inject
} from 'vue'

import { useRouter } from 'vue-router'

// ===== 国际化 =====
const i18n = inject('i18n')
const { t } = i18n

const router = useRouter()

// ======================================================
// 图片数据
// public/designs/design1/P1.webp ~ P31.webp
// ======================================================

const images = Array.from(
  { length: 31 },
  (_, i) => `/designs/design1/P${i + 1}.webp`
)

// ======================================================
// 分批加载
// ======================================================

// 刚进入页面时，只创建前 6 张图片
const INITIAL_COUNT = 6

// 每次接近画廊末尾，再加载 5 张
const BATCH_SIZE = 5

const visibleCount = ref(
  Math.min(INITIAL_COUNT, images.length)
)

const visibleImages = computed(() => {
  return images.slice(0, visibleCount.value)
})

const hasMoreImages = computed(() => {
  return visibleCount.value < images.length
})

let loadingMore = false

async function loadMoreImages() {
  if (!hasMoreImages.value || loadingMore) return

  loadingMore = true

  visibleCount.value = Math.min(
    visibleCount.value + BATCH_SIZE,
    images.length
  )

  await nextTick()

  scheduleCalculateTotalWidth()

  // 防止连续滚动时一下子把 31 张全部创建出来
  setTimeout(() => {
    loadingMore = false
  }, 250)
}

// ======================================================
// 画廊状态
// ======================================================

const wrapperRef = ref(null)
const trackRef = ref(null)

const isDragging = ref(false)

const startX = ref(0)
const startScrollX = ref(0)

const scrollX = ref(0)

const wrapperWidth = ref(0)
const totalWidth = ref(0)

// ======================================================
// 最大滚动距离
// ======================================================

const maxScroll = computed(() => {
  return Math.max(
    0,
    totalWidth.value - wrapperWidth.value
  )
})

// ======================================================
// 底部进度
// ======================================================

const progressPercent = computed(() => {
  if (maxScroll.value === 0) return 0

  return Math.min(
    100,
    Math.max(
      0,
      (scrollX.value / maxScroll.value) * 100
    )
  )
})

// ======================================================
// 横向移动
// ======================================================

const trackStyle = computed(() => {
  return {
    transform: `translateX(-${scrollX.value}px)`,
    transition: 'none'
  }
})

// ======================================================
// 返回主页
// ======================================================

function closeDetail() {
  router.push('/?scroll=design')
}

// ======================================================
// 判断是否接近当前画廊末尾
// ======================================================

function maybeLoadMore(position = scrollX.value) {
  if (!hasMoreImages.value) return

  // 距离末尾还有大约一个屏幕时，
  // 就提前加载下一批
  const threshold = Math.max(
    300,
    wrapperWidth.value * 0.8
  )

  if (
    maxScroll.value === 0 ||
    maxScroll.value - position <= threshold
  ) {
    loadMoreImages()
  }
}

// ======================================================
// 鼠标拖拽
// ======================================================

function startDrag(e) {
  if (!e.isPrimary || e.button !== 0 || e.target.closest("button")) return
  e.currentTarget.setPointerCapture(e.pointerId)
  isDragging.value = true

  startX.value = e.clientX
  startScrollX.value = scrollX.value

  document.body.style.cursor = 'grabbing'
  document.body.style.userSelect = 'none'
}

function onDrag(e) {
  if (!isDragging.value) return

  const diff = startX.value - e.clientX

  let newScrollX =
    startScrollX.value + diff

  // 如果已经拖到当前内容尾部，
  // 提前加载下一批图片
  maybeLoadMore(newScrollX)

  newScrollX = Math.max(
    0,
    Math.min(newScrollX, maxScroll.value)
  )

  scrollX.value = newScrollX
}

function endDrag() {
  if (!isDragging.value) return

  isDragging.value = false

  document.body.style.cursor = ''
  document.body.style.userSelect = ''
}

// ======================================================
// 鼠标滚轮
// ======================================================

function onWheel(e) {
  const delta = e.deltaY || e.deltaX

  let newScrollX =
    scrollX.value + delta

  // 接近末尾时加载下一批
  maybeLoadMore(newScrollX)

  newScrollX = Math.max(
    0,
    Math.min(newScrollX, maxScroll.value)
  )

  scrollX.value = newScrollX
}

// ======================================================
// 图片加载
// ======================================================

let calculateFrame = null

function scheduleCalculateTotalWidth() {
  if (calculateFrame) {
    cancelAnimationFrame(calculateFrame)
  }

  calculateFrame = requestAnimationFrame(() => {
    calculateTotalWidth()
    calculateFrame = null
  })
}

function onImageLoad() {
  // 每加载完一张图片，
  // 更新一次实际画廊宽度
  scheduleCalculateTotalWidth()
}

function onImageError(img) {
  console.error(
    '[DesignView] 图片加载失败:',
    img
  )

  scheduleCalculateTotalWidth()
}

// ======================================================
// 计算画廊总宽度
// ======================================================

async function calculateTotalWidth() {
  await nextTick()

  if (!trackRef.value) return

  const slides =
    trackRef.value.querySelectorAll('.gallery-slide')

  if (slides.length === 0) return

  wrapperWidth.value =
    wrapperRef.value?.offsetWidth ||
    window.innerWidth

  let total = 0

  slides.forEach((slide) => {
    total += slide.offsetWidth || 0
  })

  // 第一张图片居中
  const firstSlide = slides[0]

  let paddingLeft = 0

  if (firstSlide) {
    const slideWidth =
      firstSlide.offsetWidth

    if (slideWidth > 0) {
      paddingLeft = Math.max(
        0,
        (wrapperWidth.value - slideWidth) / 2
      )

      trackRef.value.style.paddingLeft =
        paddingLeft + 'px'
    }
  }

  // 计算时把左侧居中的 padding 也算进去
  totalWidth.value =
    total + paddingLeft

  // 防止窗口尺寸变化后越界
  if (scrollX.value > maxScroll.value) {
    scrollX.value =
      Math.max(0, maxScroll.value)
  }
}

// ======================================================
// 窗口变化
// ======================================================

function handleResize() {
  scheduleCalculateTotalWidth()
}

// ======================================================
// 键盘
// ======================================================

function handleKeydown(e) {
  if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
    e.preventDefault()
    onWheel({ deltaX: (e.key === "ArrowRight" ? 1 : -1) * wrapperWidth.value * .85 })
  }
  if (e.key === 'Escape') {
    closeDetail()
  }
}

// ======================================================
// 生命周期
// ======================================================

onMounted(() => {
  document.addEventListener("pointercancel", endDrag)
  document.addEventListener(
    'pointermove',
    onDrag
  )

  document.addEventListener(
    'pointerup',
    endDrag
  )

  window.addEventListener(
    'resize',
    handleResize
  )

  window.addEventListener(
    'keydown',
    handleKeydown
  )

  // 第一批 DOM 创建完成后计算宽度
  nextTick(() => {
    scheduleCalculateTotalWidth()
  })
})

onBeforeUnmount(() => {
  endDrag()
  document.removeEventListener("pointercancel", endDrag)
  document.removeEventListener(
    'pointermove',
    onDrag
  )

  document.removeEventListener(
    'pointerup',
    endDrag
  )

  window.removeEventListener(
    'resize',
    handleResize
  )

  window.removeEventListener(
    'keydown',
    handleKeydown
  )

  if (calculateFrame) {
    cancelAnimationFrame(calculateFrame)
  }
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

/* ===== 画廊容器 ===== */

.gallery-wrapper {
  width: 100%;
  height: 100%;

  overflow: hidden;
  position: relative;

  display: flex;
  align-items: center;
}

/* ===== 横向轨道 ===== */

.gallery-track {
  display: flex;
  align-items: center;

  height: 100%;

  padding: 0;
  gap: 0;

  will-change: transform;
}

/* ===== 单张作品 ===== */

.gallery-slide {
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  height: 100%;

  padding: 0 10px;

  box-sizing: border-box;
}

/* ===== 图片 ===== */

.gallery-slide img {
  max-height: 85vh;

  width: auto;
  height: auto;

  object-fit: contain;

  border-radius: 4px;

  box-shadow:
    0 4px 24px rgba(0, 0, 0, 0.3);

  background:
    rgba(0, 0, 0, 0.1);

  user-select: none;

  -webkit-user-drag: none;

  pointer-events: none;
}

/* ===== 底部导航 ===== */

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

/* ===== 进度条 ===== */

.progress-bar {
  width: 100%;
  height: 1px;

  background:
    rgba(255, 255, 255, 0.2);

  border-radius: 1px;

  overflow: hidden;
}

.progress-fill {
  height: 100%;

  background:
    rgba(255, 255, 255, 0.5);

  transition:
    width 0.1s ease-out;
}

/* ===== 关闭按钮 ===== */

.close-btn {
  position: fixed;

  top: 24px;
  right: 28px;

  background: none;
  border: none;

  color:
    rgba(255, 255, 255, 0.4);

  font-size: 18px;

  cursor: pointer;

  z-index: 20;

  transition:
    color 0.3s,
    transform 0.3s;
}

.close-btn:hover {
  color:
    rgba(255, 255, 255, 0.8);

  transform: rotate(90deg);
}

/* ===== 平板 ===== */

@media (max-width: 820px) {

  .bottom-nav {
    width: 70%;
    bottom: 20px;
  }

  .close-btn {
    top: 16px;
    right: 18px;
    font-size: 16px;
  }

  .gallery-slide img {
    max-height: 75vh;
  }

  .gallery-slide {
    padding: 0 6px;
  }
}

/* ===== 手机 ===== */

@media (max-width: 480px) {

  .bottom-nav {
    width: 80%;
    bottom: 16px;
  }

  .close-btn {
    top: 12px;
    right: 14px;
    font-size: 14px;
  }

  .gallery-slide img {
    max-height: 65vh;
  }

  .gallery-slide {
    padding: 0 4px;
  }
}
</style>
