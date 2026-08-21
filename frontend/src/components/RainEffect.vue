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