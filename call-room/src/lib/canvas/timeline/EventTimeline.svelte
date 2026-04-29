<script lang="ts">
  export let events: any[] = [];
</script>

<section class="panel p-5">
  <div class="mb-4 flex items-center justify-between">
    <div>
      <h2 class="text-lg font-semibold text-white">Event timeline</h2>
      <p class="text-sm text-slate-400">Sequence-ordered call events from the backend event log.</p>
    </div>
    <span class="soft-chip">{events.length} events</span>
  </div>
  <div class="space-y-2">
    {#if events.length === 0}
      <div class="rounded-2xl border border-dashed border-slate-700 p-5 text-sm text-slate-500">The timeline will populate as soon as the call stream starts.</div>
    {:else}
      {#each events as event}
        <div class="flex items-center gap-3 rounded-2xl border border-slate-800 bg-slate-950/80 px-4 py-3 text-sm">
          <span class="soft-chip">#{event.sequence}</span>
          <span class="font-medium text-white">{event.event_type}</span>
          <span class="text-slate-500">{event.timestamp}</span>
        </div>
      {/each}
    {/if}
  </div>
</section>
