<script lang="ts">
  import { onMount } from 'svelte';
  import { liveCallStore } from '$lib/state/liveCallStore';

  onMount(() => liveCallStore.refreshCatalogs());
</script>

<section class="panel p-5">
  <div class="mb-4 flex items-center justify-between gap-3">
    <div>
      <h1 class="text-2xl font-semibold text-white">Call review</h1>
      <p class="text-sm text-slate-400">Choose a call from the seeded history and open its audit trail.</p>
    </div>
  </div>
  <div class="grid gap-3">
    {#each $liveCallStore.recentCalls as call}
      <a class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4 hover:border-cyan-500/40" href={`/review/${call.call_id}`}>
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
