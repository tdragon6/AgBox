<template>
  <div class="login-form-wrapper">
    <div class="login-form-title">{{ $t('login.form.title') }}</div>
    <div class="login-form-sub-title">{{ $t('login.form.subTitle') }}</div>
    <a-form
      ref="loginForm"
      :model="loginFormModel"
      class="login-form"
      layout="vertical"
      @submit="login"
    >
      <a-form-item field="username" hide-label required>
        <a-input
          v-model="loginFormModel.username"
          :placeholder="$t('login.form.userName.placeholder')"
          allow-clear
        >
          <template #prefix>
            <icon-user />
          </template>
        </a-input>
      </a-form-item>
      <a-form-item field="password" required hide-label>
        <a-input-password
          v-model="loginFormModel.password"
          :placeholder="$t('login.form.password.placeholder')"
          allow-clear
        >
          <template #prefix>
            <icon-lock />
          </template>
        </a-input-password>
      </a-form-item>
      <a-space :size="16" direction="vertical">
        <a-button
          type="primary"
          html-type="submit"
          long
          :loading="loginLoading"
        >
          {{ $t('login.form.login') }}
        </a-button>
      </a-space>
    </a-form>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { Message } from '@arco-design/web-vue';
  import { useI18n } from 'vue-i18n';
  import { useUserStore } from '@/store';

  const router = useRouter();
  const { t } = useI18n();
  const userStore = useUserStore();

  const loginLoading = ref(false);

  const loginFormModel = ref({
    username: '',
    password: '',
  });

  const login = async () => {
    loginLoading.value = true;
    try {
      await userStore.login(loginFormModel.value);
      const { redirect, ...othersQuery } = router.currentRoute.value.query;
      router.push({
        name: (redirect as string) || 'Workplace',
        query: {
          ...othersQuery,
        },
      });
      Message.success(t('login.form.login.success'));

      loginFormModel.value.username = '';
      loginFormModel.value.password = '';
    } catch (_) {
      /* eslint-disable no-empty */
    } finally {
      loginLoading.value = false;
    }
  };
</script>

<style lang="less" scoped>
  .login-form {
    &-wrapper {
      width: 320px;
    }

    &-title {
      color: var(--color-text-1);
      font-weight: 500;
      font-size: 24px;
      line-height: 32px;
      margin-bottom: 5px;
    }

    &-sub-title {
      color: var(--color-text-3);
      font-size: 16px;
      line-height: 24px;
      margin-bottom: 16px;
    }
  }
</style>
