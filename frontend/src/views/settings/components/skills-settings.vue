<template>
  <a-card :title="$t('skills')" style="min-height: 33vh">
    <a-form
      :model="skillsSettingsModelForm"
      label-align="left"
      :label-col-props="{ span: 10 }"
      :wrapper-col-props="{ span: 14 }"
    >
      <a-form-item field="overwrite" :label="$t('settings.skills.overwrite')">
        <a-space
          style="display: flex; justify-content: space-between; width: 100%"
        >
          <a-select
            v-model="skillsSettingsModelForm.overwrite"
            :options="skillsSettingsOverwriteOptions"
            :placeholder="$t('settings.skills.overwrite.select.placeholder')"
            allow-clear
          >
            <template #label="{ data }">
              <a-badge
                :text="$t(data.label)"
                :status="
                  data.value === true
                    ? 'success'
                    : data.value === false
                    ? 'normal'
                    : 'danger'
                "
              />
            </template>
            <template #option="{ data }">
              <a-badge
                :text="$t(data.label)"
                :status="
                  data.value === true
                    ? 'success'
                    : data.value === false
                    ? 'normal'
                    : 'danger'
                "
              />
            </template>
          </a-select>
          <a-button
            v-debounce
            type="primary"
            size="small"
            :loading="overwriteSettingsLoading"
            @click="
              async () => {
                overwriteSettingsLoading = true;
                await setSettings(
                  'SKILLS_OVERWRITE',
                  skillsSettingsModelForm.overwrite,
                  skillsSettingsDefaultValue.overwrite,
                  $t('common.save.success')
                );
                overwriteSettingsLoading = false;
              }
            "
          >
            {{ $t('common.save') }}
          </a-button>
        </a-space>
      </a-form-item>
      <a-form-item
        field="formatCheck"
        :label="$t('settings.skills.formatCheck')"
      >
        <a-space
          style="display: flex; justify-content: space-between; width: 100%"
        >
          <a-switch
            v-model="skillsSettingsModelForm.formatCheck"
            type="round"
          />
          <a-button
            v-debounce
            type="primary"
            size="small"
            :loading="formatCheckSettingsLoading"
            @click="
              async () => {
                formatCheckSettingsLoading = true;
                await setSettings(
                  'SKILLS_FORMAT_CHECK',
                  skillsSettingsModelForm.formatCheck,
                  skillsSettingsDefaultValue.formatCheck,
                  $t('common.save.success')
                );
                formatCheckSettingsLoading = false;
              }
            "
          >
            {{ $t('common.save') }}
          </a-button>
        </a-space>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup lang="ts">
  import { ref, computed, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { getSettings, setSettings } from '@/views/settings/utils/settings';

  const { t } = useI18n();

  const skillsSettingsDefaultValue: Record<string, any> = {
    overwrite: 'intercept',
    formatCheck: true,
  };

  const skillsSettingsModelForm = ref<Record<string, any>>({
    overwrite: skillsSettingsDefaultValue.overwrite,
    formatCheck: skillsSettingsDefaultValue.formatCheck,
  });

  const overwriteSettingsLoading = ref(false);
  const formatCheckSettingsLoading = ref(false);

  const skillsSettingsOverwriteOptions = computed<Record<string, any>[]>(() => [
    {
      label: t('common.true'),
      value: true,
    },
    {
      label: t('common.false'),
      value: false,
    },
    {
      label: t('common.intercept'),
      value: 'intercept',
    },
  ]);

  onMounted(async () => {
    overwriteSettingsLoading.value = true;
    formatCheckSettingsLoading.value = true;
    skillsSettingsModelForm.value.overwrite = await getSettings(
      'SKILLS_OVERWRITE',
      skillsSettingsDefaultValue.overwrite
    );
    skillsSettingsModelForm.value.formatCheck = await getSettings(
      'SKILLS_FORMAT_CHECK',
      skillsSettingsDefaultValue.formatCheck
    );
    overwriteSettingsLoading.value = false;
    formatCheckSettingsLoading.value = false;
  });
</script>
