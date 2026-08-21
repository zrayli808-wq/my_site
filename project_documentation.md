# my_site 项目文档

*生成时间: 2026-08-21 16:32:49*

## 目录结构

```
my_site/
├── app.py
├── frontend
│   ├── .gitignore
│   ├── .vscode
│   │   └── extensions.json
│   ├── README.md
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   │   ├── albums
│   │   │   ├── album1.jpg
│   │   │   ├── album2.jpg
│   │   │   ├── album3.jpg
│   │   │   └── album4.jpg
│   │   ├── data
│   │   │   ├── albums.json
│   │   │   └── songs.json
│   │   ├── designs
│   │   │   └── design1
│   │   │       ├── Cover1.png
│   │   │       ├── P10.png
│   │   │       ├── P11.png
│   │   │       ├── P12.png
│   │   │       ├── P13.png
│   │   │       ├── P14.png
│   │   │       ├── P15.png
│   │   │       ├── P16.png
│   │   │       ├── P17.png
│   │   │       ├── P18.png
│   │   │       ├── P19.png
│   │   │       ├── P2.png
│   │   │       ├── P20.png
│   │   │       ├── P21.png
│   │   │       ├── P22.png
│   │   │       ├── P23.png
│   │   │       ├── P24.png
│   │   │       ├── P25.png
│   │   │       ├── P26.png
│   │   │       ├── P3.png
│   │   │       ├── P4.png
│   │   │       ├── P5.png
│   │   │       ├── P6.png
│   │   │       ├── P7.png
│   │   │       ├── P8.png
│   │   │       └── P9.png
│   │   ├── logo.png
│   │   ├── showpics
│   │   │   ├── bk1.jpg
│   │   │   ├── bk2-1.png
│   │   │   ├── bk2.jpg
│   │   │   ├── bk3-1.png
│   │   │   ├── bk3.jpg
│   │   │   └── bk4-1.png
│   │   └── songs
│   │       ├── album1
│   │       │   ├── a1s1.mp3
│   │       │   ├── a1s2.mp3
│   │       │   ├── a1s3.mp3
│   │       │   ├── a1s4.mp3
│   │       │   ├── a1s5.mp3
│   │       │   └── a1s6.mp3
│   │       ├── album2
│   │       ├── album3
│   │       ├── album4
│   │       └── album5
│   ├── src
│   │   ├── App.vue
│   │   ├── assets
│   │   │   ├── hero.png
│   │   │   ├── vite.svg
│   │   │   └── vue.svg
│   │   ├── components
│   │   │   ├── RainEffect.vue
│   │   │   └── layout
│   │   │       ├── NavBar.vue
│   │   │       ├── PlayerBar.vue
│   │   │       └── PlaylistSidebar.vue
│   │   ├── composables
│   │   │   └── useI18n.js
│   │   ├── locales
│   │   │   ├── en.js
│   │   │   └── zh.js
│   │   ├── main.js
│   │   ├── router
│   │   │   └── index.js
│   │   ├── stores
│   │   │   ├── player.js
│   │   │   └── ui.js
│   │   ├── style.css
│   │   ├── styles
│   │   │   ├── components
│   │   │   │   ├── album-detail.css
│   │   │   │   ├── player.css
│   │   │   │   └── playlist.css
│   │   │   ├── globals.css
│   │   │   ├── reset.css
│   │   │   ├── variables.css
│   │   │   └── views
│   │   │       ├── music.css
│   │   │       └── work.css
│   │   └── views
│   │       ├── AboutView.vue
│   │       ├── AlbumDetailView.vue
│   │       ├── ArtistView.vue
│   │       ├── DesignView.vue
│   │       ├── HomeView.vue
│   │       └── MusicView.vue
│   └── vite.config.js
├── package-lock.json
├── package.json
├── project_documentation.md
└── tempCodeRunnerFile.py
```

## 源代码

### Vue组件文件

#### frontend\src\App.vue

```vue
<script setup>
import NavBar from './components/layout/NavBar.vue'
import PlayerBar from './components/layout/PlayerBar.vue'
import PlaylistSidebar from './components/layout/PlaylistSidebar.vue'
</script>

<template>
  <NavBar />
  <router-view />
  <PlayerBar />
  <PlaylistSidebar />
</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
  background: #1a1a1a;
}
#app {
  width: 100%;
  min-height: 100vh;
  padding-bottom: 80px;
}
</style>
```

#### frontend\src\components\RainEffect.vue

```vue
<template>
  <div id="wrap-texture" ref="containerRef">
    <div id="canvas" ref="canvasRef"></div>
    <div class="plane" ref="planeRef">
      <img 
        data-sampler="dispImage" 
        id="texture" 
        :src="bgImage" 
        crossorigin="anonymous"
        alt="background"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { Curtains, Plane } from 'curtainsjs'

const props = defineProps({
  bgImage: {
    type: String,
    default: '/albums/default.jpg'
  },
  widthSegments: {
    type: Number,
    default: 40
  },
  heightSegments: {
    type: Number,
    default: 40
  }
})

const containerRef = ref(null)
const canvasRef = ref(null)
const planeRef = ref(null)

let curtains = null
let plane = null
let animationId = null
const mouse = { x: 0, y: 0 }

const shader = {
  vertex: `
    #ifdef GL_ES
    precision mediump float;
    #endif
    
    attribute vec3 aVertexPosition;
    attribute vec2 aTextureCoord;
    
    uniform mat4 uMVMatrix;
    uniform mat4 uPMatrix;
    uniform mat4 dispImageMatrix;
    
    varying vec3 vVertexPosition;
    varying vec2 vTextureCoord;
    
    void main() {
      vec3 vertexPosition = aVertexPosition;
      gl_Position = uPMatrix * uMVMatrix * vec4(vertexPosition, 1.0);
      
      vTextureCoord = (dispImageMatrix * vec4(aTextureCoord, 0., 1.)).xy;
      vVertexPosition = vertexPosition;
    }
  `,
  
  fragment: `
    #ifdef GL_ES
    precision mediump float;
    #endif
    
    #define PI2 6.28318530718
    #define PI 3.14159265359
    #define S(a,b,n) smoothstep(a,b,n)
    
    varying vec3 vVertexPosition;
    varying vec2 vTextureCoord;
    
    uniform float uTime;
    uniform vec2 uReso;
    uniform vec2 uMouse;
    
    uniform sampler2D dispImage;
    uniform sampler2D blurImage;
    
    float N12(vec2 p){
      p = fract(p * vec2(123.34, 345.45));
      p += dot(p, p + 34.345);
      return fract(p.x * p.y);
    }
    
    vec3 Layer(vec2 uv0, float t){
      vec2 asp = vec2(2., 1.);
      vec2 uv1 = uv0 * 3. * asp;
      uv1.y += t * .25;
      
      vec2 gv = fract(uv1) - .5;
      vec2 id = floor(uv1);
      
      float n = N12(id);
      t += n * PI2;
      
      float w = uv0.y * 10.;
      float x = (n - .5) * .8;
      x += (.4 - abs(x)) * sin(3. * w) * pow(sin(w), 6.) * .45;
      float y = -sin(t + sin(t + sin(t) * .5)) * (.5 - .06);
      y -= (gv.x - x) * (gv.x - x);
      
      vec2 dropPos = (gv - vec2(x, y)) / asp;
      float drop = S(.03, .02, length(dropPos));
      
      vec2 trailPos = (gv - vec2(x, t * .25)) / asp;
      trailPos.y = (fract(trailPos.y * 8.) - .5) / 8.;
      float trail = S(.02, .015, length(trailPos));
      
      float fogTrail = S(-.05, .05, dropPos.y);
      fogTrail *= S(.5, y, gv.y);
      trail *= fogTrail;
      fogTrail *= S(.03, .015, abs(dropPos.x));
      
      vec2 off = drop * dropPos + trail * trailPos;
      return vec3(off, fogTrail);
    }
    
    void main() {
      float dist = 5.;
      float blurSize = 5.;
      float t = mod(uTime * .03, 7200.);
      
      vec4 c = vec4(0);
      vec2 uv = vTextureCoord;
      
      vec3 drops = Layer(uv, t);
      drops += Layer(uv * 1.25 + 7.54, t);
      drops += Layer(uv * 1.35 + 1.54, t);
      drops += Layer(uv * 1.57 - 7.54, t);
      
      float blur = blurSize * 7. * (1. - drops.z);
      
      vec4 col = vec4(0.);
      int numSamples = 32;
      float a = N12(uv) * PI2;
      
      blur *= .0005;
      uv += drops.xy * dist;
      
      for(int n = 0; n < 32; n++){
        vec2 off = vec2(sin(a), cos(a)) * blur;
        float d = fract(sin((float(n) + 1.) * 546.) * 5424.);
        d = sqrt(d);
        off *= d;
        col += texture2D(dispImage, uv + off);
        a++;
      }
      
      col /= float(numSamples);
      gl_FragColor = col;
    }
  `
}

const initWebGL = () => {
  if (!canvasRef.value || !planeRef.value) {
    console.error('Canvas或Plane元素未找到')
    return
  }
  
  try {
    curtains = new Curtains({
      container: canvasRef.value,
      pixelRatio: Math.min(window.devicePixelRatio, 2)
    })
    
    curtains.onRender(() => {})
    
    const params = {
      vertexShader: shader.vertex,
      fragmentShader: shader.fragment,
      widthSegments: props.widthSegments,
      heightSegments: props.heightSegments,
      uniforms: {
        time: {
          name: "uTime",
          type: "1f",
          value: 0
        },
        mousepos: {
          name: "uMouse",
          type: "2f",
          value: [mouse.x, mouse.y]
        },
        resolution: {
          name: "uReso",
          type: "2f",
          value: [window.innerWidth, window.innerHeight]
        }
      }
    }
    
    plane = new Plane(curtains, planeRef.value, params)
    
    if (!plane) {
      console.error('无法创建平面')
      return
    }
    
    const animate = () => {
      if (plane && plane.uniforms) {
        plane.uniforms.time.value++
        plane.uniforms.resolution.value = [
          window.innerWidth,
          window.innerHeight
        ]
      }
      animationId = requestAnimationFrame(animate)
    }
    animate()
    
    console.log('雨特效初始化成功！')
    
  } catch (error) {
    console.error('初始化失败:', error)
  }
}

// 更新背景图片
const updateTexture = (newImageUrl) => {
  if (!newImageUrl) return
  const img = document.getElementById('texture')
  if (img) {
    img.src = newImageUrl
  }
}

// 暴露方法给父组件
defineExpose({
  updateTexture
})

const handleMouseMove = (event) => {
  mouse.x = event.clientX
  mouse.y = event.clientY
  if (plane && plane.uniforms) {
    plane.uniforms.mousepos.value = [mouse.x, mouse.y]
  }
}

const handleResize = () => {
  if (plane && plane.uniforms) {
    plane.uniforms.resolution.value = [
      window.innerWidth,
      window.innerHeight
    ]
  }
}

// 监听 bgImage 变化
watch(() => props.bgImage, (newVal) => {
  if (newVal) {
    updateTexture(newVal)
  }
})

onMounted(() => {
  initWebGL()
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('resize', handleResize)
  
  if (animationId) {
    cancelAnimationFrame(animationId)
    animationId = null
  }
  
  if (plane) {
    plane.dispose && plane.dispose()
    plane = null
  }
  
  if (curtains) {
    curtains.dispose && curtains.dispose()
    curtains = null
  }
})
</script>

<style scoped>
/* ===== 雨特效固定背景层 ===== */
#wrap-texture {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
}

#canvas {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1;
}

.plane {
  width: 100%;
  height: 100vh;
  position: relative;
  z-index: 0;
}

.plane img {
  display: none;
}
</style>
```

#### frontend\src\components\layout\NavBar.vue

```vue
<template>
  <header class="navbar">
    <router-link to="/" class="brand">
      <img src="/logo.png" alt="ZRay" class="brand-logo" />
    </router-link>
    <nav class="nav-links">
      <router-link to="/?scroll=design">{{ t('nav.design') }}</router-link>
      <router-link to="/?scroll=music">{{ t('nav.music') }}</router-link>
      <router-link to="/about">{{ t('nav.about') }}</router-link>
    </nav>
    <div class="language-selector">
      <select v-model="lang" @change="onLangChange">
        <option value="zh">中文</option>
        <option value="en">English</option>
      </select>
    </div>
  </header>
</template>

<script setup>
import { ref, inject } from 'vue'

// ★★★ 注入国际化 ★★★
const i18n = inject('i18n')
const { t, setLang, currentLang } = i18n

// 语言选择器绑定
const lang = ref(currentLang.value)

function onLangChange() {
  setLang(lang.value)
  // 刷新页面以更新所有组件的翻译
  window.location.reload()
}
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
```

