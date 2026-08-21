<template>
  <div class="home">
    <!-- ===== 上半部分：全屏展示区 ===== -->
    <section class="hero-section" ref="heroSection">
      <!-- ★★★ ZRay's World!!! 标题 ★★★ -->
      <div class="hero-title">
        <div class="hero-title-line">ZRay's</div>
        <div class="hero-title-line">World!!!</div>
      </div>

      <div class="scroll-indicator" @click="scrollTo('design')">
        <span>{{ t('home.scroll') }}</span>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M7 13l5 5 5-5M7 6l5 5 5-5"/>
        </svg>
      </div>
    </section>

    <!-- ===== 设计作品 ===== -->
    <section class="work-section design-section" ref="designSection">
      <div class="work-block design-block">
        <h2 class="work-title reveal-title" ref="designTitle">{{ t('home.designTitle') }}</h2>
        <div class="design-manifesto reveal-text">
          <p>{{ t('home.designDesc')[0] }}</p>
          <p>{{ t('home.designDesc')[1] }}</p>
        </div>
        <router-link to="/design" class="work-link reveal-text">{{ t('home.designBtn') }}</router-link>
      </div>
    </section>

    <!-- ===== 音乐作品 ===== -->
    <section class="work-section music-section" ref="musicSection">
      <div class="work-block music-block">
        <h2 class="work-title reveal-title" ref="musicTitle">{{ t('home.musicTitle') }}</h2>
        <div class="music-manifesto reveal-text">
          <p>{{ t('home.musicDesc')[0] }}</p>
          <p>{{ t('home.musicDesc')[1] }}</p>
        </div>
        <router-link to="/music" class="work-link reveal-text">{{ t('home.musicBtn') }}</router-link>
      </div>
    </section>

    <!-- ===== 个人简介 ===== -->
    <section class="work-section career-section" ref="careerSection">
      <div class="career-block">
        <h2 class="work-title reveal-title" ref="careerTitle">{{ t('home.careerTitle') }}</h2>
        <div class="career-manifesto reveal-text">
          <p class="section-title">{{ t('home.careerSections.education') }}</p>
          <p>
            <strong>{{ t('home.careerContent.uap') }}</strong><br>
            {{ t('home.careerContent.uapDegree') }}
          </p>
          <p>{{ t('home.careerContent.uapCourses') }}</p>
          <p>{{ t('home.careerContent.uapTraining') }}</p>
          <p>
            <strong>{{ t('home.careerContent.nwnu') }}</strong><br>
            {{ t('home.careerContent.nwnuDegree') }}
          </p>
          <p>{{ t('home.careerContent.nwnuProgram') }}</p>
          <p>{{ t('home.careerContent.background') }}</p>

          <p class="section-title">{{ t('home.careerSections.direction') }}</p>
          <p>{{ t('home.careerContent.directionText') }}</p>

          <p class="section-title">{{ t('home.careerSections.philosophy') }}</p>
          <p>{{ t('home.careerContent.philosophy1') }}</p>
          <p>{{ t('home.careerContent.philosophy2') }}</p>
          <p>{{ t('home.careerContent.philosophy3') }}</p>
          <p>{{ t('home.careerContent.philosophy4') }}</p>

          <p class="section-title">{{ t('home.careerSections.contact') }}</p>
          <p class="contact-email">{{ t('home.careerContent.email') }}</p>
        </div>
      </div>
    </section>

    <div class="footer">
      <a href="#">{{ t('home.footer') }}</a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// ★★★ 注入国际化 ★★★
const i18n = inject('i18n')
const { t } = i18n

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

/* ===== ★★★ ZRay's World!!! 标题（右下角） ★★★ ===== */
.hero-title {
  position: absolute;
  bottom: 10%;
  right: 6%;
  z-index: 5;
  text-align: right;
  pointer-events: none;
  user-select: none;
  line-height: 1.1;           /* ★★★ 从 1 增加到 1.1，增加行间距 ★★★ */
}

.hero-title-line {
  font-family: 'Georgia', 'Times New Roman', serif;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 2px 30px rgba(0, 0, 0, 0.3);
  letter-spacing: 0.02em;
}

.hero-title-line:first-child {
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 300;
  opacity: 0.7;
  margin-bottom: -0.1em;
}

.hero-title-line:last-child {
  font-size: clamp(56px, 10vw, 120px);
  font-weight: 700;
}

/* ===== SCROLL 指示器 ===== */
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

.career-section .career-block {
  position: absolute;
  left: 5%;
  top: 50%;
  transform: translateY(-50%);
  width: 34%;
  height: auto;
  max-height: 85%;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  border-radius: 16px;
  padding: 22px 18px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
  text-align: left;
  max-width: none;
  margin: 0;
  overflow: visible;
}

.career-section .work-title {
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 3px;
  margin: 0 0 10px 0;
  color: #1A2A3A;
  text-align: left;
}

.career-manifesto {
  flex: none;
}

.career-manifesto .section-title {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 1px;
  margin: 12px 0 4px 0;
  color: #1A2A3A;
  text-transform: uppercase;
}
.career-manifesto .section-title:first-of-type {
  margin-top: 0;
}

.career-manifesto p {
  font-family: 'Times New Roman', Georgia, serif;
  font-size: 13px;
  font-weight: 400;
  line-height: 1.7;
  letter-spacing: 0.2px;
  margin: 0 0 4px 0;
  text-align: justify;
  color: #1A2A3A;
}

.career-manifesto p strong {
  font-weight: 600;
}

.career-manifesto .contact-email {
  font-size: 14px;
  font-weight: 500;
  color: #1A2A3A;
  text-align: center;
  margin-top: 4px;
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
  .career-section .career-block {
    width: 38%;
    padding: 20px 16px;
    left: 4%;
  }
  .career-section .work-title {
    font-size: 20px;
  }
  .career-manifesto p {
    font-size: 12px;
  }
  .career-manifesto .section-title {
    font-size: 14px;
  }
  .career-manifesto .contact-email {
    font-size: 13px;
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
    padding: 24px 20px;
    border-radius: 16px;
    overflow: visible;
  }
  .career-section .work-title {
    font-size: 28px;
    text-align: center;
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
    padding: 18px 14px;
    border-radius: 12px;
  }
  .career-section .work-title {
    font-size: 24px;
  }
  .career-manifesto p {
    font-size: 13px;
  }
  .career-manifesto .section-title {
    font-size: 15px;
  }
  .career-manifesto .contact-email {
    font-size: 14px;
  }
}
</style>