import { nextTick } from 'vue';

// 数字员工等级颜色
export const robotsRankColor: Record<string, string> = {
  L1: 'blue',
  L2: 'blue',
  L3: 'cyan',
  L4: 'cyan',
  L5: 'magenta',
  L6: 'magenta',
  L7: 'pinkpurple',
  L8: 'pinkpurple',
  L9: 'orangered',
};

// 数字员工品质颜色
export const robotsQualityColor: Record<string, string> = {
  common: 'blue',
  uncommon: 'cyan',
  rare: 'pinkpurple',
  epic: 'magenta',
  legendary: 'orangered',
};

// 数字员工推理程度颜色
export const robotsReasoningEffortColor: Record<string, string> = {
  none: 'gray',
  minimal: 'blue',
  low: 'cyan',
  medium: 'magenta',
  high: 'pinkpurple',
  xhigh: 'orangered',
};

// 任务类型颜色
export const tasksTypeColor: Record<string, string> = {
  'session': 'arcoblue',
  'agbox-coordinator-sync': 'magenta',
  'agbox-coordinator-async': 'orangered',
};

// 协调器名称
export const coordinatorName: Record<string, string> = {
  'agbox-coordinator-sync': 'tasks.coordinator.sync',
  'agbox-coordinator-async': 'tasks.coordinator.async',
};

// 任务优先级颜色
export const tasksPriorityColor: Record<string, string> = {
  P1: 'orangered',
  P2: 'magenta',
  P3: 'cyan',
  P4: 'blue',
};

// 任务状态颜色
export const tasksStatusColor: Record<string, string> = {
  pending: 'blue',
  running: 'cyan',
  finished: 'green',
  interrupted: 'orangered',
  failed: 'red',
};

// 任务触发者颜色
export const tasksTriggerColor: Record<string, string> = {
  user: 'cyan',
  scheduler: 'orangered',
};

// 收件箱通知类型颜色
export const inboxTypeColor: Record<string, string> = {
  tasks: 'arcoblue',
  upgrade: 'orangered',
};

// 收件箱任务/升级状态颜色
export const inboxStatusColor: Record<string, string> = {
  finished: tasksStatusColor.finished,
  interrupted: tasksStatusColor.interrupted,
  failed: tasksStatusColor.failed,
  rank: 'arcoblue',
  quality: 'magenta',
};

// 检查 title 是否超出宽度
export function checkTitleOverflow(e: MouseEvent, item: Record<string, any>) {
  const el = e.currentTarget as HTMLElement;
  item.overflow = el.scrollWidth > el.clientWidth;
}

// 任务消息角色颜色
export const tasksMessagesRoleColor: Record<string, string> = {
  user: 'cyan',
  tool: 'orangered',
  assistant: 'magenta',
};

// 切换重命名输入框
export async function switchRenameInput(
  item: Record<string, any>,
  focusNode: string
) {
  item.input = true;
  await nextTick();
  const openedCategoryInput = document.querySelector(
    focusNode
  ) as HTMLInputElement;
  openedCategoryInput?.focus();
}

// 模型消耗字段映射
export const ModelCostKeysMap: Record<string, string> = {
  inputTokens: 'input_tokens',
  outputTokens: 'output_tokens',
  cacheReadTokens: 'cache_read_tokens',
  cacheWriteTokens: 'cache_write_tokens',
  reasoningTokens: 'reasoning_tokens',
  estimatedCostUsd: 'estimated_cost_usd',
  actualCostUsd: 'actual_cost_usd',
};

// 访问 URL
export const visitUrl = (url: string) => {
  window.open(url, '_blank');
};