#### frontend\src\components\layout\PlayerBar.vue

```vue
<template>
  <div class="player-bar" v-if="player.currentSong">
    <audio
      ref="audioRef"
      :src="player.currentSong.fileUrl"
      type="audio/mpeg"
      preload="metadata"
      @loadedmetadata="onLoaded"
      @timeupdate="onTimeUpdate"
      @ended="onEnded"
      @error="onError"
    ></audio>

    <div class="player-left">
      <img
        v-if="player.currentAlbum?.coverImage"
        :src="player.currentAlbum.coverImage"
        alt="cover"
        class="cover-mini"
      />
      <div class="song-info">
        <div class="title">{{ player.currentSong?.title || '未命名' }}</div>
        <div class="artist">{{ player.currentAlbum?.title || '未知专辑' }}</div>
      </div>
    </div>

    <div class="player-center">
      <button class="ctrl-btn" @click="player.prev" aria-label="上一首">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
          <path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/>
        </svg>
      </button>
      <button class="ctrl-btn play-btn" @click="togglePlay" aria-label="播放/暂停">
        <svg v-if="!player.isPlaying" viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
          <path d="M8 5v14l11-7z"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
          <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
        </svg>
      </button>
      <button class="ctrl-btn" @click="player.next" aria-label="下一首">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
          <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/>
        </svg>
      </button>
      <span class="time">{{ formatTime(player.currentTime) }}</span>
      <input
        type="range"
        class="progress-bar"
        min="0"
        :max="player.duration || 0"
        step="0.1"
        v-model="progressModel"
        @input="onSeek"
      />
      <span class="time">{{ formatTime(player.duration) }}</span>
    </div>

    <div class="player-right">
      <button class="playlist-btn" @click="player.togglePlaylist()" aria-label="播放列表">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
          <path d="M3 6h18v2H3V6zm0 5h18v2H3v-2zm0 5h18v2H3v-2z"/>
        </svg>
      </button>
      <input
        type="range"
        class="volume-bar"
        min="0"
        max="1"
        step="0.01"
        v-model="volumeModel"
        @input="onVolumeChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onBeforeUnmount } from 'vue'
import { usePlayerStore } from '../../stores/player'

const player = usePlayerStore()
const audioRef = ref(null)

const progressModel = computed({
  get: () => player.currentTime,
  set: (val) => player.setProgress(parseFloat(val))
})

const volumeModel = computed({
  get: () => player.volume,
  set: (val) => {
    player.volume = parseFloat(val)
    if (audioRef.value) audioRef.value.volume = player.volume
  }
})

function togglePlay() {
  player.togglePlay()
}

function onLoaded() {
  if (audioRef.value) {
    player.duration = audioRef.value.duration
    if (player.isPlaying) {
      audioRef.value.play().catch(err => console.error('自动播放失败:', err))
    }
  }
}

function onTimeUpdate() {
  if (audioRef.value) {
    player.currentTime = audioRef.value.currentTime
  }
}

function onSeek() {
  if (audioRef.value) {
    audioRef.value.currentTime = player.currentTime
  }
}

function onVolumeChange() {
  if (audioRef.value) {
    audioRef.value.volume = player.volume
  }
}

function onEnded() {
  player.next()
}

function onError(e) {
  console.error('[PlayerBar] 音频加载错误:', e.target.error)
  if (audioRef.value) {
    audioRef.value.load()
  }
}

// 监听当前歌曲变化，重置进度
watch(() => player.currentSong, (newSong) => {
  if (newSong) {
    player.currentTime = 0
  }
}, { immediate: true })

// 监听播放状态，控制播放/暂停
watch(() => player.isPlaying, (val) => {
  if (audioRef.value && player.currentSong) {
    if (val) {
      audioRef.value.play().catch(err => console.error('播放失败:', err))
    } else {
      audioRef.value.pause()
    }
  }
})

function formatTime(sec) {
  if (!sec || isNaN(sec)) return '0:00'
  const m = Math.floor(sec / 60)
  const s = Math.floor(sec % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}
</script>
```

#### frontend\src\components\layout\PlaylistSidebar.vue

```vue
<template>
  <div class="playlist-sidebar" v-if="player.playlistVisible">
    <div class="playlist-overlay" @click="player.togglePlaylist()"></div>
    <div class="playlist-panel">
      <div class="playlist-header">
        <h3>播放列表</h3>
        <button class="clear-btn" @click="clearPlaylist">清空</button>
      </div>
      <div class="playlist-body">
        <div
          v-for="(song, index) in player.queue"
          :key="song.id + index"
          class="playlist-item"
          :class="{ active: index === player.currentIndex }"
          @click="playSongFromQueue(index)"
        >
          <span class="song-title">{{ song.title }}</span>
          <span class="song-artist">{{ song.album?.title || '未知专辑' }}</span>
          <button class="remove-btn" @click.stop="removeFromQueue(index)">×</button>
        </div>
        <div v-if="player.queue.length === 0" class="empty-tip">播放列表为空</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { usePlayerStore } from '../../stores/player'

const player = usePlayerStore()

function clearPlaylist() {
  player.clearQueue()
}

function removeFromQueue(index) {
  player.removeSong(index)
}

function playSongFromQueue(index) {
  player.currentIndex = index
  player.isPlaying = true
}
</script>
```

#### frontend\src\views\AboutView.vue

```vue
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
```

#### frontend\src\views\AlbumDetailView.vue

```vue
<template>
  <div class="page-wrapper">
    <!-- ===== 冬念春：雨特效背景 ===== -->
    <RainEffect 
      v-if="album?.id === 2"
      ref="rainEffectRef"
      :bg-image="album?.coverImage || '/albums/default.jpg'" 
    />

    <!-- ===== 其他专辑：普通背景 ===== -->
    <div 
      v-if="album?.id !== 2 && album?.coverImage"
      class="bg-fallback"
      :style="{ backgroundImage: `url(${album.coverImage})` }"
    ></div>
    <div 
      v-if="album?.id !== 2 && !album?.coverImage"
      class="bg-fallback"
      :style="{ background: 'linear-gradient(135deg, #1a1a1a, #2d2d2d)' }"
    ></div>

    <!-- ===== 遮罩层（仅冬念春） ===== -->
    <div v-if="album?.id === 2" class="mask-layer"></div>

    <!-- ===== 内容 ===== -->
    <div class="detail-container">
      <div class="album-header">
        <div class="album-cover-wrapper">
          <img
            v-if="album?.coverImage"
            :src="album.coverImage"
            alt="cover"
            class="album-cover"
          />
          <div v-else class="placeholder-cover">{{ album?.title?.charAt(0) }}</div>
        </div>
        <div class="album-title-wrapper">
          <div class="title-group">
            <h1 class="album-title">{{ album?.title || '加载中...' }}</h1>
            <div class="album-meta">
              <span class="meta-item">{{ album?.artist || '未知艺术家' }}</span>
              <span class="meta-divider">·</span>
              <span class="meta-item">{{ album?.releaseDate ? formatDate(album.releaseDate) : '未知日期' }}</span>
            </div>
          </div>
          <button class="back-btn" @click="$router.back()">← 返回</button>
        </div>
      </div>

      <div class="tab-bar">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'songs' }"
          @click="activeTab = 'songs'"
        >
          歌曲
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'detail' }"
          @click="activeTab = 'detail'"
        >
          专辑详情
        </button>
      </div>

      <div class="tab-content">
        <div v-if="activeTab === 'songs'" class="song-list">
          <div v-if="loading" class="status">加载歌曲中...</div>
          <div v-else-if="error" class="status error">{{ error }}</div>
          <div v-else-if="songs.length === 0" class="empty-tip">暂无歌曲，请先添加数据</div>
          <div
            v-else
            v-for="(song, index) in songs"
            :key="song.id"
            class="song-item"
          >
            <span class="track-number">{{ index + 1 }}</span>
            <span class="song-title">{{ song.title }}</span>
            <span class="song-duration">{{ song.duration || '--:--' }}</span>
            <button class="play-btn-small" @click.stop="playSong(song)">▶</button>
            <button class="play-next-btn" @click.stop="playNext(song)">下一首播放</button>
          </div>
        </div>

        <div v-else-if="activeTab === 'detail'" class="album-detail">
          <div v-if="loading" class="status">加载中...</div>
          <div v-else-if="error" class="status error">{{ error }}</div>
          <div v-else-if="album">
            <div class="detail-header">
              <span class="detail-title">专辑简介</span>
            </div>
            <div class="detail-content">
              <!-- 专辑1：Love&Loyalty part.1 -->
              <template v-if="album.id === 1">
                <p class="intro-quote">惟愿爱与忠诚可以遍布大地</p>
                <p class="intro-quote">以情感温暖世界</p>
                <p class="intro-text">
                  这是zray在十七岁时制作的专辑，里面包含了zray在制作说唱音乐的三年中最具有代表性的几首歌曲，全专将会以两个部分进行发布并合为一张完整版专辑，每首歌中都包含着zray对这世界的思考，将自己的看法和情绪与音乐相结合，希望可以让更多人听到，更多人理解，更多人去思考我们所生活的世界与我们本身。
                </p>
                <p class="intro-text">感谢我的制作人 雁潮工作室的萧老师对我的指导与优质的混音录音技术支持</p>
                <p class="intro-text">感谢全专中如LV9.moonvibe等音乐制作人的编曲支持</p>
                <p class="intro-text">还有家人朋友们对我一如既往的支持，让我能在音乐的道路上不断坚持探寻</p>
                <p class="intro-text">是有了你们才让我完成了我即将到来的十八岁最美好的时刻。</p>
              </template>

              <!-- 专辑2：冬念春 -->
              <template v-else-if="album.id === 2">
                <p class="intro-text">
                  我想一个时期的结束从来都不是悄悄地从我的身边离开，很多时候它会带走很多旧东西，也会带来很多新东西。有些我们希望它能带走的，却偏偏被它留了下来，有些我们所一直抓紧的，不愿松手的，却总在恍惚之间烟消云散......
                </p>
                <p class="intro-text">
                  合辑中的花鸟虫鱼水，每一物到如今存在又不存在，我不会说这五首是最后写给那个时期的五首，但我相信时间总在流淌，再刻骨铭心的记忆也会随之飘散化为歌曲后的delay，所以谨以《冬念春》献给那时的人，希望我能诠释好那些故事。
                </p>
                <p class="intro-text">
                  特此致谢雁潮音乐工作室蹇常文老师对于我音乐制作的指导，歌曲后期方面仍需加油努力。感谢EVO MUSIC能够提供如此优质且免费的伴奏供大家使用，同时也感谢参与EP的每一位编曲人，希望在今后大家也继续一起努力！新的一年向更远大的目标迈去！
                </p>
                <p class="intro-text" style="text-align: right; color: rgba(255,255,255,0.5); margin-top: 8px;">—— ZRay</p>
              </template>

              <!-- 专辑3：夏望秋 -->
              <template v-else-if="album.id === 3">
                <p class="intro-text">
                  转眼间我们便走进了后疫情时代，疫情的结束也代表着我们终于摆脱了隔离的拘束，可以自由地在城市间穿行，去完成很多在隔离期间计划要完成的事，疫情的结束让我们更加珍惜世界的美好，珍惜时光的珍贵。
                </p>
                <p class="intro-text">
                  如果说《冬念春》是对曾经的回忆与反思，那么《夏望秋》则是对当下与未来的一次总结与计划；在《夏望秋》企划创作期间，ZRay也在生活上开始了许多新的尝试，在一个不熟悉的地方开启了一次全新的探索，关乎大我也关乎于小我，也仍在寻找与发现这世间的规律与真理，同时ZRay也结交了许多来自全国各地优秀的朋友，他们给予了ZRay对于音乐创作更多的灵感与更大的热忱，让ZRay不仅在新EP中有了更多曲风的尝试，而且在基于生活经历的实践上，对于歌词的叙写也有了新的理解，努力向听众们以更多方面的表现自己，推动自我走向下一个高度。
                </p>
                <p class="intro-text" style="font-weight: 500; color: rgba(255,255,255,0.8); margin-top: 8px;">新EP分为两个部分——“夏”与“秋”：</p>
                <p class="intro-text" style="padding-left: 20px;">
                  《不想再遇见你》与《夏的歌》是ZRay首次使用Punk曲风进行创作，着重在对于“夏”这部分的氛围进行烘托，渲染出夏日热烈的气氛。
                </p>
                <p class="intro-text" style="padding-left: 20px;">
                  在《TAKE OFF》与《19》两首歌中，ZRay用轻快的曲调阐述了自己的志向与梦想，直白坦率地面对自己的欲望，并且为之奋斗。
                </p>
                <p class="intro-text" style="padding-left: 20px;">
                  《SOFIA》是ZRay自己非常喜欢的一首歌，尽管在一年前释出时混音效果与录制效果差强人意，但它仍旧以朗朗上口的歌词与简单的旋律获得了不错的市场反响。
                </p>
                <p class="intro-text" style="font-weight: 500; color: rgba(255,255,255,0.8); margin-top: 8px;">EP的下半部分——“秋”：</p>
                <p class="intro-text" style="padding-left: 20px;">
                  以一首已发布的《玫瑰》作为开始曲目，用具有凋零特色的乐器，为EP的后半部分烘托出了“秋”的萧瑟与凋零。
                </p>
                <p class="intro-text" style="padding-left: 20px;">
                  《路Freestyle》以boombap伴奏进行了对于“秋”章节的续写，表达了ZRay在创作期间所遭遇到的迷茫与困惑。
                </p>
                <p class="intro-text" style="padding-left: 20px;">
                  EP以《失眠症（insomnia dealer）》结束，这是一首为“失眠商店”写的主题曲，尽管如今已经关店，但仍旧感谢失眠商店的全体兄弟们，也是希望做出一个好的作品为它画上个句号吧。
                </p>
                <p class="intro-text">
                  感谢所有EP中歌曲的编曲人，感谢你们产出高质量的伴奏供大家创作出更优秀的作品。<br>
                  感谢衡阳雁潮音乐工作室的蹇常文老师对此张EP的混音技术支持。<br>
                  特别鸣谢“兰州失眠商店”的全体成员、WC PARK、Four One Seven、Second Heart（第二颗心脏）等兄弟们的支持（0734&0931） 兰州见！
                </p>
                <p class="intro-text" style="text-align: right; color: rgba(255,255,255,0.5); margin-top: 8px;">最后祝 ZRay 19岁生日快乐！继续努力吧</p>
              </template>

              <!-- 专辑5：弱冠之年 -->
              <template v-else-if="album.id === 5">
                <p class="intro-quote">“二十岁究竟意味着什么？”</p>
                <p class="intro-text">
                  自十六岁起，我在每一个生日都会为自己写一首歌。它既是对过去一年的总结，也是对新一年的期许。五年来，这个最初只是灵光一闪的想法，逐渐变成了生日里和蛋糕一样不可或缺的仪式。
                </p>
                <p class="intro-text">
                  直到二零二四年，我恍惚间发现自己已经二十岁了。在我过往的认知中，二十岁应该是独立的象征，是一个人开始真正奔赴理想、追逐天空的起点。而反观当前的我，却仍觉得自己并没有完全准备好去迎接“它”的到来。对我而言，这个“它”或许是一种责任，一种焦虑，也可能是我对未来的期待。
                </p>
                <p class="intro-text">
                  我也在思考：成长，到底意味着什么？是承担更多的责任，还是学会与不确定共处？是奋力追逐远方，还是学会安放当下？在二十岁的门槛上，我无法给出明确的答案，但很庆幸音乐给了我一种方式，让我可以把这些困惑、这些情绪都记录下来。
                </p>
                <p class="intro-text">
                  既然如此，与其在事后回望总结，不如把未来的一年本身，作为《弱冠之年》这张专辑的灵感源泉，将未来一年中自己认知的改变，自身的思考与情绪的波动都用歌词记录下来，用旋律表达出来。
                </p>
                <p class="intro-text">
                  而让我欣慰的是，这张专辑最终确实如我所愿，完整地记录下了我在面对未知时的焦虑与转变，也让我得以理解并实践出一种属于自己的乐观主义精神。回顾此前的《冬念春》《夏望秋》《爱与诚》，它们或多或少带着些许犹疑与挣扎；而这一次，《弱冠之年》会少一些踟蹰，多一些能量、喜悦与希望。我希望这些声音中的信息可以传递给我的每一位听众。
                </p>
                <p class="intro-text">
                  这是我耗时两年多近三年的第一张长专辑，也很有可能是我的最后一张，我想未来我也不一定还会有这么多时间和精力去投入在这件事上了，确实很累……
                </p>
                <p class="intro-text" style="font-weight: 500; color: rgba(255,255,255,0.7);">但谁知道呢？</p>
                <p class="intro-text">
                  感谢参与这张专辑的每一位编曲人，有了你们优秀的编曲才给予了我每一首歌曲得以栖息的空间。<br>
                  专辑仍多有瑕疵，对此深表歉意。
                </p>
                <p class="intro-text" style="text-align: right; color: rgba(255,255,255,0.5); margin-top: 8px;">二零二五年 九月<br>ZRay子睿</p>
              </template>

              <!-- 其他专辑 -->
              <template v-else>
                <p class="intro-text">{{ album.description || '暂无简介' }}</p>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePlayerStore } from '../stores/player'
import RainEffect from '../components/RainEffect.vue'

const route = useRoute()
const router = useRouter()
const albumId = route.params.id

const album = ref(null)
const songs = ref([])
const loading = ref(true)
const error = ref(null)
const activeTab = ref('songs')
const playerStore = usePlayerStore()
const rainEffectRef = ref(null)

// ---------- 组件逻辑 ----------
const fetchAlbumDetail = async () => {
  loading.value = true
  error.value = null
  try {
    const [albumsRes, songsRes] = await Promise.all([
      fetch('/data/albums.json'),
      fetch('/data/songs.json')
    ])
    if (!albumsRes.ok || !songsRes.ok) throw new Error('数据加载失败')
    const allAlbums = await albumsRes.json()
    const allSongs = await songsRes.json()
    
    const found = allAlbums.find(a => a.id == albumId)
    if (!found) throw new Error('专辑不存在')
    album.value = found
    songs.value = allSongs.filter(s => s.albumId == albumId)
  } catch (err) {
    error.value = err.message || '加载失败'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const playSong = (song) => {
  if (!album.value) return
  console.log('[AlbumDetail] 播放歌曲:', song.title)
  playerStore.playSong(song, album.value)
}

const playNext = (song) => {
  if (!album.value) return
  console.log('[AlbumDetail] 下一首播放:', song.title)
  playerStore.addSongToNext(song, album.value)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toISOString().split('T')[0]
}

// 监听专辑变化，更新背景（仅在冬念春时生效）
watch(() => album.value, (newAlbum) => {
  if (newAlbum?.id === 2 && newAlbum?.coverImage && rainEffectRef.value) {
    rainEffectRef.value.updateTexture(newAlbum.coverImage)
  }
})

onMounted(() => {
  fetchAlbumDetail()
})
</script>

<style scoped>
/* ===== 页面布局 ===== */
.page-wrapper {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
}

/* ===== 普通背景（非冬念春） ===== */
.bg-fallback {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  background-size: cover !important;
  background-position: center !important;
  background-color: #1a1a1a;
}

/* ===== 冬念春遮罩层 ===== */
.mask-layer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1;
  background: rgba(30, 30, 30, 0.65);
  pointer-events: none;
}

/* ===== 内容层 ===== */
.detail-container {
  position: relative;
  z-index: 2;
  max-width: 900px;
  margin: 0 auto;
  padding: 140px 20px 80px;
  color: #fff;
}
</style>
```

