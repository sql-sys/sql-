<template>
  <div class="empty-state">
    <div class="empty-icon">
      <svg viewBox="0 0 64 64" width="64" height="64">
        <circle cx="32" cy="32" r="30" fill="none" stroke="#e6e6e6" stroke-width="2" />
        <path d="M20 32h24M32 20v24" stroke="#e6e6e6" stroke-width="2" stroke-linecap="round" />
      </svg>
    </div>
    <div class="empty-title">{{ title || '目前无数据' }}</div>
    <div class="empty-description" v-if="description">{{ description }}</div>
    <div class="empty-actions" v-if="$slots.actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  description?: string
}

withDefaults(defineProps<Props>(), {
  title: '目前无数据',
  description: '',
})
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  background: #fafafa;
  border: 1px dashed #e6e6e6;
  border-radius: 8px;
  margin: 20px 0;
  min-height: 300px;
}

.empty-icon {
  margin-bottom: 20px;
  opacity: 0.6;
}

.empty-icon svg {
  width: 80px;
  height: 80px;
}

.empty-title {
  font-size: 18px;
  font-weight: 500;
  color: #666;
  margin-bottom: 8px;
}

.empty-description {
  font-size: 14px;
  color: #999;
  margin-bottom: 20px;
  line-height: 1.5;
}

.empty-actions {
  margin-top: 10px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .empty-state {
    padding: 40px 15px;
    min-height: 250px;
  }

  .empty-icon svg {
    width: 60px;
    height: 60px;
  }

  .empty-title {
    font-size: 16px;
  }

  .empty-description {
    font-size: 13px;
  }
}
</style>
