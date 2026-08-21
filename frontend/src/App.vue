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