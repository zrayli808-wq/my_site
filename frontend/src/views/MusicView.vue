<template>
  <div class="page-wrapper">
    <div class="background-layer" :style="backgroundLayerStyle"></div>
    <div class="mask-layer"></div>

    <div class="shell">
      <div class="header">
        <router-link to="/?scroll=music" class="back-link">← 返回</router-link>
        <h2>音乐作品</h2>
      </div>

      <div class="timeline" v-if="!loading && !error && sortedAlbums.length > 0">
        <div
          v-for="(album, index) in sortedAlbums"
          :key="album.id"
          class="item"
          :class="{ 'item--active': activeIndex === index }"
          :ref="el => setCardRef(el, index)"
        >
          <div class="content">
            <div class="img-wrap">
              <router-link :to="getAlbumLink(album)" class="cover-link">
                <img
                  v-if="album.coverImage && album.coverImage !== ''"
                  :src="album.coverImage"
                  :alt="album.title"
                  @error="handleImageError"
                />
                <div v-else class="placeholder-cover">
                  <span>{{ album.title.charAt(0) }}</span>
                </div>
                <div class="play-overlay">
                  <span class="play-icon">▶</span>
                </div>
              </router-link>
            </div>
            <div class="text-block">
              <router-link :to="getAlbumLink(album)" class="title-link">
                <h2 class="content-title">{{ album.title }}</h2>
              </router-link>
              <p class="release-date">{{ formatDate(album.releaseDate) }}</p>
              <p v-if="album.description" class="description">{{ album.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="loading" class="status-message">加载中...</div>
      <div v-else-if="error" class="status-message error">{{ error }}</div>
      <div v-else-if="sortedAlbums.length === 0" class="status-message">暂无专辑</div>

      <div class="footer">
        <a href="#">&copy; 2026 · 音乐历程</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch, nextTick } from 'vue'

const albums = ref([])
const loading = ref(true)
const error = ref(null)
const activeIndex = ref(0)  // ★★★ 初始值改为 0，默认选中第一张 ★★★
const cardRefs = ref([])

// 过滤掉 Love&Loyalty pt2
const sortedAlbums = computed(() => {
  const filtered = albums.value.filter(album => album.title !== 'Love&Loyalty pt2')
  return [...filtered].sort((a, b) => new Date(a.releaseDate) - new Date(b.releaseDate))
})

const backgroundLayerStyle = computed(() => {
  const defaultBg = 'linear-gradient(135deg, #1a1a1a, #2d2d2d)'
  if (sortedAlbums.value.length === 0 || activeIndex.value < 0 || !sortedAlbums.value[activeIndex.value]) {
    return {
      background: defaultBg,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }
  }
  const album = sortedAlbums.value[activeIndex.value]
  if (album.coverImage && album.coverImage !== '') {
    return {
      backgroundImage: `url(${album.coverImage})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      transition: 'background-image 0.6s ease',
    }
  } else {
    const color = getColor(album.title)
    return {
      background: `linear-gradient(135deg, ${darkenColor(color, 0.8)}, ${color})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }
  }
})

function getAlbumLink(album) {
  if (album.title === '弱冠之年') {
    return '/album/4'
  }
  return `/album/${album.id}`
}

const fetchAlbums = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch('/data/albums.json')
    if (!response.ok) throw new Error('加载专辑数据失败')
    let data = await response.json()
    // 强制修正弱冠之年的封面路径（如果数据库字段与文件名不一致）
    data = data.map(album => {
      if (album.title === '弱冠之年') {
        album.coverImage = '/albums/album4.jpg'
      }
      return album
    })
    albums.value = data
    await nextTick()
    window.scrollTo({ top: 0, behavior: 'auto' })
    requestAnimationFrame(() => {
      activeIndex.value = 0
    })
  } catch (err) {
    error.value = '数据加载失败，请确保数据文件存在'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const setCardRef = (el, index) => {
  if (el) cardRefs.value[index] = el
}

// ★★★ 滚动检测：只在用户滚动时更新，不影响初始状态 ★★★
const handleScroll = () => {
  if (cardRefs.value.length === 0 || loading.value) return
  const windowHeight = window.innerHeight
  const scrollY = window.scrollY
  const viewportCenter = scrollY + windowHeight / 2
  let closestIndex = 0
  let closestDistance = Infinity
  cardRefs.value.forEach((card, index) => {
    if (!card) return
    const rect = card.getBoundingClientRect()
    const cardCenter = rect.top + rect.height / 2 + scrollY
    const distance = Math.abs(viewportCenter - cardCenter)
    if (distance < closestDistance) {
      closestDistance = distance
      closestIndex = index
    }
  })
  if (closestIndex !== activeIndex.value) {
    activeIndex.value = closestIndex
  }
}

const debounce = (fn, delay = 100) => {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}

const getColor = (title) => {
  const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FDCB6E']
  let hash = 0
  for (let i = 0; i < title.length; i++) {
    hash = title.charCodeAt(i) + ((hash << 5) - hash)
  }
  return colors[Math.abs(hash) % colors.length]
}

const darkenColor = (hex, factor) => {
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return `rgb(${Math.floor(r * factor)}, ${Math.floor(g * factor)}, ${Math.floor(b * factor)})`
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toISOString().split('T')[0]
}

const handleImageError = (e) => {
  e.target.style.display = 'none'
}

// ★★★ 在组件挂载时也滚动到顶部 ★★★
onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'auto' })
  fetchAlbums()
  const debouncedScroll = debounce(handleScroll, 100)
  window.addEventListener('scroll', debouncedScroll)
  onBeforeUnmount(() => {
    window.removeEventListener('scroll', debouncedScroll)
  })
})
</script>

