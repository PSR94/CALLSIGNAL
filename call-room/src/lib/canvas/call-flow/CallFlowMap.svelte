<script lang="ts">
  export let state = 'idle';
</script>

<section class="panel p-5">
  <div class="mb-4 flex items-center justify-between">
    <div>
      <h2 class="text-lg font-semibold text-white">Call flow map</h2>
      <p class="text-sm text-slate-400">The current state sits inside the session path.</p>
    </div>
  </div>
  <div class="grid gap-3 sm:grid-cols-5">
    {#each ['idle','connecting','active','handoff_ready','ended'] as node}
      <div class={`rounded-2xl border p-4 text-center text-sm font-semibold uppercase tracking-[0.18em] ${state === node ? 'border-cyan-400 bg-cyan-500/10 text-cyan-200' : 'border-slate-800 bg-slate-950 text-slate-400'}`}>
        {node.replaceAll('_', ' ')}
      </div>
    {/each}
  </div>
</section>