#### frontend\src\views\ArtistView.vue

```vue
<template>
  <div class="artist-page">
    <h1>🎤 歌手页</h1>
    <p>这里将展示 ZRay 的个人信息、演出经历等。</p>
  </div>
</template>

<style scoped>
.artist-page {
  position: relative;
  z-index: 2;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120px 20px 60px;
  color: #fff;
}
.artist-page h1 {
  font-size: 42px;
  margin-bottom: 20px;
}
.artist-page p {
  font-size: 18px;
  color: rgba(255,255,255,0.6);
}
</style>
```

#### frontend\src\views\DesignView.vue

```vue
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
```

#### frontend\src\views\HomeView.vue

```vue
<template>
  <div class="home">
    <!-- ===== 上半部分：全屏展示区 ===== -->
    <section class="hero-section" ref="heroSection">
      <div class="scroll-indicator" @click="scrollTo('design')">
        <span>SCROLL</span>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M7 13l5 5 5-5M7 6l5 5 5-5"/>
        </svg>
      </div>
    </section>

    <!-- ===== 设计作品 ===== -->
    <section class="work-section design-section" ref="designSection">
      <div class="work-block design-block">
        <h2 class="work-title reveal-title" ref="designTitle">设计作品</h2>
        <div class="design-manifesto reveal-text">
          <p>
            我的设计实践始于对"场所生命力"的思考。我认为，空间并不是一个静止的物理容器，而是由人的行为、感知、记忆以及自然与社会过程共同塑造的动态存在。人不断介入空间、赋予空间意义，而空间也通过自身的尺度、氛围、边界与环境条件反过来影响人的行为与感受。在这种持续的相互作用中，一个单纯的空间逐渐成为具有身份、记忆与情感的场所。
          </p>
          <p>
            因此，我所关注的并不仅是如何创造一个空间，而是如何让一个场所逐渐形成属于自己的"精神"。设计对我而言，是建立条件、关系与可能性，让人与环境之间的互动能够持续发生，并在时间中积累出独特的氛围与意义。我希望设计最终创造的不是一个被固定定义的对象，而是一个能够被使用、被感知、被记忆，并不断自我生长的场所——一个真正拥有生命力与自身精神的地方。
          </p>
        </div>
        <router-link to="/design" class="work-link reveal-text">参观设计 →</router-link>
      </div>
    </section>

    <!-- ===== 音乐作品 ===== -->
    <section class="work-section music-section" ref="musicSection">
      <div class="work-block music-block">
        <h2 class="work-title reveal-title" ref="musicTitle">音乐作品</h2>
        <div class="music-manifesto reveal-text">
          <p>
            我的音乐创作是一种情感表达、经历记录与自我反思的结合。我将音乐视为一种承载个人经验的媒介，将那些难以被直接言说的情绪、关系与人生片段转化为声音。每一首作品既是当下情绪的表达，也是对某段经历的保存，使已经发生的事情以另一种形式被重新记录和感知。
          </p>
          <p>
            随着时间推移，我也逐渐将音乐从单纯的情绪表达转向对自身经历的重新审视。创作并不只是记录发生过什么，更是一个回望、理解和重新赋予意义的过程。我会在声音、文字与氛围中重新处理过去的经验，让情绪从即时的感受转化为可以被反复观看的记忆。对我而言，音乐因此不仅记录生活，也成为理解自己、整理经历，并与过去保持对话的一种方式。
          </p>
        </div>
        <router-link to="/music" class="work-link reveal-text">欣赏音乐 →</router-link>
      </div>
    </section>

    <!-- ===== 个人简介 ===== -->
    <section class="work-section career-section" ref="careerSection">
      <div class="career-block">
        <h2 class="work-title reveal-title" ref="careerTitle">个人简介</h2>
        <div class="career-manifesto reveal-text">
          <p class="section-title">教育背景</p>
          <p>
            <strong>波兹南艺术大学（UAP）</strong>｜波兹南，波兰<br>
            景观设计 学士｜2023–2026
          </p>
          <p>
            · 核心课程：景观规划与设计、公共空间设计、生态景观设计、城市空间理论、植物配置<br>
            · 接受欧洲现代景观设计体系训练，注重场地分析、社会议题与设计表达的结合
          </p>
          <p>
            <strong>西北师范大学（NWNU）</strong>｜兰州，中国<br>
            景观设计 学士｜2022–2026
          </p>
          <p>
            · 中波联合培养双学位项目，系统学习过中国景观设计理论与实践
          </p>
          <p>
            具有中国与欧洲双重设计教育背景，在西北师范大学与波兹南艺术大学接受景观设计与空间设计训练，并在不同的教育与文化环境中建立了较为多元的设计视角。GPA 4.5+ / 5.0。
          </p>

          <p class="section-title">专业方向</p>
          <p>
            专注于景观设计、空间设计与环境设计，关注景观、公共空间、社区与城市环境之间的关系。具有从场地分析、概念构思到总体规划、空间设计、植物设计及视觉表达的完整项目经验，GPA 4.5+ / 5.0。
          </p>

          <p class="section-title">设计理念</p>
          <p>
            我的设计始于感知。面对一个场地，我首先通过观察与直觉感受其氛围、气质与潜在体验，并以此建立设计方向；随后通过功能、尺度、动线、材料、植物及场地条件等理性手段，将感知转化为空间。设计完成后，我再次回到人的体验中，对空间进行"感性验收"，检验实际感受是否与最初的设计意图一致，并持续调整。
          </p>
          <p>
            因此，我的设计过程形成了一个循环：感性定调—理性构建—感性验收。
          </p>
          <p>
            音乐与艺术创作是这一方法的重要来源。作为独立音乐创作者，我长期探索情绪、氛围、质感与审美，这种创作经验培养了我对空间整体气质与感官体验的敏感度。音乐并非被直接转化为空间形式，而是影响我感受、判断与构建空间的方式；与此同时，设计中对于人与人、人与环境关系的思考，也不断反哺我的音乐创作。
          </p>
          <p>
            对我而言，音乐与设计是两种相互影响的创作媒介：音乐塑造我感受空间的方式，而空间设计拓展我表达音乐的可能性。
          </p>

          <p class="section-title">联系方式</p>
          <p class="contact-email">
            zrayli808@gmail.com / 1423951971@qq.com
          </p>
        </div>
      </div>
    </section>

    <div class="footer">
      <a href="#">&copy; 2026 · Design</a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const heroSection = ref(null)
const designSection = ref(null)
const musicSection = ref(null)
const careerSection = ref(null)

const designTitle = ref(null)
const musicTitle = ref(null)
const careerTitle = ref(null)

const route = useRoute()
const router = useRouter()

function scrollTo(section) {
  const map = {
    design: designSection,
    music: musicSection,
    career: careerSection
  }
  const target = map[section]
  if (target && target.value) {
    target.value.scrollIntoView({ behavior: 'smooth' })
    router.replace({ query: {} })
  }
}

onMounted(() => {
  const scrollParam = route.query.scroll
  if (scrollParam && ['design', 'music', 'career'].includes(scrollParam)) {
    nextTick(() => {
      scrollTo(scrollParam)
    })
  }
})

watch(() => route.query.scroll, (newVal) => {
  if (newVal && ['design', 'music', 'career'].includes(newVal)) {
    nextTick(() => {
      scrollTo(newVal)
    })
  }
})

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible')
        observer.unobserve(entry.target)
      }
    })
  }, { threshold: 0.1 })

  const elementsToObserve = [
    designTitle.value,
    musicTitle.value,
    careerTitle.value
  ]
  const designManifesto = document.querySelector('.design-manifesto')
  const musicManifesto = document.querySelector('.music-manifesto')
  const careerManifesto = document.querySelector('.career-manifesto')
  if (designManifesto) elementsToObserve.push(designManifesto)
  if (musicManifesto) elementsToObserve.push(musicManifesto)
  if (careerManifesto) elementsToObserve.push(careerManifesto)

  const linkElements = document.querySelectorAll('.work-link.reveal-text')
  linkElements.forEach(el => elementsToObserve.push(el))
  elementsToObserve.forEach(el => {
    if (el) observer.observe(el)
  })
})
</script>

<style scoped>
/* ===== 全局重置 ===== */
.home {
  min-height: 100vh;
  background: #ffffff;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  overflow-x: hidden;
}

/* ===== 上半部分：全屏 ===== */
.hero-section {
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  background-image: url('/showpics/bk1.jpg');
  background-size: cover;
  background-position: center;
}
.hero-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  z-index: 0;
}
.hero-section > * {
  position: relative;
  z-index: 1;
}

/* ===== 灰蓝色分隔线 ===== */
.hero-section::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: #7A8B9E;
  z-index: 2;
}

.scroll-indicator {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
  letter-spacing: 3px;
  text-transform: uppercase;
  cursor: pointer;
  transition: color 0.3s, transform 0.3s;
  z-index: 10;
}
.scroll-indicator:hover {
  color: rgba(255, 255, 255, 0.85);
  transform: translateX(-50%) translateY(4px);
}
.scroll-indicator svg {
  width: 24px;
  height: 24px;
  stroke: currentColor;
}

/* ===== 作品区块通用 ===== */
.work-section {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  position: relative;
}
.work-block {
  max-width: 720px;
  width: 100%;
  position: relative;
  z-index: 1;
}
.work-title {
  font-size: 48px;
  font-weight: 300;
  letter-spacing: 4px;
  color: #1a1a1a;
  margin: 0 0 16px 0;
}
.work-link {
  display: inline-block;
  padding: 12px 40px;
  border: 1px solid #1a1a1a;
  color: #1a1a1a;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 2px;
  transition: background 0.3s, color 0.3s;
}
.work-link:hover {
  background: #1a1a1a;
  color: #ffffff;
}

/* ============================================================ */
/* ===== 设计作品区块 ===== */
.design-section {
  background: 
    url('/showpics/bk2.jpg'),
    url('/showpics/bk2-1.png');
  background-size: 40% auto, 100% 100%;
  background-position: right center, 0 0;
  background-repeat: no-repeat, no-repeat;
  justify-content: center;
}

.design-section .work-title,
.design-section .work-link,
.design-section .design-manifesto {
  font-family: 'Times New Roman', Georgia, serif;
}

.design-section .design-block {
  transform: translateX(-200px);
  text-align: left;
}

.design-section .work-title,
.design-section .work-link {
  color: #1A2A3A;
}
.design-section .work-link {
  border-color: #1A2A3A;
}
.design-section .work-link:hover {
  background: #1A2A3A;
  color: #E8D5B7;
}

.design-manifesto {
  width: 560px;
  margin-bottom: 32px;
}

.design-manifesto p {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 15px;
  font-weight: 500;
  line-height: 2.0;
  letter-spacing: 0.4px;
  margin: 0 0 18px 0;
  text-align: justify;
  color: #1A2A3A;
}
.design-manifesto p:last-child {
  margin-bottom: 0;
}

/* ============================================================ */
/* ===== 音乐作品区块 ===== */
.music-section {
  background: 
    url('/showpics/bk3.jpg'),
    url('/showpics/bk2-1.png');
  background-size: 40% auto, 100% 100%;
  background-position: left center, 0 0;
  background-repeat: no-repeat, no-repeat;
  justify-content: center;
  border-top: none;
}

.music-section .work-title,
.music-section .work-link,
.music-section .music-manifesto {
  font-family: 'Times New Roman', Georgia, serif;
}

.music-section .music-block {
  transform: translateX(360px);
  text-align: left;
}

.music-section .work-title,
.music-section .work-link {
  color: #1A2A3A;
}
.music-section .work-link {
  border-color: #1A2A3A;
}
.music-section .work-link:hover {
  background: #1A2A3A;
  color: #E8D5B7;
}

.music-manifesto {
  width: 560px;
  margin-bottom: 32px;
  margin-left: 0;
}

.music-manifesto p {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 15px;
  font-weight: 500;
  line-height: 2.0;
  letter-spacing: 0.4px;
  margin: 0 0 18px 0;
  text-align: justify;
  color: #1A2A3A;
}
.music-manifesto p:last-child {
  margin-bottom: 0;
}

/* ============================================================ */
/* ===== 个人简介区块 ===== */
.career-section {
  background: 
    url('/showpics/bk4-1.png');
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  justify-content: flex-start;
  border-top: none;
  position: relative;
  aspect-ratio: 16 / 9;
  min-height: 0;
  width: 100%;
  background-color: #f5f0eb;
  padding: 0;
}

.career-section .work-title,
.career-section .career-manifesto {
  font-family: 'Times New Roman', Georgia, serif;
}

/* ★★★ 白框：宽度增加，圆角，透明度70，无滚动 ★★★ */
.career-section .career-block {
  position: absolute;
  left: 5%;
  top: 50%;
  transform: translateY(-50%);
  width: 46%;                         /* 从 38% 增加到 46% */
  height: auto;
  background: rgba(255, 255, 255, 0.7); /* 不透明度 70% */
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  border-radius: 16px;                /* ★★★ 圆角 ★★★ */
  padding: 36px 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
  text-align: left;
  max-width: none;
  margin: 0;
  overflow: visible;                  /* 移除滚动 */
}

.career-section .work-title {
  font-size: 28px;
  font-weight: 600;
  letter-spacing: 3px;
  margin: 0 0 14px 0;
  color: #1A2A3A;
  text-align: left;
}

.career-manifesto {
  flex: none;
}

.career-manifesto .section-title {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 1px;
  margin: 18px 0 8px 0;
  color: #1A2A3A;
  text-transform: uppercase;
}
.career-manifesto .section-title:first-of-type {
  margin-top: 0;
}

.career-manifesto p {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 15px;
  font-weight: 400;
  line-height: 1.9;
  letter-spacing: 0.2px;
  margin: 0 0 8px 0;
  text-align: justify;
  color: #1A2A3A;
}

.career-manifesto p strong {
  font-weight: 600;
}

.career-manifesto .contact-email {
  font-size: 16px;
  font-weight: 500;
  color: #1A2A3A;
  text-align: center;
  margin-top: 6px;
  letter-spacing: 0.5px;
  opacity: 0.8;
}

/* ===== 底部版权 ===== */
.footer {
  padding: 60px 0 30px;
  text-align: center;
  background: #ffffff;
}
.footer a {
  color: rgba(0, 0, 0, 0.3);
  text-decoration: none;
  font-size: 13px;
  letter-spacing: 2px;
  transition: color 0.3s;
}
.footer a:hover {
  color: rgba(0, 0, 0, 0.7);
}

/* ===== 渐显动画 ===== */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.reveal-title,
.reveal-text {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}
.reveal-title.visible,
.reveal-text.visible {
  opacity: 1;
  transform: translateY(0);
}
.reveal-text {
  transition-delay: 0.15s;
}

/* ===== 响应式 ===== */
@media (max-width: 1024px) {
  .design-section .design-block {
    transform: translateX(-140px);
  }
  .music-section .music-block {
    transform: translateX(252px);
  }
  .design-manifesto,
  .music-manifesto {
    width: 440px;
  }
  .design-manifesto p,
  .music-manifesto p {
    font-size: 14px;
  }
  /* 平板：框更宽 */
  .career-section .career-block {
    width: 52%;
    padding: 28px 24px;
    left: 4%;
  }
  .career-section .work-title {
    font-size: 26px;
  }
  .career-manifesto p {
    font-size: 14px;
  }
  .career-manifesto .section-title {
    font-size: 17px;
  }
  .career-manifesto .contact-email {
    font-size: 15px;
  }
}

@media (max-width: 768px) {
  .work-title { font-size: 36px; }
  .work-link { padding: 10px 32px; font-size: 14px; }
  .scroll-indicator { bottom: 20px; font-size: 10px; }

  .design-section .design-block {
    transform: translateX(-80px);
  }
  .music-section .music-block {
    transform: translateX(144px);
  }
  .design-manifesto,
  .music-manifesto {
    width: 100%;
    max-width: 100%;
  }
  .design-manifesto p,
  .music-manifesto p {
    font-size: 14px;
    line-height: 1.9;
  }

  /* 小屏：框变为全宽，相对定位 */
  .career-section {
    aspect-ratio: auto;
    min-height: 60vh;
    background-size: cover;
    justify-content: center;
    padding: 40px 16px;
  }
  .career-section .career-block {
    position: relative;
    left: 0;
    top: 0;
    transform: none;
    width: 100%;
    height: auto;
    padding: 28px 22px;
    border-radius: 16px;
    overflow: visible;
  }
  .career-section .work-title {
    font-size: 30px;
    text-align: center;
  }
  .career-manifesto p {
    font-size: 16px;
  }
  .career-manifesto .section-title {
    font-size: 19px;
  }
  .career-manifesto .contact-email {
    font-size: 17px;
  }
}

@media (max-width: 480px) {
  .work-title { font-size: 28px; }
  .work-link { padding: 8px 24px; font-size: 13px; }

  .design-section .design-block,
  .music-section .music-block {
    transform: translateX(0);
    text-align: center;
  }
  .design-manifesto,
  .music-manifesto {
    width: 100%;
  }
  .design-manifesto p,
  .music-manifesto p {
    font-size: 13px;
    line-height: 1.8;
    text-align: justify;
  }

  .career-section {
    min-height: 50vh;
    padding: 20px 12px;
  }
  .career-section .career-block {
    padding: 20px 16px;
    border-radius: 12px;
  }
  .career-section .work-title {
    font-size: 26px;
  }
  .career-manifesto p {
    font-size: 15px;
  }
  .career-manifesto .section-title {
    font-size: 17px;
  }
  .career-manifesto .contact-email {
    font-size: 16px;
  }
}
</style>
```

