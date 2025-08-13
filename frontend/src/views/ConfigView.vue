<script setup>
import { ref, onMounted } from 'vue'

const config = ref({}); // 用于存储配置项
const isLoading = ref(true); // 控制加载状态
const message = ref(''); // 用于显示反馈信息
const messageType = ref(''); // success 或 error

// 获取当前配置
const fetchConfig = async () => {
  isLoading.value = true;
  message.value = '';
  try {
    const response = await fetch('/api/config');
    if (!response.ok) throw new Error('无法加载配置');
    config.value = await response.json();
  } catch (error) {
    message.value = `错误: ${error.message}`;
    messageType.value = 'error';
  } finally {
    isLoading.value = false;
  }
};

// 保存配置
const saveConfig = async () => {
  isLoading.value = true;
  message.value = '正在保存...';
  messageType.value = 'info';
  try {
    const response = await fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config.value)
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '保存失败');
    }
    await response.json();
    message.value = '配置已成功保存！请注意，部分更改可能需要重启后台监控任务才能生效。';
    messageType.value = 'success';
  } catch (error) {
    message.value = `错误: ${error.message}`;
    messageType.value = 'error';
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchConfig);
</script>

<template>
  <main class="config-view">
    <h2>系统配置</h2>
    <div class="card">
      <div v-if="isLoading && !Object.keys(config).length">正在加载配置...</div>
      <form v-else @submit.prevent="saveConfig">
        <div v-for="(value, key) in config" :key="key" class="form-group">
          <label :for="key">{{ key.replaceAll('_', ' ') }}</label>
          <input 
            :id="key"
            :type="typeof value === 'number' ? 'number' : 'text'"
            v-model="config[key]"
            :step="typeof value === 'number' && !Number.isInteger(value) ? '0.1' : '1'"
          />
        </div>
        <button type="submit" class="save-btn" :disabled="isLoading">
          {{ isLoading ? '保存中...' : '保存更改' }}
        </button>
      </form>
      <div v-if="message" :class="['message', messageType]">
        {{ message }}
      </div>
    </div>
  </main>
</template>

<style scoped>
.config-view { padding: 0 2rem; }
.card { background-color: #fff; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.form-group { margin-bottom: 1.5rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: bold; text-transform: capitalize; color: #555; }
input { width: 100%; padding: 0.8rem; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; }
.save-btn { background-color: #007bff; color: white; padding: 0.8rem 1.5rem; border: none; border-radius: 5px; cursor: pointer; font-size: 1rem; transition: background-color 0.3s; }
.save-btn:hover:not(:disabled) { background-color: #0056b3; }
.save-btn:disabled { background-color: #aaa; cursor: not-allowed; }
.message { margin-top: 1rem; padding: 1rem; border-radius: 5px; }
.message.success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.message.error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.message.info { background-color: #cce5ff; color: #004085; border: 1px solid #b8daff; }
</style>