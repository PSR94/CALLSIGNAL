<script lang="ts">
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';
  import { liveCallStore } from '$lib/state/liveCallStore';
  import CallCommandBar from '$lib/call-controls/CallCommandBar.svelte';
  import WaveformVisualizer from '$lib/canvas/waveform/WaveformVisualizer.svelte';
  import CallFlowMap from '$lib/canvas/call-flow/CallFlowMap.svelte';
  import LiveTranscriptRail from '$lib/transcript/LiveTranscriptRail.svelte';
  import EscalationLane from '$lib/escalation/EscalationLane.svelte';
  import HandoffPacket from '$lib/escalation/HandoffPacket.svelte';
  import RubricScorecard from '$lib/qa/RubricScorecard.svelte';
  import EventTimeline from '$lib/canvas/timeline/EventTimeline.svelte';

  const state = liveCallStore;
  let selectedScenario = '';
  let busy = false;

  onMount(() => {
    state.refreshCatalogs();
    const unsubscribe = liveCallStore.subscribe((value) => {
      if (!selectedScenario && value.scenarios.length) {
        selectedScenario = value.scenarios[0].scenario_id;
      }
    });
    return unsubscribe;
  });

  async function startDemo(scenarioId: string) {
    busy = true;
    try {
      await state.openDemoCall(scenarioId);
      selectedScenario = scenarioId;
    } finally {
      busy = false;
    }
  }

  async function resolveCall() {
    const snapshot = get(liveCallStore).activeCall;
    if (!snapshot) return;
    busy = true;
    try {
      await state.runAction('resolve', snapshot.call_id, { resolution_code: 'resolved', summary: 'Call resolved in the workspace.' });
    } finally {
      busy = false;
    }
  }

  async function escalateCall() {
    const snapshot = get(liveCallStore).activeCall;
    if (!snapshot) return;
    busy = true;
    try {
      await state.runAction('escalate', snapshot.call_id, { reason: 'supervisor_requested' });
    } finally {
      busy = false;
    }
  }

  async function prepareHandoff() {
    const snapshot = get(liveCallStore).activeCall;
    if (!snapshot) return;
    busy = true;
    try {
      await state.runAction('handoff', snapshot.call_id);
    } finally {
      busy = false;
    }
  }

  async function endCall() {
    const snapshot = get(liveCallStore).activeCall;
    if (!snapshot) return;
    busy = true;
    try {
      await state.runAction('end', snapshot.call_id);
    } finally {
      busy = false;
    }
  }
</script>

  {#if $liveCallStore}
  <div class="voice-grid lg:grid-cols-[1.2fr_0.8fr]">
    <div class="space-y-4">
      <CallCommandBar state={$liveCallStore.activeCall?.state ?? 'idle'} startedAt={$liveCallStore.activeCall?.started_at ?? null} scenarios={$liveCallStore.scenarios} bind:selectedScenario {busy} onStart={startDemo} onResolve={resolveCall} onEscalate={escalateCall} onHandoff={prepareHandoff} onEnd={endCall} />
      <WaveformVisualizer active={$liveCallStore.connectionStatus === 'open' || $liveCallStore.connectionStatus === 'connecting'} />
      <CallFlowMap state={$liveCallStore.activeCall?.state ?? 'idle'} />
      <LiveTranscriptRail transcript={$liveCallStore.transcript} />
      <EventTimeline events={$liveCallStore.events} />
    </div>
    <div class="space-y-4">
      <section class="panel p-5">
        <h2 class="mb-3 text-lg font-semibold text-white">Extracted fields</h2>
        <div class="space-y-2 text-sm text-slate-300">
          {#if $liveCallStore.signals?.fields?.length}
            {#each $liveCallStore.signals.fields as field}
              <div class="rounded-2xl border border-slate-800 bg-slate-950/90 p-3">
                <div class="text-xs uppercase tracking-[0.18em] text-slate-500">{field.field_name}</div>
                <div class="mt-1 font-semibold text-white">{field.value}</div>
                <div class="mt-1 text-xs text-slate-500">{field.redaction_status} · confidence {Math.round(field.confidence * 100)}%</div>
              </div>
            {/each}
          {:else}
            <p class="text-slate-500">No fields extracted yet.</p>
          {/if}
        </div>
      </section>
      <section class="panel p-5">
        <h2 class="mb-3 text-lg font-semibold text-white">Redaction events</h2>
        <div class="space-y-2 text-sm text-slate-300">
          {#if $liveCallStore.signals?.redactions?.length}
            {#each $liveCallStore.signals.redactions as redaction}
              <div class="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-3">
                <div class="text-xs uppercase tracking-[0.18em] text-cyan-200">{redaction.redaction_kind}</div>
                <div class="mt-1 text-slate-100">{redaction.placeholder}</div>
                <div class="mt-1 text-xs text-slate-500">turn {redaction.turn_id}</div>
              </div>
            {/each}
          {:else}
            <p class="text-slate-500">No redactions recorded yet.</p>
          {/if}
        </div>
      </section>
      <EscalationLane escalation={$liveCallStore.signals?.escalation} handoffPacket={$liveCallStore.signals?.handoff} />
      <HandoffPacket packet={$liveCallStore.signals?.handoff} />
      <RubricScorecard quality={$liveCallStore.quality} />
      <section class="panel p-5">
        <h2 class="mb-3 text-lg font-semibold text-white">Detected intent</h2>
        <pre class="whitespace-pre-wrap rounded-2xl bg-slate-950 p-4 text-sm text-slate-200">{JSON.stringify($liveCallStore.signals?.intent ?? {}, null, 2)}</pre>
      </section>
    </div>
  </div>
{/if}
