<script setup lang="ts">

</script>

<template>
  <div id="app-container">
    <router-view /> <!-- 必须保留，否则所有页面无法渲染 -->
  </div>
</template>

<style>
#app {
  min-height: 100vh;
}
#app-container {
  width: 100%; /* 撑满视口宽度 */
  min-width: 1200px; /* 设置最小宽度（根据业务需求调整） */
}
</style>
