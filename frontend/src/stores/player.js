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