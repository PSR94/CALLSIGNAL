<script lang="ts">
  export let quality: any = null;
</script>

<section class="panel p-5">
  <div class="mb-4 flex items-center justify-between">
    <div>
      <h2 class="text-lg font-semibold text-white">QA scorecard</h2>
      <p class="text-sm text-slate-400">Deterministic rubric scoring from the current call timeline.</p>
    </div>
    {#if quality}
      <span class="soft-chip">{quality.score}%</span>
    {/if}
  </div>
  {#if quality}
    <div class="grid gap-4 lg:grid-cols-2">
      <div class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4">
        <h3 class="mb-2 text-xs uppercase tracking-[0.22em] text-slate-500">Pass / fail</h3>
        <p class="text-2xl font-semibold text-white">{quality.passed ? 'Passed' : 'Needs attention'}</p>
        <p class="mt-2 text-sm text-slate-400">Score {quality.score}% · evidence turns {quality.evidence_turns.join(', ')}</p>
      </div>
      <div class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4">
        <h3 class="mb-2 text-xs uppercase tracking-[0.22em] text-slate-500">Missed items</h3>
        <div class="flex flex-wrap gap-2">
          {#each quality.missed_rubric_items as item}
            <span class="rounded-full border border-rose-500/30 bg-rose-500/10 px-3 py-1 text-xs font-semibold text-rose-200">{item}</span>
          {/each}
        </div>
      </div>
    </div>
  {:else}
    <p class="text-sm text-slate-500">Start a call to calculate the rubric score.</p>
  {/if}
</section>
