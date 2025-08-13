<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// --- 响应式变量 ---
const statusText = ref('正在加载...');
const isRunning = ref(false);
const watchlist = ref([]);
const isLoading = ref(false); // 用于控制按钮的禁用状态
let statusInterval = null; // 用于存放我们的定时器

// --- 股票管理相关变量 ---
const stockList = ref([]);
const newStockTicker = ref('');
const newStockNotes = ref('');
const isStockLoading = ref(false);
const showAddStock = ref(false);

// --- API 调用函数 ---

// 获取股票列表
const fetchStocks = async () => {
  try {
    const response = await fetch('/api/stocks');
    if (!response.ok) throw new Error('获取股票列表失败');
    const data = await response.json();
    stockList.value = data.stocks;
  } catch (error) {
    console.error('获取股票列表失败:', error);
  }
};

// 添加股票
const addStock = async () => {
  if (!newStockTicker.value.trim()) return;
  
  isStockLoading.value = true;
  try {
    const response = await fetch('/api/stocks/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ticker: newStockTicker.value.toUpperCase().trim(),
        is_active: true,
        notes: newStockNotes.value.trim() || null
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || '添加股票失败');
    }
    
    // 重新获取股票列表和状态
    await fetchStocks();
    await fetchStatus();
    
    // 清空输入框
    newStockTicker.value = '';
    newStockNotes.value = '';
    showAddStock.value = false;
  } catch (error) {
    console.error('添加股票失败:', error);
    alert('添加股票失败: ' + error.message);
  } finally {
    isStockLoading.value = false;
  }
};

// 删除股票
const removeStock = async (ticker) => {
  if (!confirm(`确定要删除股票 ${ticker} 吗？`)) return;
  
  isStockLoading.value = true;
  try {
    const response = await fetch(`/api/stocks/${ticker}`, {
      method: 'DELETE'
    });
    
    if (!response.ok) throw new Error('删除股票失败');
    
    // 重新获取股票列表和状态
    await fetchStocks();
    await fetchStatus();
  } catch (error) {
    console.error('删除股票失败:', error);
    alert('删除股票失败: ' + error.message);
  } finally {
    isStockLoading.value = false;
  }
};

