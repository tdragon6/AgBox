import { DirectiveBinding } from 'vue';

export default {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const delay = binding.value || 300;
    let timer: ReturnType<typeof setTimeout> | null = null;
    el.addEventListener('click', () => {
      if (timer) return;
      el.style.pointerEvents = 'none';
      timer = setTimeout(() => {
        el.style.pointerEvents = '';
        timer = null;
      }, delay);
    });
  },
};