#### frontend\src\views\MusicView.vue

```vue
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
```

### JavaScript文件文件

#### frontend\src\composables\useI18n.js

```javascript
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
```

#### frontend\src\locales\en.js

```javascript
export default {
  nav: {
    design: 'Design Works',
    music: 'Music Works',
    about: 'About'
  },
  home: {
    scroll: 'SCROLL',
    designTitle: 'Design Works',
    designDesc: [
      'My design practice begins with thinking about the "vitality of place." I believe that space is not a static physical container, but a dynamic existence shaped by human behavior, perception, memory, and natural and social processes. People continuously intervene in space, giving it meaning, while space in turn influences human behavior and feelings through its scale, atmosphere, boundaries, and environmental conditions. In this ongoing interaction, a mere space gradually becomes a place with identity, memory, and emotion.',
      'Therefore, what I care about is not just how to create a space, but how to let a place gradually form its own "spirit." Design, for me, is about establishing conditions, relationships, and possibilities, allowing the interaction between people and the environment to continue, and accumulating unique atmosphere and meaning over time. I hope that design ultimately creates not a fixed object, but a place that can be used, perceived, remembered, and continuously grows—a place with true vitality and its own spirit.'
    ],
    designBtn: 'Visit Design →',
    musicTitle: 'Music Works',
    musicDesc: [
      'My music creation is a combination of emotional expression, experience recording, and self-reflection. I regard music as a medium that carries personal experiences, transforming emotions, relationships, and life fragments that are difficult to express directly into sound. Each piece is both an expression of current emotion and a preservation of a certain experience, allowing what has happened to be recorded and perceived in another form.',
      'Over time, I have gradually shifted music from pure emotional expression to re-examining my own experiences. Creation is not just about recording what happened, but also about looking back, understanding, and re-giving meaning. I re-process past experiences through sound, words, and atmosphere, transforming emotions from immediate feelings into memories that can be revisited. For me, music therefore not only records life but also becomes a way to understand myself, organize experiences, and maintain a dialogue with the past.'
    ],
    musicBtn: 'Listen Music →',
    careerTitle: 'About Me',
    careerSections: {
      education: 'Education',
      direction: 'Professional Direction',
      philosophy: 'Design Philosophy',
      contact: 'Contact'
    },
    careerContent: {
      uap: 'University of Arts Poznan (UAP)｜Poznan, Poland',
      uapDegree: 'Bachelor of Landscape Architecture｜2023–2026',
      uapCourses: '· Core Courses: Landscape Planning and Design, Public Space Design, Ecological Landscape Design, Urban Space Theory, Plant Configuration',
      uapTraining: '· Trained in European modern landscape design system, focusing on site analysis, social issues, and design expression',
      nwnu: 'Northwest Normal University (NWNU)｜Lanzhou, China',
      nwnuDegree: 'Bachelor of Landscape Architecture｜2022–2026',
      nwnuProgram: '· China-Poland Joint Double Degree Program, systematically studied Chinese landscape design theory and practice',
      background: 'With a dual design education background from China and Europe, I received training in landscape architecture and spatial design at Northwest Normal University and the University of Arts Poznan, establishing a diverse design perspective across different educational and cultural environments. GPA 4.5+ / 5.0.',
      directionText: 'Specializing in landscape design, spatial design, and environmental design, focusing on the relationships between landscape, public space, community, and urban environment. Experienced in the complete project process from site analysis and conceptual development to master planning, spatial design, planting design, and visual presentation. GPA 4.5+ / 5.0.',
      philosophy1: 'My design starts with perception. Facing a site, I first sense its atmosphere, character, and potential experience through observation and intuition, establishing the design direction; then I transform perception into space through rational means such as function, scale, circulation, materials, plants, and site conditions. After the design is completed, I return to human experience, conducting a "sensory acceptance" to verify whether the actual feeling aligns with the original design intent, and continuously adjust.',
      philosophy2: 'Thus, my design process forms a cycle: Perceptual Tuning — Rational Construction — Sensory Acceptance.',
      philosophy3: 'Music and artistic creation are important sources of this approach. As an independent music creator, I have long explored emotion, atmosphere, texture, and aesthetics, and this creative experience has cultivated my sensitivity to the overall character and sensory experience of space. Music is not directly transformed into spatial form, but rather influences the way I feel, judge, and construct space; at the same time, reflections on human relationships and the human-environment connection in design also feed back into my music creation.',
      philosophy4: 'For me, music and design are two mutually influencing creative mediums: music shapes the way I perceive space, and spatial design expands the possibilities of my musical expression.',
      email: 'zrayli808@gmail.com / 1423951971@qq.com'
    },
    footer: '© 2026 · Design'
  },
  about: {
    title: 'About',
    subtitle: 'Behind This Site',
    text1: 'This is a portfolio site for an independent musician, using minimalist visual language to convey music and attitude.',
    text2: 'Design inspired by the minimalist aesthetics of BIG — black, white, gray, white space, restraint.'
  },
  music: {
    back: '← Back',
    title: 'Music Works',
    loading: 'Loading...',
    noData: 'No albums available',
    error: 'Failed to load data, please ensure data files exist',
    footer: '© 2026 · Music Journey'
  },
  design: {
    close: '✕'
  },
  album: {
    songs: 'Songs',
    detail: 'Album Detail',
    loading: 'Loading songs...',
    noSongs: 'No songs available, please add data first',
    unknownArtist: 'Unknown Artist',
    unknownDate: 'Unknown Date',
    back: '← Back',
    albumIntro: 'Album Introduction',
    playNext: 'Play Next'
  }
}
```

