<template>
  <div class="container">
    <Breadcrumb
      v-if="props.robotImport === false && props.robot === ''"
      :items="['menu.skills']"
    />
    <div class="layout">
      <div class="layout-left-side" :resize-directions="['right']">
        <CategoryItems
          v-model:selected-category-items="selectedCategoryItems"
          :robot="props.robot"
        />
      </div>
      <div class="layout-content">
        <SkillsTable
          :selected-category-items="selectedCategoryItems"
          :robot="props.robot"
          :robot-import="props.robotImport"
          :robot-import-category="props.robotImportCategory"
          :robot-import-robot="props.robotImportRobot"
          @close="emit('close')"
          @refresh="emit('refresh')"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import NProgress from 'nprogress';
  import CategoryItems from './components/category-items.vue';
  import SkillsTable from './components/skills-table.vue';

  const selectedCategoryItems = ref(['#default']);

  const props = withDefaults(
    defineProps<{
      robot: string;
      robotImport: boolean;
      robotImportCategory: string;
      robotImportRobot: string;
    }>(),
    {
      robot: '',
      robotImport: false,
      robotImportCategory: '',
      robotImportRobot: '',
    }
  );

  const emit = defineEmits<{ close: []; refresh: [] }>();

  onMounted(() => {
    NProgress.done();
  });
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }

  .layout {
    display: flex;

    &-left-side {
      flex-basis: 35vh;
      overflow: hidden;
    }

    &-content {
      flex: 1;
      margin: 0 -10px;
    }

    &-right-side {
      flex-basis: 280px;
    }
  }
</style>

<style scoped lang="less">
  @media (max-width: @screen-lg) {
    .layout {
      flex-wrap: wrap;

      &-left-side {
        flex: 1;
        flex-basis: 100%;
        margin-bottom: 16px;
      }

      &-content {
        flex: none;
        flex-basis: 100%;
        order: -1;
        margin-bottom: 16px;
        padding: 0;
      }
    }
  }
</style>
