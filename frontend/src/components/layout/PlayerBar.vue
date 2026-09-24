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
        aria-label="播放进度"
        :style="{ '--player-progress': `${player.duration ? Math.min(100, Math.max(0, player.currentTime / player.duration * 100)) : 0}%` }"
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
        aria-label="音量"
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
