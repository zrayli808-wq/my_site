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