#### frontend\src\locales\zh.js

```javascript
export default {
  nav: {
    design: '设计作品',
    music: '音乐作品',
    about: '关于我们'
  },
  home: {
    scroll: 'SCROLL',
    designTitle: '设计作品',
    designDesc: [
      '我的设计实践始于对"场所生命力"的思考。我认为，空间并不是一个静止的物理容器，而是由人的行为、感知、记忆以及自然与社会过程共同塑造的动态存在。人不断介入空间、赋予空间意义，而空间也通过自身的尺度、氛围、边界与环境条件反过来影响人的行为与感受。在这种持续的相互作用中，一个单纯的空间逐渐成为具有身份、记忆与情感的场所。',
      '因此，我所关注的并不仅是如何创造一个空间，而是如何让一个场所逐渐形成属于自己的"精神"。设计对我而言，是建立条件、关系与可能性，让人与环境之间的互动能够持续发生，并在时间中积累出独特的氛围与意义。我希望设计最终创造的不是一个被固定定义的对象，而是一个能够被使用、被感知、被记忆，并不断自我生长的场所——一个真正拥有生命力与自身精神的地方。'
    ],
    designBtn: '参观设计 →',
    musicTitle: '音乐作品',
    musicDesc: [
      '我的音乐创作是一种情感表达、经历记录与自我反思的结合。我将音乐视为一种承载个人经验的媒介，将那些难以被直接言说的情绪、关系与人生片段转化为声音。每一首作品既是当下情绪的表达，也是对某段经历的保存，使已经发生的事情以另一种形式被重新记录和感知。',
      '随着时间推移，我也逐渐将音乐从单纯的情绪表达转向对自身经历的重新审视。创作并不只是记录发生过什么，更是一个回望、理解和重新赋予意义的过程。我会在声音、文字与氛围中重新处理过去的经验，让情绪从即时的感受转化为可以被反复观看的记忆。对我而言，音乐因此不仅记录生活，也成为理解自己、整理经历，并与过去保持对话的一种方式。'
    ],
    musicBtn: '欣赏音乐 →',
    careerTitle: '个人简介',
    careerSections: {
      education: '教育背景',
      direction: '专业方向',
      philosophy: '设计理念',
      contact: '联系方式'
    },
    careerContent: {
      uap: '波兹南艺术大学（UAP）｜波兹南，波兰',
      uapDegree: '景观设计 学士｜2023–2026',
      uapCourses: '· 核心课程：景观规划与设计、公共空间设计、生态景观设计、城市空间理论、植物配置',
      uapTraining: '· 接受欧洲现代景观设计体系训练，注重场地分析、社会议题与设计表达的结合',
      nwnu: '西北师范大学（NWNU）｜兰州，中国',
      nwnuDegree: '景观设计 学士｜2022–2026',
      nwnuProgram: '· 中波联合培养双学位项目，系统学习过中国景观设计理论与实践',
      background: '具有中国与欧洲双重设计教育背景，在西北师范大学与波兹南艺术大学接受景观设计与空间设计训练，并在不同的教育与文化环境中建立了较为多元的设计视角。GPA 4.5+ / 5.0。',
      directionText: '专注于景观设计、空间设计与环境设计，关注景观、公共空间、社区与城市环境之间的关系。具有从场地分析、概念构思到总体规划、空间设计、植物设计及视觉表达的完整项目经验，GPA 4.5+ / 5.0。',
      philosophy1: '我的设计始于感知。面对一个场地，我首先通过观察与直觉感受其氛围、气质与潜在体验，并以此建立设计方向；随后通过功能、尺度、动线、材料、植物及场地条件等理性手段，将感知转化为空间。设计完成后，我再次回到人的体验中，对空间进行"感性验收"，检验实际感受是否与最初的设计意图一致，并持续调整。',
      philosophy2: '因此，我的设计过程形成了一个循环：感性定调—理性构建—感性验收。',
      philosophy3: '音乐与艺术创作是这一方法的重要来源。作为独立音乐创作者，我长期探索情绪、氛围、质感与审美，这种创作经验培养了我对空间整体气质与感官体验的敏感度。音乐并非被直接转化为空间形式，而是影响我感受、判断与构建空间的方式；与此同时，设计中对于人与人、人与环境关系的思考，也不断反哺我的音乐创作。',
      philosophy4: '对我而言，音乐与设计是两种相互影响的创作媒介：音乐塑造我感受空间的方式，而空间设计拓展我表达音乐的可能性。',
      email: 'zrayli808@gmail.com / 1423951971@qq.com'
    },
    footer: '© 2026 · Design'
  },
  about: {
    title: '关于我们',
    subtitle: '这个站点的背后',
    text1: '这是一个独立音乐人的作品展示站，用简洁的视觉语言传递音乐与态度。',
    text2: '设计灵感来自建筑事务所 BIG 的极简美学 —— 黑白灰，留白，克制。'
  },
  music: {
    back: '← 返回',
    title: '音乐作品',
    loading: '加载中...',
    noData: '暂无专辑',
    error: '数据加载失败，请确保数据文件存在',
    footer: '© 2026 · 音乐历程'
  },
  design: {
    close: '✕'
  },
  album: {
    songs: '歌曲',
    detail: '专辑详情',
    loading: '加载歌曲中...',
    noSongs: '暂无歌曲，请先添加数据',
    unknownArtist: '未知艺术家',
    unknownDate: '未知日期',
    back: '← 返回',
    albumIntro: '专辑简介',
    playNext: '下一首播放'
  }
}
```

#### frontend\src\main.js

```javascript
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
```

