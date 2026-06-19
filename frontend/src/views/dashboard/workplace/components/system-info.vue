<template>
  <a-card style="min-height: 360px">
    <template #title>
      {{ $t('dashboard.systemInfo') }}
      <a-tooltip :content="$t('common.refresh')">
        <icon-refresh
          v-debounce
          class="custom-icon-button"
          @click="getSystemInfo"
        />
      </a-tooltip>
    </template>
    <a-spin :loading="systemInfoLoading">
      <a-form
        :model="systemInfo"
        :label-col-props="{ span: 8 }"
        :wrapper-col-props="{ span: 16 }"
        label-align="left"
      >
        <a-row>
          <a-col :span="24">
            <a-form-item field="version" :label="$t('dashboard.version')">
              <a-tag color="arcoblue">{{ systemInfo.version }}</a-tag>
            </a-form-item>
          </a-col>
          <a-col :span="24">
            <a-form-item field="address" :label="$t('dashboard.address')">
              <a-tag color="green">{{ systemInfo.address }}</a-tag>
            </a-form-item>
          </a-col>
          <a-col :span="24">
            <a-form-item field="cpuPercent" :label="$t('dashboard.cpuPercent')">
              <a-tag color="orangered">{{ systemInfo.cpuPercent }}</a-tag>
            </a-form-item>
          </a-col>
          <a-col :span="24">
            <a-form-item field="memory" :label="$t('dashboard.memory')">
              <a-tag color="magenta">{{ systemInfo.memory }}</a-tag>
            </a-form-item>
          </a-col>
          <a-col :span="24">
            <a-form-item field="disk" :label="$t('dashboard.disk')">
              <a-tag color="purple">{{ systemInfo.disk }}</a-tag>
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
    </a-spin>
  </a-card>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { apiGetSystemInfo } from '@/api/settings';

  const systemInfoLoading = ref(false);

  const systemInfo = ref<Record<string, any>>({
    version: '',
    cpuPercent: '',
    memory: '',
    disk: '',
    address: '',
  });

  const getSystemInfo = async () => {
    systemInfoLoading.value = true;
    try {
      const { data } = await apiGetSystemInfo();
      systemInfo.value.version = data.version;
      systemInfo.value.address = `${data.host}:${data.port}`;
      systemInfo.value.cpuPercent = `${data.cpu_percent}%`;
      systemInfo.value.memory = `${data.memory_used.toFixed(
        2
      )} GB / ${data.memory_total.toFixed(2)} GB`;
      systemInfo.value.disk = `${data.disk_used.toFixed(
        2
      )} GB / ${data.disk_total.toFixed(2)} GB`;
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      systemInfoLoading.value = false;
    }
  };

  onMounted(() => {
    getSystemInfo();
  });
</script>
