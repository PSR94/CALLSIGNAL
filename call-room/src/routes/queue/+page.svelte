<script lang="ts">
  import { onMount } from 'svelte';
  import { API_BASE_URL } from '$lib/api/runtime';
  import { liveCallStore } from '$lib/state/liveCallStore';
  import QueuePriorityChip from '$lib/escalation/QueuePriorityChip.svelte';

  onMount(() => liveCallStore.refreshCatalogs());

  async function resolveQueuedCall(callId: string) {
    await fetch(`${API_BASE_URL}/calls/${callId}/resolve`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ resolution_code: 'escalated_resolution', summary: 'Resolved from the escalation queue.' })
    });
    await liveCallStore.refreshCatalogs();
  }
</script>

<section class="panel p-5">
  <div class="mb-4 flex items-center justify-between">
    <div>
      <h1 class="text-2xl font-semibold text-white">Escalation queue</h1>
      <p class="text-sm text-slate-400">Escalated and handoff-ready calls sorted by priority.</p>
    </div>
  </div>
  <div class="space-y-3">
    {#each $liveCallStore.escalationQueue as item}
      <article class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div class="text-sm font-semibold text-white">{item.call_id}</div>
            <div class="text-xs uppercase tracking-[0.18em] text-slate-500">{item.recommended_queue}</div>
          </div>
          <QueuePriorityChip priority={item.priority} />
        </div>
        <div class="mt-3 flex flex-wrap gap-2 text-xs text-slate-300">
          {#each item.reason as reason}
            <span class="rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1">{reason}</span>
          {/each}
        </div>
        <div class="mt-4 flex justify-end">
          <button class="rounded-2xl border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-semibold text-slate-100" on:click={() => resolveQueuedCall(item.call_id)}>Resolve call</button>
        </div>
        {#if item.handoff_packet}
          <pre class="mt-3 overflow-auto rounded-xl bg-slate-900 p-3 text-xs text-slate-200">{JSON.stringify(item.handoff_packet, null, 2)}</pre>
        {/if}
      </article>
    {/each}
  </div>
</section>
