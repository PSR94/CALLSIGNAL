<script lang="ts">
  import { onMount } from 'svelte';
  import { liveCallStore } from '$lib/state/liveCallStore';

  onMount(() => liveCallStore.refreshCatalogs());
</script>

<section class="panel p-5">
  <h1 class="mb-2 text-2xl font-semibold text-white">Call history</h1>
  <p class="mb-4 text-sm text-slate-400">Synthetic call sessions seeded from the scenario library.</p>
  <div class="space-y-3">
    {#each $liveCallStore.recentCalls as call}
      <a class="block rounded-2xl border border-slate-800 bg-slate-950/90 p-4 hover:border-cyan-500/40" href={`/review/${call.call_id}`}>
        <div class="flex items-center justify-between gap-3">
          <div>
            <div class="font-semibold text-white">{call.call_id}</div>
            <div class="text-sm text-slate-400">{call.scenario_id}</div>
          </div>
          <div class="text-right text-sm text-slate-300">
            <div>{call.state}</div>
            <div class="text-xs uppercase tracking-[0.18em] text-slate-500">score {call.quality_score ?? 'n/a'}</div>
          </div>
        </div>
      </a>
    {/each}
  </div>
</section>
