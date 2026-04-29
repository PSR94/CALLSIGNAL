<script lang="ts">
  export let summary: any = null;
</script>

<div class="signal-grid">
  {#each [
    ['Total calls', summary?.total_calls ?? 0],
    ['Active calls', summary?.active_calls ?? 0],
    ['Escalated calls', summary?.escalated_calls ?? 0],
    ['QA average', summary?.qa_average ?? 0]
  ] as [label, value]}
    <article class="panel p-5">
      <div class="text-xs uppercase tracking-[0.2em] text-slate-500">{label}</div>
      <div class="mt-3 text-3xl font-semibold text-white">{value}</div>
    </article>
  {/each}
</div>