#### frontend\src\router\index.js

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AlbumDetailView from '../views/AlbumDetailView.vue'
import DesignView from '../views/DesignView.vue'
import MusicView from '../views/MusicView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/design', name: 'design', component: DesignView },
  { path: '/music', name: 'music', component: MusicView },
  { path: '/album/:id', name: 'album-detail', component: AlbumDetailView, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

#### frontend\src\stores\player.js

```javascript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const usePlayerStore = defineStore('player', () => {
  const queue = ref([])
  const currentIndex = ref(0)
  const isPlaying = ref(false)
  const currentTime = ref(0)
  const duration = ref(0)
  const volume = ref(0.8)
  const playlistVisible = ref(false)

  const currentSong = computed(() => {
    return queue.value[currentIndex.value] || null
  })

  const currentAlbum = computed(() => {
    return currentSong.value?.album || null
  })

  // 播放指定歌曲（添加到队列头部，后来居上）
  function playSong(song, album) {
    // 如果歌曲已在队列中，移除原位置
    const existingIndex = queue.value.findIndex(s => s.id === song.id && s.album?.id === album?.id)
    if (existingIndex !== -1) {
      queue.value.splice(existingIndex, 1)
      // 如果移除位置在当前索引之前，调整 currentIndex
      if (existingIndex < currentIndex.value) {
        currentIndex.value--
      }
    }
    // 添加到队列头部
    queue.value.unshift({ ...song, album })
    currentIndex.value = 0
    isPlaying.value = true
  }

  // 下一首播放（插入到当前歌曲之后）
  function addSongToNext(song, album) {
    const existingIndex = queue.value.findIndex(s => s.id === song.id && s.album?.id === album?.id)
    if (existingIndex !== -1) {
      queue.value.splice(existingIndex, 1)
      if (existingIndex <= currentIndex.value) {
        currentIndex.value--
      }
    }
    const insertIndex = currentIndex.value + 1
    queue.value.splice(insertIndex, 0, { ...song, album })
    if (queue.value.length === 1) {
      currentIndex.value = 0
      isPlaying.value = true
    }
  }

  // ★★★ 播放整张专辑（从本地 songs.json 读取） ★★★
  async function playAlbum(album) {
    try {
      const res = await fetch('/data/songs.json')
      if (!res.ok) throw new Error('加载歌曲数据失败')
      const allSongs = await res.json()
      // 根据 albumId 过滤出该专辑的歌曲
      const albumSongs = allSongs.filter(s => s.albumId === album.id)
      // 按 trackNumber 排序
      albumSongs.sort((a, b) => a.trackNumber - b.trackNumber)
      queue.value = albumSongs.map(song => ({ ...song, album }))
      currentIndex.value = 0
      currentTime.value = 0
      isPlaying.value = true
    } catch (err) {
      console.error('播放专辑失败:', err)
    }
  }

  function clearQueue() {
    queue.value = []
    currentIndex.value = 0
    isPlaying.value = false
    currentTime.value = 0
    duration.value = 0
    playlistVisible.value = false
  }

  function removeSong(index) {
    if (index < 0 || index >= queue.value.length) return
    if (index === currentIndex.value) {
      if (queue.value.length > 1) {
        if (index === queue.value.length - 1) {
          currentIndex.value = index - 1
        } else {
          currentIndex.value = index
        }
        queue.value.splice(index, 1)
      } else {
        clearQueue()
        return
      }
    } else {
      if (index < currentIndex.value) {
        queue.value.splice(index, 1)
        currentIndex.value--
      } else {
        queue.value.splice(index, 1)
      }
    }
    if (queue.value.length === 0) clearQueue()
  }

  function togglePlay() {
    isPlaying.value = !isPlaying.value
  }

  function next() {
    if (queue.value.length === 0) return
    if (currentIndex.value < queue.value.length - 1) {
      currentIndex.value++
      currentTime.value = 0
    } else {
      isPlaying.value = false
    }
  }

  function prev() {
    if (queue.value.length === 0) return
    if (currentIndex.value > 0) {
      currentIndex.value--
      currentTime.value = 0
    } else {
      isPlaying.value = false
    }
  }

  function setProgress(time) {
    currentTime.value = time
  }

  function togglePlaylist() {
    playlistVisible.value = !playlistVisible.value
  }

  return {
    queue,
    currentIndex,
    isPlaying,
    currentTime,
    duration,
    volume,
    playlistVisible,
    currentSong,
    currentAlbum,
    playSong,
    addSongToNext,
    playAlbum,
    clearQueue,
    removeSong,
    togglePlay,
    next,
    prev,
    setProgress,
    togglePlaylist
  }
})
```

#### frontend\src\stores\ui.js

```javascript
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
```

#### frontend\vite.config.js

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173
  }
})
```

### CSS样式文件文件

#### frontend\src\style.css

```css
:root {
  --text: #6b6375;
  --text-h: #08060d;
  --bg: #fff;
  --border: #e5e4e7;
  --code-bg: #f4f3ec;
  --accent: #aa3bff;
  --accent-bg: rgba(170, 59, 255, 0.1);
  --accent-border: rgba(170, 59, 255, 0.5);
  --social-bg: rgba(244, 243, 236, 0.5);
  --shadow:
    rgba(0, 0, 0, 0.1) 0 10px 15px -3px, rgba(0, 0, 0, 0.05) 0 4px 6px -2px;

  --sans: system-ui, 'Segoe UI', Roboto, sans-serif;
  --heading: system-ui, 'Segoe UI', Roboto, sans-serif;
  --mono: ui-monospace, Consolas, monospace;

  font: 18px/145% var(--sans);
  letter-spacing: 0.18px;
  color-scheme: light dark;
  color: var(--text);
  background: var(--bg);
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  @media (max-width: 1024px) {
    font-size: 16px;
  }
}

@media (prefers-color-scheme: dark) {
  :root {
    --text: #9ca3af;
    --text-h: #f3f4f6;
    --bg: #16171d;
    --border: #2e303a;
    --code-bg: #1f2028;
    --accent: #c084fc;
    --accent-bg: rgba(192, 132, 252, 0.15);
    --accent-border: rgba(192, 132, 252, 0.5);
    --social-bg: rgba(47, 48, 58, 0.5);
    --shadow:
      rgba(0, 0, 0, 0.4) 0 10px 15px -3px, rgba(0, 0, 0, 0.25) 0 4px 6px -2px;
  }

  #social .button-icon {
    filter: invert(1) brightness(2);
  }
}

body {
  margin: 0;
}

h1,
h2 {
  font-family: var(--heading);
  font-weight: 500;
  color: var(--text-h);
}

h1 {
  font-size: 56px;
  letter-spacing: -1.68px;
  margin: 32px 0;
  @media (max-width: 1024px) {
    font-size: 36px;
    margin: 20px 0;
  }
}
h2 {
  font-size: 24px;
  line-height: 118%;
  letter-spacing: -0.24px;
  margin: 0 0 8px;
  @media (max-width: 1024px) {
    font-size: 20px;
  }
}
p {
  margin: 0;
}

code,
.counter {
  font-family: var(--mono);
  display: inline-flex;
  border-radius: 4px;
  color: var(--text-h);
}

code {
  font-size: 15px;
  line-height: 135%;
  padding: 4px 8px;
  background: var(--code-bg);
}

.counter {
  font-size: 16px;
  padding: 5px 10px;
  border-radius: 5px;
  color: var(--accent);
  background: var(--accent-bg);
  border: 2px solid transparent;
  transition: border-color 0.3s;
  margin-bottom: 24px;

  &:hover {
    border-color: var(--accent-border);
  }
  &:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
}

.hero {
  position: relative;

  .base,
  .framework,
  .vite {
    inset-inline: 0;
    margin: 0 auto;
  }

  .base {
    width: 170px;
    position: relative;
    z-index: 0;
  }

  .framework,
  .vite {
    position: absolute;
  }

  .framework {
    z-index: 1;
    top: 34px;
    height: 28px;
    transform: perspective(2000px) rotateZ(300deg) rotateX(44deg) rotateY(39deg)
      scale(1.4);
  }

  .vite {
    z-index: 0;
    top: 107px;
    height: 26px;
    width: auto;
    transform: perspective(2000px) rotateZ(300deg) rotateX(40deg) rotateY(39deg)
      scale(0.8);
  }
}

#app {
  width: 1126px;
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
  border-inline: 1px solid var(--border);
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

#center {
  display: flex;
  flex-direction: column;
  gap: 25px;
  place-content: center;
  place-items: center;
  flex-grow: 1;

  @media (max-width: 1024px) {
    padding: 32px 20px 24px;
    gap: 18px;
  }
}

#next-steps {
  display: flex;
  border-top: 1px solid var(--border);
  text-align: left;

  & > div {
    flex: 1 1 0;
    padding: 32px;
    @media (max-width: 1024px) {
      padding: 24px 20px;
    }
  }

  .icon {
    margin-bottom: 16px;
    width: 22px;
    height: 22px;
  }

  @media (max-width: 1024px) {
    flex-direction: column;
    text-align: center;
  }
}

#docs {
  border-right: 1px solid var(--border);

  @media (max-width: 1024px) {
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
}

#next-steps ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 8px;
  margin: 32px 0 0;

  .logo {
    height: 18px;
  }

  a {
    color: var(--text-h);
    font-size: 16px;
    border-radius: 6px;
    background: var(--social-bg);
    display: flex;
    padding: 6px 12px;
    align-items: center;
    gap: 8px;
    text-decoration: none;
    transition: box-shadow 0.3s;

    &:hover {
      box-shadow: var(--shadow);
    }
    .button-icon {
      height: 18px;
      width: 18px;
    }
  }

  @media (max-width: 1024px) {
    margin-top: 20px;
    flex-wrap: wrap;
    justify-content: center;

    li {
      flex: 1 1 calc(50% - 8px);
    }

    a {
      width: 100%;
      justify-content: center;
      box-sizing: border-box;
    }
  }
}

#spacer {
  height: 88px;
  border-top: 1px solid var(--border);
  @media (max-width: 1024px) {
    height: 48px;
  }
}

.ticks {
  position: relative;
  width: 100%;

  &::before,
  &::after {
    content: '';
    position: absolute;
    top: -4.5px;
    border: 5px solid transparent;
  }

  &::before {
    left: 0;
    border-left-color: var(--border);
  }
  &::after {
    right: 0;
    border-right-color: var(--border);
  }
}
```

#### frontend\src\styles\components\album-detail.css

```css
/* ===== 页面容器 ===== */
.page-wrapper {
  position: relative;
  width: 100%;
  min-height: 100vh;
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
.detail-container {
  position: relative;
  z-index: 2;
  max-width: 900px;
  margin: 0 auto;
  padding: 140px 20px 80px;
  color: #fff;
}

/* ===== 专辑头部 ===== */
.album-header {
  display: flex;
  align-items: flex-start;
  gap: 30px;
  margin-bottom: 30px;
}
.album-cover-wrapper {
  flex-shrink: 0;
}
.album-cover {
  width: 160px;
  height: 160px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.placeholder-cover {
  width: 160px;
  height: 160px;
  border-radius: 12px;
  background: linear-gradient(135deg, #2d2d44, #1a1a2e);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 64px;
  font-weight: 700;
  color: rgba(255,255,255,0.15);
}
.album-title-wrapper {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  padding-top: 4px;
}
.title-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.album-title {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}
.album-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  color: rgba(255,255,255,0.6);
}
.meta-divider {
  color: rgba(255,255,255,0.3);
}
.meta-item {
  color: rgba(255,255,255,0.6);
}
.back-btn {
  background: none;
  border: none;
  color: rgba(255,255,255,0.6);
  font-size: 16px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  transition: background 0.2s, color 0.2s;
  white-space: nowrap;
}
.back-btn:hover {
  background: rgba(255,255,255,0.08);
  color: #fff;
}

/* ===== Tab 栏 ===== */
.tab-bar {
  display: flex;
  gap: 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 24px;
}
.tab-btn {
  background: none;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 500;
  color: rgba(255,255,255,0.5);
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
}
.tab-btn:hover {
  color: rgba(255,255,255,0.8);
}
.tab-btn.active {
  color: #fff;
  border-bottom-color: #f7971e;
}

/* ===== 内容区 ===== */
.tab-content {
  min-height: 200px;
}

/* ===== 歌曲列表 ===== */
.song-list {
  background: rgba(0,0,0,0.25);
  border-radius: 12px;
  padding: 8px 0;
  backdrop-filter: blur(4px);
}
.song-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  transition: background 0.2s;
}
.song-item:hover {
  background: rgba(255,255,255,0.05);
}
.track-number {
  width: 36px;
  color: rgba(255,255,255,0.3);
  font-size: 14px;
  text-align: left;
}
.song-title {
  flex: 1;
  font-size: 16px;
  color: #fff;
  text-align: left;
}
.song-duration {
  width: 60px;
  text-align: right;
  color: rgba(255,255,255,0.4);
  font-size: 14px;
  margin-right: 8px;
}
.play-btn-small {
  background: none;
  border: none;
  color: #f7971e;
  font-size: 18px;
  cursor: pointer;
  padding: 0 8px;
}
.play-btn-small:hover {
  color: #ffb347;
}
.play-next-btn {
  background: none;
  border: none;
  color: rgba(255,255,255,0.3);
  font-size: 12px;
  cursor: pointer;
  padding: 0 8px;
  transition: color 0.2s;
  white-space: nowrap;
}
.play-next-btn:hover {
  color: #f7971e;
}

/* ===== 专辑详情 ===== */
.album-detail {
  background: rgba(0,0,0,0.25);
  border-radius: 12px;
  padding: 24px 20px;
  backdrop-filter: blur(4px);
}
.detail-header {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 24px;
}
.detail-title {
  font-size: 24px;
  font-weight: 600;
  color: rgba(255,255,255,0.7);
  letter-spacing: 1px;
}
.detail-content {
  font-size: 16px;
  line-height: 1.8;
  color: rgba(255,255,255,0.85);
  margin: 0;
  padding: 0;
}
.intro-quote,
.intro-text {
  text-align: left !important;
}
.intro-quote {
  font-size: 18px;
  font-weight: 500;
  color: rgba(255,255,255,0.9);
  margin: 0 0 4px 0;
  letter-spacing: 1px;
}
.intro-text {
  margin: 0 0 12px 0;
  line-height: 1.8;
}
.intro-text:last-child {
  margin-bottom: 0;
}
.status {
  text-align: center;
  padding: 40px 0;
  color: rgba(255,255,255,0.6);
}
.status.error {
  color: #ff6b6b;
}
.empty-tip {
  padding: 30px;
  text-align: center;
  color: rgba(255,255,255,0.3);
}

/* ===== 响应式 ===== */
@media (max-width: 700px) {
  .album-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 16px;
  }
  .album-cover, .placeholder-cover {
    width: 120px;
    height: 120px;
  }
  .album-title-wrapper {
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }
  .title-group {
    align-items: center;
  }
  .album-title {
    font-size: 26px;
  }
  .album-meta {
    font-size: 14px;
  }
  .back-btn {
    font-size: 14px;
  }
  .tab-btn {
    padding: 10px 16px;
    font-size: 14px;
  }
  .detail-container {
    padding-top: 120px;
  }
  .detail-title {
    font-size: 20px;
  }
  .intro-quote {
    font-size: 16px;
    text-align: left !important;
  }
  .intro-text {
    font-size: 15px;
    text-align: left !important;
  }
  .play-next-btn {
    font-size: 11px;
  }
}
```

#### frontend\src\styles\components\player.css

```css
/* ===== 与导航栏统一风格 ===== */
.player-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 80px;
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 999;
  color: #fff;
  box-sizing: border-box;
}

