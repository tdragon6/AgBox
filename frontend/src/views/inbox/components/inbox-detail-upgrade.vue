<template>
  <div>
    <a-space class="header" direction="vertical">
      <span class="crown">LEVEL UP</span>
      <Media
        class="avatar-ring"
        :style="{
          backgroundColor: 'var(--color-bg-2)',
        }"
        :size="100"
        :url="
          apiGetRobotsManageAvatarUrl({ name: props.selectedInboxItem.robot })
        "
        scope="avatar"
      />
      <span class="robot-name">
        {{ props.selectedInboxItem.robot }}
      </span>
      <a-space>
        <a-tag
          class="status-tag"
          :color="inboxStatusColor[props.selectedInboxItem.status]"
        >
          {{ $t(`robots.${props.selectedInboxItem.status}`) }}
        </a-tag>
        <a-tag
          class="status-tag"
          :color="
            props.selectedInboxItem.status === 'rank'
              ? robotsRankColor[props.selectedInboxItem.result]
              : robotsQualityColor[props.selectedInboxItem.result]
          "
        >
          {{
            props.selectedInboxItem.status === 'rank'
              ? props.selectedInboxItem.result
              : $t(`robots.quality.${props.selectedInboxItem.result}`)
          }}
        </a-tag>
      </a-space>
    </a-space>
    <div class="content">
      <div class="title-block">
        <h1 class="title-main"> 🎉 {{ $t('inbox.upgrade.title') }} </h1>
        <p class="title-sub">{{ $t('inbox.upgrade.subtitle') }}</p>
      </div>
      <div class="level-transition">
        <div class="level-box old">
          <div class="level-label">BEFORE</div>
          <div class="level-num">
            {{
              props.selectedInboxItem.status === 'rank'
                ? getPreviousLevel()
                : $t(`robots.quality.${getPreviousLevel()}`)
            }}
          </div>
        </div>
        <div class="arrow">
          <icon-right class="arrow-icon" />
        </div>
        <div class="level-box new">
          <div class="level-label">NOW</div>
          <div class="level-num highlight">
            {{
              props.selectedInboxItem.status === 'rank'
                ? props.selectedInboxItem.result
                : $t(`robots.quality.${props.selectedInboxItem.result}`)
            }}
          </div>
        </div>
      </div>
    </div>
    <a-typography-text type="secondary" class="footer">
      {{
        dayjs(props.selectedInboxItem.updated_time).format(
          'YYYY-MM-DD HH:mm:ss'
        )
      }}
    </a-typography-text>
  </div>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue';
  import { useFireworks } from '@/utils/fireworks';
  import { apiGetRobotsManageAvatarUrl } from '@/api/robots/manage';
  import {
    robotsRankColor,
    robotsQualityColor,
    inboxStatusColor,
  } from '@/utils/func';
  import dayjs from 'dayjs';
  import Media from '@/components/media/index.vue';

  const props = defineProps<{
    selectedInboxItem: Record<string, any>;
  }>();

  const { fire, fireSides, fireRing } = useFireworks();

  const getPreviousLevel = () => {
    let levelItem = {};
    if (props.selectedInboxItem.status === 'rank') {
      levelItem = robotsRankColor;
    } else {
      levelItem = robotsQualityColor;
    }
    const keys = Object.keys(levelItem);
    const idx = keys.indexOf(props.selectedInboxItem.result);
    return keys[idx - 1];
  };

  onMounted(() => {
    fire();
    setTimeout(() => fireSides(), 300);
    setTimeout(() => fireRing(), 800);
    setTimeout(() => fireSides(), 1200);
  });
</script>

<style scoped>
  .header {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 320px;
    border-radius: 10px;
    background: linear-gradient(135deg, #f6416c 0%, #ff8c42 50%, #fff6b7 100%);
  }
  .crown {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 16px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 999px;
    color: #ff6b00;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 2px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    animation: badge-bounce 1.5s ease-in-out infinite;
    margin-bottom: 6px;
  }
  @keyframes badge-bounce {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-4px);
    }
  }

  .avatar-ring {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 130px;
    height: 130px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(10px);
    border: 3px solid rgba(255, 255, 255, 0.6);
    animation: ring-pulse 2s ease-in-out infinite;
  }
  @keyframes ring-pulse {
    0%,
    100% {
      box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.5),
        0 0 30px rgba(255, 234, 0, 0.5);
    }
    50% {
      box-shadow: 0 0 0 12px rgba(255, 255, 255, 0),
        0 0 50px rgba(255, 234, 0, 0.8);
    }
  }

  .robot-name {
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }

  .status-tag {
    font-weight: 600;
    font-size: 13px;
    padding: 4px 12px;
  }

  .content {
    position: relative;
    z-index: 1;
    padding: 72px;
    background: var(--color-bg-1);
  }

  .title-block {
    text-align: center;
    margin-bottom: 24px;
  }
  .title-main {
    margin: 0;
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg, #f6416c, #ff8c42, #ffaa00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: title-shine 3s ease-in-out infinite;
  }
  .title-sub {
    margin-top: 16px;
    color: var(--color-text-2);
    font-size: 14px;
  }

  .level-transition {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 24px;
    margin-bottom: 28px;
    margin-top: 32px;
  }
  .level-box {
    text-align: center;
    padding: 12px 28px;
    border-radius: 12px;
    background: var(--color-fill-2);
    min-width: 100px;
  }
  .level-box.new {
    background: linear-gradient(135deg, #f6416c20, #ffaa0020);
    border: 2px solid #ffaa00;
    animation: new-level-pulse 2s ease-in-out infinite;
  }
  @keyframes new-level-pulse {
    0%,
    100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
  }
  .level-label {
    font-size: 11px;
    color: var(--color-text-3);
    letter-spacing: 1.5px;
    margin-bottom: 4px;
  }
  .level-num {
    font-size: 24px;
    font-weight: 700;
    color: var(--color-text-1);
  }
  .level-num.highlight {
    background: linear-gradient(135deg, #f6416c, #ff8c42);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .arrow-icon {
    font-size: 28px;
    color: #ffaa00;
    animation: arrow-move 1.2s ease-in-out infinite;
  }
  @keyframes arrow-move {
    0%,
    100% {
      transform: translateX(0);
    }
    50% {
      transform: translateX(6px);
    }
  }

  .footer {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: 16px;
    border-top: 1px solid var(--color-border-2);
    gap: 6px;
    font-size: 15px;
  }
</style>
