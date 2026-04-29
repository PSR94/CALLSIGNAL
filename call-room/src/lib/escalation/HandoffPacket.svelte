<script lang="ts">
  export let packet: any = null;
</script>

<section class="panel p-5">
  <div class="mb-3 flex items-center justify-between">
    <div>
      <h2 class="text-lg font-semibold text-white">Handoff packet</h2>
      <p class="text-sm text-slate-400">This is the supervisor-ready summary for the current call.</p>
    </div>
  </div>
  {#if packet}
    <dl class="grid gap-3 text-sm text-slate-300 sm:grid-cols-2">
      <div><dt class="text-slate-500">Priority</dt><dd class="mt-1 font-semibold text-white">{packet.priority}</dd></div>
      <div><dt class="text-slate-500">Recommended queue</dt><dd class="mt-1 font-semibold text-white">{packet.recommended_queue}</dd></div>
      <div class="sm:col-span-2"><dt class="text-slate-500">Call summary</dt><dd class="mt-1 leading-6 text-slate-200">{packet.call_summary}</dd></div>
      <div class="sm:col-span-2"><dt class="text-slate-500">Next best action</dt><dd class="mt-1 leading-6 text-slate-200">{packet.next_best_action}</dd></div>
    </dl>
  {:else}
    <p class="text-sm text-slate-500">No packet yet.</p>
  {/if}
</section>