.player-left {
  display: flex;
  align-items: center;
  gap: 14px;
  flex: 0 0 220px;
}
.cover-mini {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  object-fit: cover;
  background: #333;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
.song-info .title {
  font-size: 15px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
  color: #fff;
}
.song-info .artist {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
}

.player-center {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  justify-content: center;
  max-width: 600px;
}
.ctrl-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  padding: 6px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, color 0.2s, transform 0.1s;
}
.ctrl-btn:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.08);
}
.ctrl-btn:active {
  transform: scale(0.92);
}
.play-btn {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #f7971e, #ffb347);
  color: #fff;
  box-shadow: 0 4px 15px rgba(247, 151, 30, 0.3);
}
.play-btn:hover {
  background: linear-gradient(135deg, #ffa82e, #ffc15e);
  color: #fff;
  transform: scale(1.04);
}
.play-btn:active {
  transform: scale(0.96);
}
.ctrl-btn svg {
  display: block;
}
.time {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  min-width: 36px;
  font-variant-numeric: tabular-nums;
}
.progress-bar {
  flex: 1;
  min-width: 80px;
  height: 4px;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
  outline: none;
  transition: background 0.2s;
}
.progress-bar::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #f7971e;
  cursor: pointer;
  box-shadow: 0 0 8px rgba(247, 151, 30, 0.4);
  transition: transform 0.15s;
}
.progress-bar::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}
.progress-bar::-moz-range-thumb {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #f7971e;
  cursor: pointer;
  border: none;
}

.player-right {
  flex: 0 0 120px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.playlist-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  padding: 4px 8px;
  margin-right: 8px;
  border-radius: 4px;
  transition: background 0.2s, color 0.2s;
}
.playlist-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}
.volume-bar {
  width: 80px;
  height: 4px;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
  outline: none;
}
.volume-bar::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  cursor: pointer;
}
.volume-bar::-webkit-slider-thumb:hover {
  background: #fff;
}
.volume-bar::-moz-range-thumb {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  border: none;
}

@media (max-width: 700px) {
  .player-bar {
    padding: 0 12px;
    flex-wrap: wrap;
    height: auto;
    min-height: 70px;
    gap: 8px;
  }
  .player-left {
    flex: 0 0 auto;
  }
  .player-center {
    order: 3;
    flex: 1 1 100%;
    gap: 8px;
  }
  .player-right {
    flex: 0 0 auto;
  }
  .cover-mini {
    width: 40px;
    height: 40px;
  }
  .song-info .title {
    font-size: 13px;
    max-width: 100px;
  }
  .play-btn {
    width: 36px;
    height: 36px;
  }
  .ctrl-btn svg {
    width: 18px;
    height: 18px;
  }
  .player-right {
    flex: 0 0 80px;
  }
  .volume-bar {
    width: 50px;
  }
}
```

#### frontend\src\styles\components\playlist.css

```css
/* ===== 遮罩层 ===== */
.playlist-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  display: flex;
  justify-content: flex-end;
}
.playlist-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

/* ===== 侧栏面板 ===== */
.playlist-panel {
  position: relative;
  width: 380px;
  max-width: 85%;
  height: 100%;
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-left: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  padding: 24px 20px 20px;
  box-sizing: border-box;
  animation: slideIn 0.3s ease;
}
@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

/* ===== 头部 ===== */
.playlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.playlist-header h3 {
  color: #fff;
  font-size: 20px;
  font-weight: 500;
  margin: 0;
  letter-spacing: 0.5px;
}
.clear-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  font-size: 14px;
  padding: 4px 12px;
  border-radius: 4px;
  transition: background 0.2s, color 0.2s;
}
.clear-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}

/* ===== 列表区域 ===== */
.playlist-body {
  flex: 1;
  overflow-y: auto;
  padding-top: 12px;
}
.playlist-item {
  display: flex;
  align-items: center;
  padding: 10px 12px 10px 0;
  margin-bottom: 4px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  color: rgba(255, 255, 255, 0.8);
}
.playlist-item:hover {
  background: rgba(255, 255, 255, 0.06);
}
.playlist-item.active {
  background: rgba(247, 151, 30, 0.12);
  color: #fff;
}
.playlist-item.active .song-title {
  color: #f7971e;
}
.playlist-item .song-title {
  flex: 1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.playlist-item .song-artist {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  margin-left: 10px;
  white-space: nowrap;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
}
.remove-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.2);
  font-size: 18px;
  cursor: pointer;
  padding: 0 4px;
  margin-left: 8px;
  transition: color 0.2s, transform 0.2s;
}
.remove-btn:hover {
  color: #ff6b6b;
  transform: scale(1.2);
}

.empty-tip {
  text-align: center;
  color: rgba(255, 255, 255, 0.3);
  padding: 60px 0;
  font-size: 14px;
}

/* ===== 滚动条美化 ===== */
.playlist-body::-webkit-scrollbar {
  width: 4px;
}
.playlist-body::-webkit-scrollbar-track {
  background: transparent;
}
.playlist-body::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
}
.playlist-body::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.25);
}
```

#### frontend\src\styles\globals.css

```css
/* frontend/src/styles/globals.css */
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}
.glass-morphism {
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: var(--zray-blur-md);
  -webkit-backdrop-filter: var(--zray-blur-md);
  border: 1px solid var(--zray-border-light);
}
.gold-text {
  color: var(--zray-gold);
}
.gold-border-bottom {
  border-bottom: 2px solid var(--zray-gold);
}
```

#### frontend\src\styles\reset.css

```css
/* frontend/src/styles/reset.css */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html, body, #app {
  width: 100%;
  min-height: 100vh;
  background: #ffffff;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
}
img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
a {
  text-decoration: none;
  color: inherit;
}
```

#### frontend\src\styles\variables.css

```css
/* frontend/src/styles/variables.css */
:root {
  --zray-gold: #333333;
  --zray-gold-light: #666666;
  --zray-bg-dark: #ffffff;
  --zray-bg-card: rgba(0, 0, 0, 0.35);
  --zray-text-white:#1a1a1a;
  --zray-text-muted: #888888;
  --zray-border-light: rgba(255, 255, 255, 0.06);
  --zray-shadow-sm: 0 2px 12px rgba(0, 0, 0, 0.15);
  --zray-shadow-lg: 0 20px 60px rgba(0, 0, 0, 0.4);
  --zray-blur-md: blur(12px);
  --zray-radius-sm: 8px;
  --zray-radius-md: 12px;
  --zray-radius-lg: 16px;
  --zray-nav-height: 84px;
  --zray-player-height: 80px;
  --zray-transition-smooth: 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

#### frontend\src\styles\views\music.css

```css
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

/* ===== 时间线（复用原有样式） ===== */
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
```

#### frontend\src\styles\views\work.css

```css
/* ===== 重置 ===== */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ===== 页面容器 ===== */
.page-wrapper {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow-x: hidden;
}

/* ===== 背景层 ===== */
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

/* ===== 内容层 ===== */
.shell {
  position: relative;
  z-index: 2;
  width: 100%;
  min-height: 100vh;
  padding: 164px 0 80px;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* ===== 卡片网格 ===== */
.category-grid {
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 80px;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

/* ===== 卡片 ===== */
.category-card {
  flex: 0 0 324px;
  height: 709px;
  border-radius: 0;
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow:
    0 8px 30px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.06),
    inset 0 0 20px rgba(255, 255, 255, 0.02);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  position: relative;
  background-size: cover;
  background-position: center;
}
.category-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(247, 151, 30, 0.2),
    inset 0 0 30px rgba(247, 151, 30, 0.03);
}
.category-card:active {
  transform: scale(0.97);
}

/* ===== 半透明覆盖层 ===== */
.overlay {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 10px 16px;
  transition: top 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  will-change: top;
  overflow: hidden;
}

/* 悬停时覆盖层高度变为 2/9 */
.category-card:hover .overlay {
  top: 77.778%;
}

/* ===== 文字信息 ===== */
.card-info {
  text-align: center;
  width: 100%;
}
.card-title {
  font-size: 28px;
  font-weight: 600;
  color: #ffffff;
  letter-spacing: 4px;
  margin-bottom: 4px;
  transition: font-size 0.3s ease;
}
.card-sub {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 5px;
  font-weight: 300;
  transition: font-size 0.3s ease;
}

.category-card:hover .card-title {
  font-size: 22px;
}
.category-card:hover .card-sub {
  font-size: 13px;
  letter-spacing: 4px;
}

/* ===== 底部 ===== */
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
.footer a:hover {
  color: rgba(255, 255, 255, 0.7);
}

/* ============================================================ */
/* ===== 响应式 ===== */
@media only screen and (max-width: 820px) {
  .shell {
    padding: 120px 0 80px;
  }
  .category-grid {
    gap: 50px;
  }
  .category-card {
    flex: 0 0 216px;
    height: 473px;
  }
  .card-title {
    font-size: 24px;
  }
  .category-card:hover .card-title {
    font-size: 18px;
  }
  .category-card:hover .card-sub {
    font-size: 11px;
  }
}

@media only screen and (max-width: 480px) {
  .shell {
    padding: 100px 0 40px;
  }
  .category-grid {
    flex-direction: column;
    align-items: center;
    gap: 35px;
  }
  .category-card {
    flex: 0 0 162px;
    height: 355px;
    width: 162px;
  }
  .card-title {
    font-size: 20px;
  }
  .card-sub {
    font-size: 12px;
    letter-spacing: 3px;
  }
  .category-card:hover .card-title {
    font-size: 16px;
  }
  .category-card:hover .card-sub {
    font-size: 10px;
    letter-spacing: 2px;
  }
}
```

### HTML文件文件

#### frontend\index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ZRay 个人网站</title>
    <!-- 1. 引入 timelinr 的 CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jquery.timelinr@1.0.0/css/style.css" />
  </head>
  <body>
    <div id="app"></div>
    <!-- 2. 先加载 jQuery -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"></script>
    <!-- 3. 再加载 timelinr 插件 -->
    <script src="https://cdn.jsdelivr.net/npm/jquery.timelinr@1.0.0/js/jquery.timelinr.min.js"></script>
    <!-- 4. 最后加载 Vue 入口 -->
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

### Python文件文件

#### app.py

```python
# -*- coding: utf-8 -*-
"""
将当前目录下的文件结构及代码整合到Markdown文件
支持文件类型: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css
"""

import os
import sys
from pathlib import Path
import fnmatch

def get_directory_tree(start_path, ignore_patterns=None):
    """
    获取目录树结构
    """
    if ignore_patterns is None:
        ignore_patterns = ['.git', '__pycache__', '*.pyc', '.idea', 'build', 'dist', 'node_modules']
    
    tree_lines = []
    
    def _walk(dir_path, prefix=""):
        # 获取当前目录下的所有项目
        try:
            items = sorted(os.listdir(dir_path))
        except PermissionError:
            return
        
        # 过滤掉忽略的项目
        items = [item for item in items 
                if not any(fnmatch.fnmatch(item, pattern) 
                          for pattern in ignore_patterns)]
        
        for i, item in enumerate(items):
            item_path = os.path.join(dir_path, item)
            is_last = (i == len(items) - 1)
            
            # 选择适当的前缀符号
            if is_last:
                tree_lines.append(f"{prefix}└── {item}")
                new_prefix = prefix + "    "
            else:
                tree_lines.append(f"{prefix}├── {item}")
                new_prefix = prefix + "│   "
            
            # 如果是目录，递归遍历
            if os.path.isdir(item_path):
                _walk(item_path, new_prefix)
    
    # 添加根目录名称
    root_name = os.path.basename(os.path.abspath(start_path))
    tree_lines.append(f"{root_name}/")
    _walk(start_path)
    
    return "\n".join(tree_lines)

def should_process_file(filename):
    """
    判断文件是否需要处理
    支持的扩展名: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css
    """
    valid_extensions = [
        '.h', '.cpp', '.pro', '.vue', '.js', '.ts', '.jsx', '.tsx',
        '.yml', '.yaml', '.xml', '.html', '.htm', '.py', '.css'   # <--- 添加 .css
    ]
    return any(filename.endswith(ext) for ext in valid_extensions)

def read_file_content(filepath):
    """
    读取文件内容
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 如果UTF-8解码失败，尝试使用其他编码
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                return f.read()
        except:
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                return f"[无法读取文件: 编码不支持]"
    except Exception as e:
        return f"[读取文件时出错: {str(e)}]"

def generate_markdown(output_file="project_documentation.md"):
    """
    生成Markdown文档
    """
    current_dir = os.getcwd()
    dir_name = os.path.basename(current_dir)
    
    with open(output_file, 'w', encoding='utf-8') as md_file:
        # 写入标题
        md_file.write(f"# {dir_name} 项目文档\n\n")
        
        # 写入生成时间
        from datetime import datetime
        md_file.write(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        # 写入目录树
        md_file.write("## 目录结构\n\n")
        md_file.write("```\n")
        md_file.write(get_directory_tree(current_dir))
        md_file.write("\n```\n\n")
        
        # 收集所有需要处理的文件
        files_to_process = []
        for root, dirs, files in os.walk(current_dir):
            # 忽略一些目录
            dirs[:] = [d for d in dirs if not d.startswith('.') 
                      and d not in ['__pycache__', 'build', 'dist', 'node_modules']]
            
            for file in files:
                if should_process_file(file):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, current_dir)
                    files_to_process.append((rel_path, full_path))
        
        # 按文件类型和路径排序
        files_to_process.sort(key=lambda x: (os.path.splitext(x[0])[1], x[0]))
        
        # 写入文件内容
        md_file.write("## 源代码\n\n")
        
        if not files_to_process:
            md_file.write("*没有找到支持的文件类型*\n")
            md_file.write("*支持的文件类型: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css*\n")
        else:
            # 按文件类型分组
            file_types = {
                '.pro': 'Qt项目文件',
                '.h': '头文件',
                '.cpp': 'C++源文件',
                '.vue': 'Vue组件',
                '.js': 'JavaScript文件',
                '.ts': 'TypeScript文件',
                '.jsx': 'React JSX文件',
                '.tsx': 'React TSX文件',
                '.yml': 'YAML配置文件',
                '.yaml': 'YAML配置文件',
                '.xml': 'XML文件',
                '.html': 'HTML文件',
                '.htm': 'HTML文件',
                '.py': 'Python文件',
                '.css': 'CSS样式文件'   # <--- 添加 .css 描述
            }
            
            # 定义分组顺序
            extensions_order = [
                '.pro', '.h', '.cpp', 
                '.vue', '.ts', '.tsx', '.js', '.jsx',
                '.yml', '.yaml', '.xml', 
                '.css',                     # <--- 添加 .css，放在 HTML 之前或之后均可
                '.html', '.htm',
                '.py'
            ]
            
            for ext in extensions_order:
                type_files = [(rel, full) for rel, full in files_to_process if rel.endswith(ext)]
                if type_files:
                    md_file.write(f"### {file_types.get(ext, ext)}文件\n\n")
                    
                    for rel_path, full_path in type_files:
                        # 写入文件名作为子标题
                        md_file.write(f"#### {rel_path}\n\n")
                        
                        # 写入文件内容
                        content = read_file_content(full_path)
                        
                        # 根据文件扩展名设置代码块语言
                        lang_map = {
                            '.h': 'cpp',
                            '.cpp': 'cpp',
                            '.pro': 'makefile',
                            '.vue': 'vue',
                            '.js': 'javascript',
                            '.ts': 'typescript',
                            '.jsx': 'jsx',
                            '.tsx': 'tsx',
                            '.yml': 'yaml',
                            '.yaml': 'yaml',
                            '.xml': 'xml',
                            '.html': 'html',
                            '.htm': 'html',
                            '.py': 'python',
                            '.css': 'css'      # <--- 添加 .css 对应的语言标识
                        }
                        lang = lang_map.get(ext, '')
                        
                        md_file.write(f"```{lang}\n")
                        md_file.write(content)
                        if content and not content.endswith('\n'):
                            md_file.write('\n')
                        md_file.write("```\n\n")
        
        # 写入统计信息
        md_file.write("## 统计信息\n\n")
        md_file.write(f"- 总文件数: {len(files_to_process)}\n")
        
        # 按扩展名统计
        ext_counts = {}
        for rel_path, _ in files_to_process:
            ext = os.path.splitext(rel_path)[1]
            ext_counts[ext] = ext_counts.get(ext, 0) + 1
        
        # 显示统计信息
        ext_names = {
            '.pro': 'Qt项目',
            '.h': '头文件',
            '.cpp': 'C++源文件',
            '.vue': 'Vue组件',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React JSX',
            '.tsx': 'React TSX',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.xml': 'XML',
            '.html': 'HTML',
            '.htm': 'HTML',
            '.py': 'Python',
            '.css': 'CSS样式'    # <--- 添加 .css 统计名称
        }
        
        for ext, count in ext_counts.items():
            name = ext_names.get(ext, ext)
            md_file.write(f"- {name}文件 ({ext}): {count}个\n")
    
    print(f"文档已生成: {output_file}")
    print(f"共处理了 {len(files_to_process)} 个文件")
    print(f"支持的文件类型: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css")

