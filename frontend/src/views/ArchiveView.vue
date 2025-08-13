<script setup>
import { ref, onMounted, computed } from 'vue';

// --- 响应式变量 ---
const alerts = ref([]);            // 存储从API获取的所有警报记录
const selectedAlert = ref(null);   // 存储当前在弹窗中查看的警报详情
const isLoading = ref(true);
const error = ref(null);

// --- API 调用 ---
const fetchAlerts = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    // 新的API端点，一次性获取所有警报数据
    const response = await fetch('/api/archive?limit=200'); // 获取最近200条
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || '无法加载历史警报');
    }
    const data = await response.json();
    // 后端返回的是倒序，我们前端可以根据需要再次排序或直接使用
    alerts.value = data;
  } catch (err) {
    error.value = err.message;
  } finally {
    isLoading.value = false;
  }
};

// --- 生命周期钩子 ---
onMounted(fetchAlerts);

// --- UI交互函数 ---
const viewDetails = (alert) => {
  // 点击“查看详情”按钮时，设置选中的警报，并显示弹窗
  selectedAlert.value = alert;
};

const closeDetailsModal = () => {
  // 关闭弹窗
  selectedAlert.value = null;
};

// --- 计算属性 ---
// 一个简单的计算属性，用于动态决定警报类型的颜色
const getAlertTypeClass = (alertType) => {
  if (alertType.includes('看涨') || alertType.includes('机会')) {
    return 'positive';
  }
  if (alertType.includes('看跌') || alertType.includes('风险')) {
    return 'negative';
  }
  return 'neutral';
};

</script>

<template>
  <main class="archive-view">
    <h2>历史警报记录</h2>

    <div v-if="isLoading" class="loading-state">正在从数据库加载记录...</div>
    <div v-if="error" class="error-msg">{{ error }}</div>

    <div v-if="!isLoading && alerts.length > 0" class="card">
      <table class="alerts-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>时间 (UTC)</th>
            <th>股票代码</th>
            <th>警报类型</th>
            <th class="reason-col">核心判断</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alert in alerts" :key="alert.id">
            <td>{{ alert.id }}</td>
            <td>{{ new Date(alert.archive_timestamp_utc).toLocaleString('sv-SE') }}</td>
            <td><strong>{{ alert.ticker }}</strong></td>
            <td>
              <span :class="['alert-type-badge', getAlertTypeClass(alert.alert_type)]">
                {{ alert.alert_type }}
              </span>
            </td>
            <td class="reason-col">{{ alert.reason }}</td>
            <td>
              <button @click="viewDetails(alert)" class="details-btn">查看详情</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!isLoading && alerts.length === 0 && !error" class="placeholder">
      数据库中还没有任何警报记录。
    </div>

    <!-- 详情弹窗 (Modal) -->
    <div v-if="selectedAlert" class="modal-overlay" @click.self="closeDetailsModal">
      <div class="modal-content card">
        <button class="close-btn" @click="closeDetailsModal">&times;</button>
        <h3>警报详情 (ID: {{ selectedAlert.id }})</h3>
        <div class="details-grid">
          <p><strong>股票:</strong> {{ selectedAlert.ticker }}</p>
          <p><strong>类型:</strong> {{ selectedAlert.alert_type }}</p>
          <p><strong>时间:</strong> {{ new Date(selectedAlert.archive_timestamp_utc).toLocaleString() }}</p>
          <p class="full-width"><strong>核心判断:</strong> {{ selectedAlert.reason }}</p>
        </div>

        <details open>
          <summary>三维分析快照</summary>
          <div class="snapshot-grid">
            <span><strong>价格变化:</strong> {{ selectedAlert.price_change_percent }}%</span>
            <span><strong>成交量倍数:</strong> {{ selectedAlert.volume_multiplier }}x</span>
            <span><strong>情绪评分:</strong> {{ selectedAlert.sentiment_score }}/10</span>
          </div>
        </details>

        <details>
          <summary>触发时系统参数</summary>
          <pre>{{ JSON.stringify(selectedAlert.trigger_conditions, null, 2) }}</pre>
        </details>

        <details v-if="selectedAlert.raw_news_data && selectedAlert.raw_news_data.length > 0">
          <summary>原始新闻数据</summary>
          <ul>
            <li v-for="(news, index) in selectedAlert.raw_news_data" :key="index" class="news-item">
              <a :href="news.link" target="_blank" rel="noopener noreferrer">{{ news.title }}</a>
              <span v-if="news.source" class="news-source"> ({{ news.source }})</span>
            </li>
          </ul>
        </details>
      </div>
    </div>

  </main>
</template>

<style scoped>
/* --- 主布局与卡片 --- */
.archive-view {
  padding: 0 1rem;
  width: 100%;
}
.card {
  background-color: #ffffff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  overflow-x: auto; /* 让表格可以横向滚动 */
}

/* --- 表格样式 --- */
.alerts-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}
.alerts-table th, .alerts-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #e0e0e0;
  vertical-align: middle;
}
.alerts-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #343a40;
}
.alerts-table tbody tr:hover {
  background-color: #f1f3f5;
}
.reason-col {
  max-width: 400px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.details-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.details-btn:hover {
  background-color: #0056b3;
}

/* --- 警报类型徽章 --- */
.alert-type-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: bold;
  color: #fff;
}
.alert-type-badge.positive { background-color: #28a745; }
.alert-type-badge.negative { background-color: #dc3545; }
.alert-type-badge.neutral { background-color: #6c757d; }

/* --- 状态提示 --- */
.loading-state, .placeholder {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
  font-size: 1.2rem;
}
.error-msg {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 1rem;
  border-radius: 5px;
  text-align: center;
}

/* --- 详情弹窗 (Modal) --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}
.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #6c757d;
}
.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}
.full-width { grid-column: 1 / -1; }
details {
  margin-top: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.8rem;
}
summary { font-weight: bold; cursor: pointer; }
pre { background-color: #f5f5f5; padding: 1rem; border-radius: 5px; white-space: pre-wrap; word-break: break-all; margin-top: 0.5rem; }
.snapshot-grid { display: flex; gap: 2rem; margin-top: 0.5rem; }
.news-item { font-size: 0.9em; margin-top: 0.5rem; }
.news-item a { color: #007bff; text-decoration: none; }
.news-item a:hover { text-decoration: underline; }
.news-source { color: #6c757d; font-style: italic; }
strong { font-weight: bold; }
</style>