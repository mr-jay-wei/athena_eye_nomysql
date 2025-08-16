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
        
        <!-- 监控参数 -->
        <div class="config-section">
          <h3>监控参数</h3>
          <div class="form-group">
            <label for="MONITOR_INTERVAL_MINUTES">监控频率（分钟）</label>
            <input id="MONITOR_INTERVAL_MINUTES" type="number" v-model.number="config.MONITOR_INTERVAL_MINUTES" min="1" />
          </div>
          <div class="form-group">
            <label for="PRICE_DATA_INTERVAL">K线周期</label>
            <select id="PRICE_DATA_INTERVAL" v-model="config.PRICE_DATA_INTERVAL">
              <option value="1min">1分钟</option>
              <option value="5min">5分钟</option>
              <option value="15min">15分钟</option>
              <option value="30min">30分钟</option>
              <option value="1hour">1小时</option>
            </select>
          </div>
          <div class="form-group">
            <label for="VOLUME_LOOKBACK_PERIOD">成交量回看期</label>
            <input id="VOLUME_LOOKBACK_PERIOD" type="number" v-model.number="config.VOLUME_LOOKBACK_PERIOD" min="1" />
          </div>
          <div class="form-group">
            <label for="VOLUME_SPIKE_MULTIPLIER">成交量放大倍数阈值</label>
            <input id="VOLUME_SPIKE_MULTIPLIER" type="number" v-model.number="config.VOLUME_SPIKE_MULTIPLIER" step="0.1" min="0.1" />
          </div>
          <div class="form-group">
            <label for="PRICE_SIGNIFICANT_CHANGE_PERCENT">显著价格变化百分比（%）</label>
            <input id="PRICE_SIGNIFICANT_CHANGE_PERCENT" type="number" v-model.number="config.PRICE_SIGNIFICANT_CHANGE_PERCENT" step="0.1" min="0" />
          </div>
          <div class="form-group">
            <label for="SENTIMENT_SCORE_THRESHOLD">情绪评分阈值（1-9）</label>
            <input id="SENTIMENT_SCORE_THRESHOLD" type="number" v-model.number="config.SENTIMENT_SCORE_THRESHOLD" min="1" max="9" />
          </div>
          <div class="form-group">
            <label for="NEWS_FETCH_COUNT">新闻获取数量</label>
            <input id="NEWS_FETCH_COUNT" type="number" v-model.number="config.NEWS_FETCH_COUNT" min="1" max="100" />
          </div>
        </div>

        <!-- 邮件配置 -->
        <div class="config-section">
          <h3>邮件配置(必须是qq邮箱)</h3>
          <div class="form-group">
            <label for="SENDER_EMAIL">发件人邮箱</label>
            <input id="SENDER_EMAIL" type="email" v-model="config.SENDER_EMAIL" placeholder="your-email@qq.com" />
          </div>
          <div class="form-group">
            <label for="EMAIL_APP_PASSWORD">邮箱授权码</label>
            <input id="EMAIL_APP_PASSWORD" type="password" v-model="config.EMAIL_APP_PASSWORD" placeholder="邮箱授权码（非登录密码）" />
          </div>
          <div class="form-group">
            <label for="RECIPIENT_EMAIL">收件人邮箱</label>
            <input id="RECIPIENT_EMAIL" type="email" v-model="config.RECIPIENT_EMAIL" placeholder="recipient@qq.com" />
          </div>
          <div class="form-group">
            <label for="SMTP_SERVER">SMTP服务器</label>
            <input id="SMTP_SERVER" type="text" v-model="config.SMTP_SERVER" placeholder="smtp.qq.com" />
          </div>
          <div class="form-group">
            <label for="SMTP_PORT">SMTP端口</label>
            <input id="SMTP_PORT" type="number" v-model.number="config.SMTP_PORT" min="1" max="65535" />
          </div>
        </div>

        <!-- LLM配置 -->
        <div class="config-section">
          <h3>LLM配置</h3>
          <div class="form-group">
            <label for="OPENROUTER_API_KEY">API密钥</label>
            <input id="OPENROUTER_API_KEY" type="password" v-model="config.OPENROUTER_API_KEY" placeholder="sk-or-v1-..." />
          </div>
          <div class="form-group">
            <label for="OPENROUTER_BASE_URL">API基础URL</label>
            <input id="OPENROUTER_BASE_URL" type="url" v-model="config.OPENROUTER_BASE_URL" placeholder="https://openrouter.ai/api/v1" />
          </div>
          <div class="form-group">
            <label for="OPENROUTER_MODEL_NAME">使用的模型名称</label>
            <input id="OPENROUTER_MODEL_NAME" type="text" v-model="config.OPENROUTER_MODEL_NAME" placeholder="anthropic/claude-3.5-sonnet" />
          </div>
        </div>

        <!-- API配置 -->
        <div class="config-section">
          <h3>数据源API配置</h3>
          <div class="form-group">
            <label for="POLYGON_API_KEY">Polygon.io API密钥</label>
            <input id="POLYGON_API_KEY" type="password" v-model="config.POLYGON_API_KEY" placeholder="Polygon.io API密钥" />
          </div>
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

.config-section { 
  margin-bottom: 2rem; 
  padding: 1.5rem; 
  border: 1px solid #e9ecef; 
  border-radius: 6px; 
  background-color: #f8f9fa; 
}

.config-section h3 { 
  margin-top: 0; 
  margin-bottom: 1rem; 
  color: #495057; 
  font-size: 1.2rem; 
  border-bottom: 2px solid #007bff; 
  padding-bottom: 0.5rem; 
}

.form-group { margin-bottom: 1.5rem; }

label { 
  display: block; 
  margin-bottom: 0.5rem; 
  font-weight: bold; 
  color: #555; 
  text-transform: none; 
}

input, select { 
  width: 100%; 
  padding: 0.8rem; 
  border: 1px solid #ccc; 
  border-radius: 4px; 
  font-size: 1rem; 
  transition: border-color 0.3s;
}

input:focus, select:focus { 
  outline: none; 
  border-color: #007bff; 
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25); 
}

input[type="password"] {
  font-family: monospace;
}

.save-btn { 
  background-color: #007bff; 
  color: white; 
  padding: 0.8rem 1.5rem; 
  border: none; 
  border-radius: 5px; 
  cursor: pointer; 
  font-size: 1rem; 
  transition: background-color 0.3s; 
  margin-top: 1rem;
}

.save-btn:hover:not(:disabled) { background-color: #0056b3; }
.save-btn:disabled { background-color: #aaa; cursor: not-allowed; }

.message { 
  margin-top: 1rem; 
  padding: 1rem; 
  border-radius: 5px; 
}

.message.success { 
  background-color: #d4edda; 
  color: #155724; 
  border: 1px solid #c3e6cb; 
}

.message.error { 
  background-color: #f8d7da; 
  color: #721c24; 
  border: 1px solid #f5c6cb; 
}

.message.info { 
  background-color: #cce5ff; 
  color: #004085; 
  border: 1px solid #b8daff; 
}
</style>