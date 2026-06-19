<template>
  <div class="container">
    <div class="logo">
      <a-image
        src="/logo.svg"
        width="30"
        :style="{ boxShadow: '0 2px 8px rgba(0, 0, 0, 0.5)' }"
      />
      <div class="logo-text">AgBox</div>
    </div>
    <LoginBanner />
    <div class="content">
      <div class="content-inner">
        <LoginForm />
      </div>
      <div class="footer">
        <Footer />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import Footer from '@/components/footer/index.vue';
  import NProgress from 'nprogress';
  import { onMounted } from 'vue';
  import LoginForm from './components/login-form.vue';
  import LoginBanner from './components/banner.vue';

  onMounted(() => {
    NProgress.done();
  });
</script>

<style lang="less" scoped>
  .container {
    display: flex;
    height: 100vh;

    .banner {
      width: 550px;
      background: linear-gradient(163.85deg, #ff0099, #00ccff);
    }

    .content {
      position: relative;
      display: flex;
      flex: 1;
      align-items: center;
      justify-content: center;
      padding-bottom: 40px;
    }

    .footer {
      position: absolute;
      right: 0;
      bottom: 0;
      width: 100%;
    }
  }

  .logo {
    position: fixed;
    top: 24px;
    left: 22px;
    z-index: 1;
    display: inline-flex;
    align-items: center;

    &-text {
      margin-right: 4px;
      margin-left: 10px;
      color: var(--color-fill-1);
      font-size: 24px;
      font-weight: bolder;
    }
  }
</style>

<style lang="less" scoped>
  @media (max-width: @screen-lg) {
    .container {
      .banner {
        width: 25%;
      }
    }
  }
</style>
