<script lang="ts">
  import { onMount } from 'svelte';
  import { downloadReport } from '$lib/api/reportApi';
  import { API_BASE_URL } from '$lib/api/runtime';

  export let data: { callId: string };
  let report: any = null;
  let markdown = '';
  let exportStatus = '';

  onMount(async () => {
    const response = await fetch(`${API_BASE_URL}/calls/${data.callId}/report`);
    report = await response.json();
    markdown = await downloadReport(data.callId, 'markdown');
  });

  async function exportJson() {
    exportStatus = 'exporting';
    const response = await fetch(`${API_BASE_URL}/calls/${data.callId}/report/export`, { method: 'POST' });
    await response.json();
    exportStatus = 'exported';
  }
</script>

<section class="panel p-5">
  <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
    <div>
      <h1 class="text-2xl font-semibold text-white">Call review</h1>
      <p class="text-sm text-slate-400">Audit-style review for {data.callId}.</p>
    </div>
    <div class="flex items-center gap-3">
      {#if exportStatus}
        <span class="soft-chip">{exportStatus}</span>
      {/if}
      <button class="rounded-2xl border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-semibold text-slate-100" on:click={exportJson}>Export review report</button>
    </div>
  </div>
  {#if report}
    <div class="grid gap-4 xl:grid-cols-2">
      <div class="space-y-4">
        <article class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4">
          <h2 class="mb-2 text-sm uppercase tracking-[0.22em] text-slate-500">Call summary</h2>
          <p class="text-sm leading-6 text-slate-200">{report.summary}</p>
          <div class="mt-4 grid gap-3 sm:grid-cols-2">
            <div><div class="text-xs uppercase tracking-[0.18em] text-slate-500">Intent</div><div class="mt-1 text-white">{report.current_intent}</div></div>
            <div><div class="text-xs uppercase tracking-[0.18em] text-slate-500">QA score</div><div class="mt-1 text-white">{report.quality.score}</div></div>
            <div><div class="text-xs uppercase tracking-[0.18em] text-slate-500">Resolution code</div><div class="mt-1 text-white">{report.resolution_code}</div></div>
            <div><div class="text-xs uppercase tracking-[0.18em] text-slate-500">Escalation</div><div class="mt-1 text-white">{report.signals.escalation.reasons.join(', ') || 'none'}</div></div>
          </div>
        </article>
        <article class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4">
          <h2 class="mb-2 text-sm uppercase tracking-[0.22em] text-slate-500">Extracted fields</h2>
          <div class="space-y-2 text-sm text-slate-300">
            {#each report.signals.fields as field}
              <div class="rounded-2xl border border-slate-800 bg-slate-900/80 p-3">
                <div class="text-xs uppercase tracking-[0.18em] text-slate-500">{field.field_name}</div>
                <div class="mt-1 text-white">{field.value}</div>
              </div>
            {/each}
          </div>
        </article>
        <article class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4">
          <h2 class="mb-2 text-sm uppercase tracking-[0.22em] text-slate-500">Redacted transcript</h2>
          <div class="space-y-2 text-sm text-slate-300">
            {#each report.transcript as turn}
              <div class="rounded-2xl border border-slate-800 bg-slate-900/80 p-3">
                <div class="text-xs uppercase tracking-[0.18em] text-slate-500">{turn.speaker}</div>
                <div class="mt-1 text-white">{turn.redacted_text}</div>
              </div>
            {/each}
          </div>
        </article>
      </div>
      <div class="space-y-4">
        <article class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4">
          <h2 class="mb-2 text-sm uppercase tracking-[0.22em] text-slate-500">Timeline</h2>
          <pre class="max-h-[26rem] overflow-auto rounded-2xl bg-slate-950 p-4 text-xs text-slate-200">{JSON.stringify(report.timeline, null, 2)}</pre>
        </article>
        <article class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4">
          <h2 class="mb-2 text-sm uppercase tracking-[0.22em] text-slate-500">Markdown export</h2>
          <pre class="max-h-[26rem] overflow-auto rounded-2xl bg-slate-950 p-4 text-xs text-slate-200">{markdown}</pre>
        </article>
      </div>
    </div>
  {:else}
    <p class="text-sm text-slate-500">Loading report...</p>
  {/if}
</section>
