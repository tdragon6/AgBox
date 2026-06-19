<template>
  <div class="container">
    <Breadcrumb :items="['menu.inbox']" />
    <div class="layout">
      <div class="layout-left-side" :resize-directions="['right']">
        <InboxItems
          v-model:selected-robots-names="selectedRobotsNames"
          scope="inbox"
        />
      </div>
      <div class="layout-content">
        <InboxTable
          :selected-robot="
            selectedRobotsNames.length !== 0 ? selectedRobotsNames[0] : ''
          "
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import NProgress from 'nprogress';
  import InboxItems from './components/inbox-items.vue';
  import InboxTable from './components/inbox-table.vue';

  const route = useRoute();

  const selectedRobotsNames = ref(
    route.query.robot !== undefined ? [route.query.robot as string] : []
  );

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
