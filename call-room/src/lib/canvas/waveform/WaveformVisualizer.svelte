<script lang="ts">
  export let active = false;
  const bars = [18, 42, 28, 56, 22, 64, 30, 46, 24, 52, 20, 60];
</script>

<section class="panel p-5">
  <div class="mb-3 flex items-center justify-between">
    <div>
      <h2 class="text-lg font-semibold text-white">Signal waveform</h2>
      <p class="text-sm text-slate-400">Visual pulse for the current call session.</p>
    </div>
    <span class="soft-chip">{active ? 'live' : 'idle'}</span>
  </div>
  <div class="flex h-28 items-end gap-2 rounded-3xl border border-slate-800 bg-slate-950/80 p-4">
    {#each bars as height, index}
      <span class={`w-full rounded-full transition-all duration-300 ${active ? 'bg-gradient-to-t from-cyan-500 via-emerald-400 to-amber-300' : 'bg-slate-700'}`} style={`height:${active ? height + (index % 3) * 8 : 12}px; opacity:${active ? 0.9 : 0.45}`}></span>
    {/each}
  </div>
</section>
