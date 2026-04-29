<script lang="ts">
  import { onMount } from 'svelte';
  import { supervisorStore } from '$lib/state/supervisorStore';
  import SignalTiles from '$lib/supervisor/SignalTiles.svelte';
  import IntentMixChart from '$lib/supervisor/IntentMixChart.svelte';
  import EscalationTrend from '$lib/supervisor/EscalationTrend.svelte';
  import RecentCallsTable from '$lib/supervisor/RecentCallsTable.svelte';

  onMount(() => supervisorStore.refresh());
</script>

<div class="space-y-4">
  <SignalTiles summary={$supervisorStore.summary} />
  <div class="grid gap-4 xl:grid-cols-2">
    <IntentMixChart rows={$supervisorStore.intentMix} />
    <EscalationTrend rows={$supervisorStore.qualityTrend} />
  </div>
  <RecentCallsTable calls={$supervisorStore.recentCalls} />
</div>
