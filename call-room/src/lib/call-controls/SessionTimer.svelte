<script lang="ts">
  import { onMount } from 'svelte';
  export let startedAt: string | null = null;
  let elapsed = '00:00';

  function tick() {
    if (!startedAt) {
      elapsed = '00:00';
      return;
    }
    const diff = Math.max(0, Date.now() - new Date(startedAt).getTime());
    const minutes = String(Math.floor(diff / 60000)).padStart(2, '0');
    const seconds = String(Math.floor((diff % 60000) / 1000)).padStart(2, '0');
    elapsed = `${minutes}:${seconds}`;
  }

  onMount(() => {
    tick();
    const interval = setInterval(tick, 1000);
    return () => clearInterval(interval);
  });
</script>

<span class="soft-chip">Session {elapsed}</span>
