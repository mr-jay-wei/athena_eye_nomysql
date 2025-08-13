<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <h1>Athena Eye - 智能监控面板</h1>
      <nav>
        <RouterLink to="/">控制面板</RouterLink>
        <RouterLink to="/config">系统配置</RouterLink>
        <RouterLink to="/archive">历史警报</RouterLink>
      </nav>
    </div>
  </header>

  <!-- RouterView是所有页面的“出口”，我们的页面组件将在这里被渲染 -->
  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  border-bottom: 1px solid #ddd;
  margin-bottom: 2rem;
}

h1 {
  font-weight: bold;
  color: #2c3e50;
}

.wrapper {
  padding: 1rem 2rem;
}

nav {
  width: 100%;
  font-size: 1rem;
  text-align: left;
  margin-top: 1rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
  border-bottom: 2px solid hsla(160, 100%, 37%, 1);
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
  padding-left: 0;
}
</style>