<style scoped>
/* ===== 重置 ===== */
* { margin: 0; padding: 0; box-sizing: border-box; }
img { display: block; width: 100%; height: 100%; object-fit: cover; }

.page-wrapper {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow-x: hidden;
}
.background-layer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  background-color: #1a1a1a;
  background-size: cover !important;
  background-position: center !important;
  transition: background-image 0.6s ease;
}
.mask-layer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1;
  background: rgba(30, 30, 30, 0.78);
  pointer-events: none;
}
.shell {
  position: relative;
  z-index: 2;
  width: 100%;
  min-height: 100vh;
  padding: 164px 0 80px;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  color: #fff;
}

.header {
  text-align: center;
  margin-bottom: 50px;
}
.back-link {
  display: inline-block;
  color: rgba(255, 255, 255, 0.4);
  text-decoration: none;
  font-size: 14px;
  letter-spacing: 2px;
  margin-bottom: 16px;
  transition: color 0.3s;
}
.back-link:hover {
  color: #fff;
}
.header h2 {
  color: rgba(255, 255, 255, 0.5);
  font-size: 18px;
  font-weight: 400;
  letter-spacing: 8px;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.header p {
  color: rgba(255, 255, 255, 0.4);
  font-size: 14px;
  letter-spacing: 2px;
}

/* ===== 时间线 ===== */
.timeline {
  position: relative;
  max-width: 960px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
}
.timeline::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  width: 2px;
  height: 100%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.10);
  pointer-events: none;
}
.item {
  display: flex;
  align-items: stretch;
  width: 100%;
  padding: 40px 0;
  opacity: 0.3;
  filter: blur(2px);
  transform: translateY(-60px);
  transition: opacity 0.7s ease, transform 0.7s ease, filter 0.7s ease;
  position: relative;
}
.item--active {
  opacity: 1;
  transform: translateY(0);
  filter: blur(0);
}
.item:nth-child(odd) .content { flex-direction: row; }
.item:nth-child(odd) .text-block { order: 1; padding-right: 30px; text-align: right; align-items: flex-end; }
.item:nth-child(odd) .img-wrap { order: 2; }
.item:nth-child(even) .content { flex-direction: row; }
.item:nth-child(even) .text-block { order: 2; padding-left: 30px; text-align: left; align-items: flex-start; }
.item:nth-child(even) .img-wrap { order: 1; }