// 切换股票启用状态
const toggleStock = async (stock) => {
  isStockLoading.value = true;
  try {
    const response = await fetch(`/api/stocks/${stock.ticker}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...stock,
        is_active: !stock.is_active
      })
    });
    
    if (!response.ok) throw new Error('更新股票状态失败');
    
    // 重新获取股票列表和状态
    await fetchStocks();
    await fetchStatus();
  } catch (error) {
    console.error('更新股票状态失败:', error);
    alert('更新股票状态失败: ' + error.message);
  } finally {
    isStockLoading.value = false;
  }
};

// 获取系统状态
const fetchStatus = async () => {
  try {
    const response = await fetch('/api/control/status');
    if (!response.ok) throw new Error('网络响应错误');
    const data = await response.json();
    isRunning.value = data.is_running;
    statusText.value = data.is_running ? '运行中' : '已停止';
    watchlist.value = data.monitoring_watchlist;
  } catch (error) {
    console.error('获取状态失败:', error);
    statusText.value = '获取状态失败 (请确保后端服务已运行)';
  }
};

// 启动监控
const startMonitor = async () => {
  if (isRunning.value) return; // 如果已在运行，则不执行
  isLoading.value = true;
  statusText.value = '正在启动...';
  try {
    const response = await fetch('/api/control/start', { method: 'POST' });
    if (!response.ok) throw new Error('启动请求失败');
    // 请求成功后，我们立即刷新一次状态，而不是等待轮询
    await fetchStatus(); 
  } catch (error) {
    console.error('启动监控失败:', error);
    statusText.value = '启动失败';
  } finally {
    isLoading.value = false;
  }
};

// 停止监控
const stopMonitor = async () => {
  if (!isRunning.value) return; // 如果已停止，则不执行
  isLoading.value = true;
  statusText.value = '正在停止...';
  try {
    const response = await fetch('/api/control/stop', { method: 'POST' });
    if (!response.ok) throw new Error('停止请求失败');
    await fetchStatus();
  } catch (error) {
    console.error('停止监控失败:', error);
    statusText.value = '停止失败';
  } finally {
    isLoading.value = false;
  }
};


// --- 生命周期钩子 ---

// onMounted: 组件加载后执行
onMounted(() => {
  fetchStatus(); // 立即获取一次状态
  fetchStocks(); // 获取股票列表
  // 设置一个定时器，每5秒自动刷新一次状态
  statusInterval = setInterval(fetchStatus, 5000); 
});

// onUnmounted: 组件被销毁前执行 (例如切换到其他页面)
onUnmounted(() => {
  // 清除定时器，防止内存泄漏
  clearInterval(statusInterval); 
});

</script>

<template>
  <main class="dashboard">
    <h2>系统状态</h2>

    <div class="status-card">
      <div class="status-indicator" :class="{ 'running': isRunning, 'stopped': !isRunning }"></div>
      <span class="status-text">{{ statusText }}</span>
    </div>

    <div v-if="watchlist.length > 0" class="watchlist-card">
      <h3>当前监控列表:</h3>
      <ul>
        <li v-for="ticker in watchlist" :key="ticker">{{ ticker }}</li>
      </ul>
    </div>

    <!-- 股票管理卡片 -->
    <div class="stock-management-card">
      <div class="card-header">
        <h3>股票管理</h3>
        <button 
          @click="showAddStock = !showAddStock" 
          class="add-btn"
          :disabled="isStockLoading">
          {{ showAddStock ? '取消' : '添加股票' }}
        </button>
      </div>

      <!-- 添加股票表单 -->
      <div v-if="showAddStock" class="add-stock-form">
        <div class="form-row">
          <input 
            v-model="newStockTicker" 
            placeholder="股票代码 (如: AAPL)" 
            class="stock-input"
            @keyup.enter="addStock"
            :disabled="isStockLoading">
          <input 
            v-model="newStockNotes" 
            placeholder="备注 (可选)" 
            class="notes-input"
            @keyup.enter="addStock"
            :disabled="isStockLoading">
          <button 
            @click="addStock" 
            class="control-btn start-btn"
            :disabled="!newStockTicker.trim() || isStockLoading">
            {{ isStockLoading ? '添加中...' : '确认添加' }}
          </button>
        </div>
      </div>

      <!-- 股票列表 -->
      <div class="stock-list">
        <div v-if="stockList.length === 0" class="empty-state">
          暂无监控股票，点击"添加股票"开始配置
        </div>
        <div v-else>
          <div 
            v-for="stock in stockList" 
            :key="stock.ticker" 
            class="stock-item"
            :class="{ 'inactive': !stock.is_active }">
            <div class="stock-info">
              <span class="stock-ticker">{{ stock.ticker }}</span>
              <span v-if="stock.notes" class="stock-notes">{{ stock.notes }}</span>
            </div>
            <div class="stock-actions">
              <button 
                @click="toggleStock(stock)" 
                class="toggle-btn"
                :class="{ 'active': stock.is_active }"
                :disabled="isStockLoading">
                {{ stock.is_active ? '启用' : '禁用' }}
              </button>
              <button 
                @click="removeStock(stock.ticker)" 
                class="remove-btn"
                :disabled="isStockLoading">
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="controls-card">
        <h3>系统控制</h3>
        <!-- 核心升级：为按钮绑定点击事件和禁用状态 -->
        <button 
          @click="startMonitor" 
          :disabled="isRunning || isLoading" 
          class="control-btn start-btn">
          {{ isLoading && !isRunning ? '启动中...' : '启动监控' }}
        </button>
        <button 
          @click="stopMonitor" 
          :disabled="!isRunning || isLoading" 
          class="control-btn stop-btn">
          {{ isLoading && isRunning ? '停止中...' : '停止监控' }}
        </button>
    </div>
  </main>
</template>

<style scoped>
/* ... (样式部分完全不变) ... */
.dashboard {
  padding: 0 2rem;
}
.status-card {
  display: flex;
  align-items: center;
  background-color: #f5f7fa;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1.2rem;
  margin-bottom: 2rem;
}
.status-indicator {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-right: 1rem;
  animation: pulse 2s infinite;
}
.status-indicator.running {
  background-color: #28a745;
}
.status-indicator.stopped {
  background-color: #dc3545;
  animation: none;
}
.watchlist-card, .controls-card {
    background-color: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}
.watchlist-card ul {
    list-style: none;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
}
.watchlist-card li {
    background-color: #eef;
    padding: 0.5rem 1rem;
    margin: 0.5rem;
    border-radius: 20px;
    font-weight: bold;
}
.control-btn {
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 5px;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    margin-right: 1rem;
    transition: all 0.3s ease;
}
.control-btn:disabled {
    cursor: not-allowed;
    opacity: 0.5;
}
.start-btn {
    background-color: #28a745;
}
.start-btn:hover:not(:disabled) {
    background-color: #218838;
}
.stop-btn {
    background-color: #dc3545;
}
.stop-btn:hover:not(:disabled) {
    background-color: #c82333;
}
/* 股票管理样式 */
.stock-management-card {
    background-color: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.add-btn {
    padding: 0.5rem 1rem;
    border: 2px solid #007bff;
    border-radius: 5px;
    background-color: transparent;
    color: #007bff;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.add-btn:hover:not(:disabled) {
    background-color: #007bff;
    color: white;
}

.add-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.add-stock-form {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 5px;
    margin-bottom: 1rem;
}

.form-row {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.stock-input, .notes-input {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.stock-input {
    flex: 0 0 150px;
    text-transform: uppercase;
}

.notes-input {
    flex: 1;
}

.stock-input:disabled, .notes-input:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
}

.empty-state {
    text-align: center;
    color: #666;
    padding: 2rem;
    font-style: italic;
}

.stock-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border: 1px solid #eee;
    border-radius: 5px;
    margin-bottom: 0.5rem;
    transition: all 0.3s ease;
}

.stock-item:hover {
    background-color: #f8f9fa;
}

.stock-item.inactive {
    opacity: 0.6;
    background-color: #f5f5f5;
}

.stock-info {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.stock-ticker {
    font-weight: bold;
    font-size: 1.1rem;
    color: #333;
}

.stock-notes {
    font-size: 0.9rem;
    color: #666;
    font-style: italic;
}

.stock-actions {
    display: flex;
    gap: 0.5rem;
}

.toggle-btn {
    padding: 0.4rem 0.8rem;
    border: 1px solid #28a745;
    border-radius: 4px;
    background-color: transparent;
    color: #28a745;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.toggle-btn.active {
    background-color: #28a745;
    color: white;
}

.toggle-btn:not(.active) {
    border-color: #6c757d;
    color: #6c757d;
}

.toggle-btn:hover:not(:disabled) {
    background-color: #28a745;
    color: white;
}

.remove-btn {
    padding: 0.4rem 0.8rem;
    border: 1px solid #dc3545;
    border-radius: 4px;
    background-color: transparent;
    color: #dc3545;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.remove-btn:hover:not(:disabled) {
    background-color: #dc3545;
    color: white;
}

.toggle-btn:disabled, .remove-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

@keyframes pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(40, 167, 69, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }
}
</style>