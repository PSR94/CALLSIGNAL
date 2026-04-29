<script lang="ts">
  export let calls: any[] = [];
</script>

<section class="panel p-5">
  <h2 class="mb-4 text-lg font-semibold text-white">Recent calls</h2>
  <div class="overflow-x-auto">
    <table class="min-w-full text-left text-sm text-slate-300">
      <thead class="text-xs uppercase tracking-[0.18em] text-slate-500">
        <tr>
          <th class="py-2">Call</th>
          <th class="py-2">Scenario</th>
          <th class="py-2">State</th>
          <th class="py-2">Intent</th>
          <th class="py-2">QA</th>
        </tr>
      </thead>
      <tbody>
        {#each calls as call}
          <tr class="border-t border-slate-800">
            <td class="py-3 font-medium text-white">{call.call_id}</td>
            <td class="py-3">{call.scenario_id}</td>
            <td class="py-3">{call.state}</td>
            <td class="py-3">{call.current_intent ?? 'unknown'}</td>
            <td class="py-3">{call.quality_score ?? 'n/a'}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</section>
