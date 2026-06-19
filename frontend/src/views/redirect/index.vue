<template>
  <div></div>
</template>

<script setup lang="ts">
  import { useRouter, useRoute } from 'vue-router';

  const router = useRouter();
  const route = useRoute();

  const gotoPath = route.params.path as string;

  router.replace({ path: gotoPath });
</script>

<style scoped lang="less"></style>
