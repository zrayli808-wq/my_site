<template>
  <div class="page-wrapper" :class="{ 'winter-page': album?.id === 2 }">
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
            <template v-if="album?.id === 2">
              <p class="winter-eyebrow">ZRAY / SELECTED WORKS / 2023</p>
              <h1 class="album-title winter-title">冬念春</h1>
              <p class="winter-subtitle" lang="en">Winter Misses Spring</p>
              <p class="winter-meta">ZRay <span aria-hidden="true">·</span> <time datetime="2023-02-21">2023.02.21</time></p>
            </template>
            <h1 v-else class="album-title">{{ album?.title || '加载中...' }}</h1>
            <div v-if="album?.id !== 2" class="album-meta">
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
          <div v-else-if="album?.id === 2" class="winter-tracks">
            <p class="winter-list-caption"><span>TRACKLIST</span><span>08 TRACKS</span></p>
            <button
              v-for="(song, index) in songs"
              :key="song.id"
              type="button"
              class="winter-track"
              :class="{ 'is-current': playerStore.currentSong?.id === song.id && playerStore.currentAlbum?.id === 2 }"
              :aria-label="`播放 ${song.title}`"
              :aria-current="playerStore.currentSong?.id === song.id && playerStore.currentAlbum?.id === 2 ? 'true' : undefined"
              @click="playSong(song)"
            >
              <span class="winter-number">{{ String(index + 1).padStart(2, '0') }}</span>
              <span class="winter-song-name">{{ song.title }}</span>
              <svg class="winter-play-icon" aria-hidden="true" viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M8 5v14l11-7z" /></svg>
              <span class="winter-duration">{{ song.duration || '--:--' }}</span>
            </button>
            <p class="winter-colophon">冬日里的回望，写给春天。<span>WINTER MISSES SPRING — ZRAY</span></p>
          </div>
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
<!-- These overrides only match while the Winter album page is mounted. -->
<style src="../styles/views/winter-editorial.css"></style>
