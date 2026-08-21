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