.content { display: flex; width: 100%; gap: 0; align-items: flex-start; }
.img-wrap {
  flex: 0 0 55%;
  max-width: 55%;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
  transition: transform 0.4s ease;
}
.item--active .img-wrap { transform: scale(1); }
.img-wrap:hover .play-overlay { opacity: 1; }
.img-wrap img { aspect-ratio: 1 / 1; object-fit: cover; }
.placeholder-cover {
  aspect-ratio: 1 / 1;
  background: linear-gradient(135deg, #2d2d44, #1a1a2e);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.2);
}
.cover-link { display: block; width: 100%; height: 100%; text-decoration: none; position: relative; }
.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 12px;
  pointer-events: none;
}
.play-icon {
  font-size: 48px;
  color: #fff;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  transform: scale(1);
  transition: transform 0.2s;
}
.img-wrap:hover .play-icon { transform: scale(1.1); }

.text-block {
  flex: 0 0 45%;
  max-width: 45%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 0 0 10px 0;
  overflow: visible;
}
.title-link { text-decoration: none; color: inherit; display: inline-block; }
.title-link:hover .content-title { color: #f7971e; }
.content-title {
  font-weight: 700;
  font-size: 40px;
  line-height: 1.2;
  letter-spacing: 1px;
  margin: 0 0 6px 0;
  word-break: break-word;
  color: #fff;
  transition: color 0.2s;
}
.release-date {
  font-size: 18px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.55);
  letter-spacing: 1.5px;
  margin: 0;
  line-height: 1.4;
}
.item--active .release-date { color: rgba(255, 255, 255, 0.7); }
.description {
  font-size: 16px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 10px;
  max-width: 90%;
  word-break: break-word;
}
.item:nth-child(odd) .description { text-align: right; align-self: flex-end; }
.item:nth-child(even) .description { text-align: left; align-self: flex-start; }

.status-message {
  text-align: center;
  padding: 60px 20px;
  font-size: 18px;
  color: rgba(255, 255, 255, 0.6);
}
.status-message.error { color: #ff6b6b; }

.footer {
  padding: 60px 0 30px;
  text-align: center;
}
.footer a {
  color: rgba(255, 255, 255, 0.3);
  text-decoration: none;
  font-size: 13px;
  letter-spacing: 2px;
  transition: color 0.3s;
}
.footer a:hover { color: rgba(255, 255, 255, 0.7); }

@media only screen and (max-width: 820px) {
  .shell { padding-top: 120px; }
  .timeline { max-width: 100%; padding: 0 16px; }
  .timeline::before { left: 24px; transform: none; }
  .item { padding: 30px 0 30px 50px; width: 100%; opacity: 0.6; filter: blur(0); transform: none; }
  .item--active { opacity: 1; }
  .content { flex-direction: column !important; gap: 16px; align-items: stretch !important; }
  .img-wrap { flex: 0 0 auto; max-width: 100%; width: 100%; order: 1 !important; }
  .img-wrap img, .placeholder-cover { aspect-ratio: 4 / 3; height: auto; }
  .text-block { flex: 0 0 auto; max-width: 100%; width: 100%; order: 2 !important; padding: 0 !important; text-align: left !important; align-items: flex-start !important; }
  .content-title { font-size: 30px; text-align: left !important; }
  .release-date { font-size: 16px; text-align: left !important; }
  .description { text-align: left !important; align-self: flex-start !important; max-width: 100%; }
  .play-icon { font-size: 36px; }
  .title-link:hover .content-title { color: #fff; }
}
@media only screen and (max-width: 480px) {
  .shell { padding: 100px 0 40px; }
  .header { margin-bottom: 30px; }
  .item { padding: 20px 0 20px 40px; }
  .content-title { font-size: 26px; }
  .release-date { font-size: 14px; }
  .img-wrap { border-radius: 8px; }
  .play-icon { font-size: 28px; }
}
</style>