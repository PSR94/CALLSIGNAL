<script lang="ts">
  import type { ScenarioDefinition } from '$lib/api/call-contracts';
  import CallStateBadge from './CallStateBadge.svelte';
  import SessionTimer from './SessionTimer.svelte';

  export let state = 'idle';
  export let startedAt: string | null = null;
  export let scenarios: ScenarioDefinition[] = [];
  export let selectedScenario = '';
  export let busy = false;
  export let onStart: (scenarioId: string) => void;
  export let onResolve: () => void;
  export let onEscalate: () => void;
  export let onHandoff: () => void;
  export let onEnd: () => void;
</script>

<section class="panel p-5">
  <div class="flex flex-wrap items-center justify-between gap-4">
    <div>
      <div class="mb-2 flex items-center gap-3">
        <CallStateBadge {state} />
        <SessionTimer {startedAt} />
      </div>
      <h1 class="voice-title font-semibold text-white">CALLSIGNAL Voice Workspace</h1>
      <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-400">Start a deterministic demo call, watch the live transcript rail update, and move the session through escalation, handoff, resolution, or end.</p>
    </div>
    <div class="flex flex-wrap items-center gap-3">
      <select bind:value={selectedScenario} class="rounded-2xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-200 shadow-glow outline-none">
        {#each scenarios as scenario}
          <option value={scenario.scenario_id}>{scenario.title}</option>
        {/each}
      </select>
      <button class="rounded-2xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:opacity-50" disabled={busy || !selectedScenario} on:click={() => onStart(selectedScenario)}>Start demo call</button>
      <button class="rounded-2xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm font-semibold text-slate-100 transition hover:border-slate-500 disabled:opacity-50" disabled={busy} on:click={onResolve}>Resolve</button>
      <button class="rounded-2xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm font-semibold text-slate-100 transition hover:border-slate-500 disabled:opacity-50" disabled={busy} on:click={onEscalate}>Escalate</button>
      <button class="rounded-2xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm font-semibold text-slate-100 transition hover:border-slate-500 disabled:opacity-50" disabled={busy} on:click={onHandoff}>Prepare handoff</button>
      <button class="rounded-2xl border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm font-semibold text-rose-200 transition hover:bg-rose-500/20 disabled:opacity-50" disabled={busy} on:click={onEnd}>End call</button>
    </div>
  </div>
</section>
