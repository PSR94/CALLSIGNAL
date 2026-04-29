<script lang="ts">
  export let escalation: any = null;
  export let handoffPacket: any = null;
</script>

<section class="panel p-5">
  <div class="mb-4 flex items-center justify-between">
    <div>
      <h2 class="text-lg font-semibold text-white">Escalation lane</h2>
      <p class="text-sm text-slate-400">Rules, priority, and the handoff packet that would go to a supervisor.</p>
    </div>
    {#if escalation?.priority}
      <span class="soft-chip">{escalation.priority}</span>
    {/if}
  </div>
  <div class="grid gap-4 lg:grid-cols-2">
    <div class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4 text-sm text-slate-300">
      <h3 class="mb-2 text-xs uppercase tracking-[0.22em] text-slate-500">Reasons</h3>
      <div class="flex flex-wrap gap-2">
        {#if escalation?.reasons?.length}
          {#each escalation.reasons as reason}
            <span class="rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-200">{reason}</span>
          {/each}
        {:else}
          <span class="text-slate-500">No escalation triggered yet.</span>
        {/if}
      </div>
    </div>
    <div class="rounded-2xl border border-slate-800 bg-slate-950/90 p-4 text-sm text-slate-300">
      <h3 class="mb-2 text-xs uppercase tracking-[0.22em] text-slate-500">Handoff packet</h3>
      {#if handoffPacket}
        <pre class="max-h-64 overflow-auto whitespace-pre-wrap rounded-xl bg-slate-900/90 p-3 text-xs text-slate-200">{JSON.stringify(handoffPacket, null, 2)}</pre>
      {:else}
        <p class="text-slate-500">The backend will generate a redacted packet when escalation conditions are met.</p>
      {/if}
    </div>
  </div>
</section>
