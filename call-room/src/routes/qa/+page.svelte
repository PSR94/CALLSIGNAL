<script lang="ts">
  import { onMount } from 'svelte';
  import { liveCallStore } from '$lib/state/liveCallStore';
  import RubricScorecard from '$lib/qa/RubricScorecard.svelte';
  import MissedItemsList from '$lib/qa/MissedItemsList.svelte';
  import CoachingNotes from '$lib/qa/CoachingNotes.svelte';

  onMount(() => liveCallStore.refreshCatalogs());
</script>

<div class="grid gap-4 xl:grid-cols-2">
  <RubricScorecard quality={$liveCallStore.quality} />
  <div class="space-y-4">
    <section class="panel p-5">
      <h2 class="mb-3 text-lg font-semibold text-white">Score distribution</h2>
      <div class="grid grid-cols-5 gap-2 text-center text-xs uppercase tracking-[0.18em] text-slate-400">
        {#each [60, 70, 80, 90, 100] as bucket}
          <div class="rounded-2xl border border-slate-800 bg-slate-950/90 p-3">
            <div class="text-lg font-semibold text-white">{$liveCallStore.recentCalls.filter((call) => (call.quality_score ?? 0) >= bucket && (call.quality_score ?? 0) < bucket + 10).length}</div>
            <div class="mt-1 text-slate-500">{bucket}s</div>
          </div>
        {/each}
      </div>
    </section>
    <MissedItemsList items={$liveCallStore.quality?.missed_rubric_items ?? []} />
    <CoachingNotes notes={$liveCallStore.quality?.coaching_notes ?? []} />
    <section class="panel p-5">
      <h2 class="mb-3 text-lg font-semibold text-white">Call samples</h2>
      <div class="space-y-2 text-sm text-slate-300">
        {#each $liveCallStore.recentCalls.slice(0, 5) as call}
          <div class="rounded-2xl border border-slate-800 bg-slate-950/90 p-3">
            <div class="font-semibold text-white">{call.call_id}</div>
            <div class="text-xs uppercase tracking-[0.18em] text-slate-500">{call.scenario_id} · {call.state} · score {call.quality_score ?? 'n/a'}</div>
          </div>
        {/each}
      </div>
    </section>
  </div>
</div>
