<script lang="ts">
  import RedactionMarker from './RedactionMarker.svelte';
  export let turn: { turn_id: string; speaker: string; text: string; redacted_text: string; sequence: number; is_partial: boolean; redactions?: { kind: string; placeholder: string }[] };
</script>

<article class="rounded-2xl border border-slate-800/90 bg-slate-950/80 p-4 shadow-[0_12px_60px_rgba(0,0,0,0.3)]">
  <div class="mb-2 flex items-center justify-between gap-3 text-xs uppercase tracking-[0.22em] text-slate-400">
    <span>{turn.speaker}</span>
    <span>Turn {turn.sequence}</span>
  </div>
  <p class="text-sm leading-6 text-slate-100">{turn.redacted_text}</p>
  {#if turn.redactions?.length}
    <div class="mt-3 flex flex-wrap gap-2">
      {#each turn.redactions as redaction}
        <RedactionMarker kind={redaction.kind} placeholder={redaction.placeholder} />
      {/each}
    </div>
  {/if}
</article>