def main():
    """
    主函数
    """
    print("项目文档生成器 (支持C/C++/Qt/Vue/JavaScript/TypeScript/YAML/XML/HTML/Python/CSS)")
    print("=" * 80)
    
    # 可以自定义输出文件名
    output_filename = "project_documentation.md"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    
    generate_markdown(output_filename)

if __name__ == "__main__":
    main()
```

#### tempCodeRunnerFile.py

```python
# -*- coding: utf-8 -*-
"""
将当前目录下的文件结构及代码整合到Markdown文件
支持文件类型: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css
"""

import os
import sys
from pathlib import Path
import fnmatch

def get_directory_tree(start_path, ignore_patterns=None):
    """
    获取目录树结构
    """
    if ignore_patterns is None:
        ignore_patterns = ['.git', '__pycache__', '*.pyc', '.idea', 'build', 'dist', 'node_modules']
    
    tree_lines = []
    
    def _walk(dir_path, prefix=""):
        # 获取当前目录下的所有项目
        try:
            items = sorted(os.listdir(dir_path))
        except PermissionError:
            return
        
        # 过滤掉忽略的项目
        items = [item for item in items 
                if not any(fnmatch.fnmatch(item, pattern) 
                          for pattern in ignore_patterns)]
        
        for i, item in enumerate(items):
            item_path = os.path.join(dir_path, item)
            is_last = (i == len(items) - 1)
            
            # 选择适当的前缀符号
            if is_last:
                tree_lines.append(f"{prefix}└── {item}")
                new_prefix = prefix + "    "
            else:
                tree_lines.append(f"{prefix}├── {item}")
                new_prefix = prefix + "│   "
            
            # 如果是目录，递归遍历
            if os.path.isdir(item_path):
                _walk(item_path, new_prefix)
    
    # 添加根目录名称
    root_name = os.path.basename(os.path.abspath(start_path))
    tree_lines.append(f"{root_name}/")
    _walk(start_path)
    
    return "\n".join(tree_lines)

def should_process_file(filename):
    """
    判断文件是否需要处理
    支持的扩展名: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css
    """
    valid_extensions = [
        '.h', '.cpp', '.pro', '.vue', '.js', '.ts', '.jsx', '.tsx',
        '.yml', '.yaml', '.xml', '.html', '.htm', '.py', '.css'   # <--- 添加 .css
    ]
    return any(filename.endswith(ext) for ext in valid_extensions)

def read_file_content(filepath):
    """
    读取文件内容
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 如果UTF-8解码失败，尝试使用其他编码
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                return f.read()
        except:
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                return f"[无法读取文件: 编码不支持]"
    except Exception as e:
        return f"[读取文件时出错: {str(e)}]"

def generate_markdown(output_file="project_documentation.md"):
    """
    生成Markdown文档
    """
    current_dir = os.getcwd()
    dir_name = os.path.basename(current_dir)
    
    with open(output_file, 'w', encoding='utf-8') as md_file:
        # 写入标题
        md_file.write(f"# {dir_name} 项目文档\n\n")
        
        # 写入生成时间
        from datetime import datetime
        md_file.write(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        # 写入目录树
        md_file.write("## 目录结构\n\n")
        md_file.write("```\n")
        md_file.write(get_directory_tree(current_dir))
        md_file.write("\n```\n\n")
        
        # 收集所有需要处理的文件
        files_to_process = []
        for root, dirs, files in os.walk(current_dir):
            # 忽略一些目录
            dirs[:] = [d for d in dirs if not d.startswith('.') 
                      and d not in ['__pycache__', 'build', 'dist', 'node_modules']]
            
            for file in files:
                if should_process_file(file):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, current_dir)
                    files_to_process.append((rel_path, full_path))
        
        # 按文件类型和路径排序
        files_to_process.sort(key=lambda x: (os.path.splitext(x[0])[1], x[0]))
        
        # 写入文件内容
        md_file.write("## 源代码\n\n")
        
        if not files_to_process:
            md_file.write("*没有找到支持的文件类型*\n")
            md_file.write("*支持的文件类型: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css*\n")
        else:
            # 按文件类型分组
            file_types = {
                '.pro': 'Qt项目文件',
                '.h': '头文件',
                '.cpp': 'C++源文件',
                '.vue': 'Vue组件',
                '.js': 'JavaScript文件',
                '.ts': 'TypeScript文件',
                '.jsx': 'React JSX文件',
                '.tsx': 'React TSX文件',
                '.yml': 'YAML配置文件',
                '.yaml': 'YAML配置文件',
                '.xml': 'XML文件',
                '.html': 'HTML文件',
                '.htm': 'HTML文件',
                '.py': 'Python文件',
                '.css': 'CSS样式文件'   # <--- 添加 .css 描述
            }
            
            # 定义分组顺序
            extensions_order = [
                '.pro', '.h', '.cpp', 
                '.vue', '.ts', '.tsx', '.js', '.jsx',
                '.yml', '.yaml', '.xml', 
                '.css',                     # <--- 添加 .css，放在 HTML 之前或之后均可
                '.html', '.htm',
                '.py'
            ]
            
            for ext in extensions_order:
                type_files = [(rel, full) for rel, full in files_to_process if rel.endswith(ext)]
                if type_files:
                    md_file.write(f"### {file_types.get(ext, ext)}文件\n\n")
                    
                    for rel_path, full_path in type_files:
                        # 写入文件名作为子标题
                        md_file.write(f"#### {rel_path}\n\n")
                        
                        # 写入文件内容
                        content = read_file_content(full_path)
                        
                        # 根据文件扩展名设置代码块语言
                        lang_map = {
                            '.h': 'cpp',
                            '.cpp': 'cpp',
                            '.pro': 'makefile',
                            '.vue': 'vue',
                            '.js': 'javascript',
                            '.ts': 'typescript',
                            '.jsx': 'jsx',
                            '.tsx': 'tsx',
                            '.yml': 'yaml',
                            '.yaml': 'yaml',
                            '.xml': 'xml',
                            '.html': 'html',
                            '.htm': 'html',
                            '.py': 'python',
                            '.css': 'css'      # <--- 添加 .css 对应的语言标识
                        }
                        lang = lang_map.get(ext, '')
                        
                        md_file.write(f"```{lang}\n")
                        md_file.write(content)
                        if content and not content.endswith('\n'):
                            md_file.write('\n')
                        md_file.write("```\n\n")
        
        # 写入统计信息
        md_file.write("## 统计信息\n\n")
        md_file.write(f"- 总文件数: {len(files_to_process)}\n")
        
        # 按扩展名统计
        ext_counts = {}
        for rel_path, _ in files_to_process:
            ext = os.path.splitext(rel_path)[1]
            ext_counts[ext] = ext_counts.get(ext, 0) + 1
        
        # 显示统计信息
        ext_names = {
            '.pro': 'Qt项目',
            '.h': '头文件',
            '.cpp': 'C++源文件',
            '.vue': 'Vue组件',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React JSX',
            '.tsx': 'React TSX',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.xml': 'XML',
            '.html': 'HTML',
            '.htm': 'HTML',
            '.py': 'Python',
            '.css': 'CSS样式'    # <--- 添加 .css 统计名称
        }
        
        for ext, count in ext_counts.items():
            name = ext_names.get(ext, ext)
            md_file.write(f"- {name}文件 ({ext}): {count}个\n")
    
    print(f"文档已生成: {output_file}")
    print(f"共处理了 {len(files_to_process)} 个文件")
    print(f"支持的文件类型: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css")

def main():
    """
    主函数
    """
    print("项目文档生成器 (支持C/C++/Qt/Vue/JavaScript/TypeScript/YAML/XML/HTML/Python/CSS)")
    print("=" * 80)
    
    # 可以自定义输出文件名
    output_filename = "project_documentation.md"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    
    generate_markdown(output_filename)

if __name__ == "__main__":
    main()
```

## 统计信息

- 总文件数: 31
- CSS样式文件 (.css): 9个
- HTML文件 (.html): 1个
- JavaScript文件 (.js): 8个
- Python文件 (.py): 2个
- Vue组件文件 (.vue): 11个
