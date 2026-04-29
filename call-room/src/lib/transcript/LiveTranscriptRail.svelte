<script lang="ts">
  import TranscriptTurn from './TranscriptTurn.svelte';
  export let transcript: any[] = [];
</script>

<section class="panel p-5">
  <div class="mb-4 flex items-center justify-between">
    <div>
      <h2 class="text-lg font-semibold text-white">Live transcript</h2>
      <p class="text-sm text-slate-400">Streaming safe transcript frames with redaction already applied.</p>
    </div>
    <span class="soft-chip">{transcript.length} turns</span>
  </div>
  <div class="space-y-3">
    {#if transcript.length === 0}
      <div class="rounded-2xl border border-dashed border-slate-700 p-6 text-sm text-slate-400">Start a demo call to populate the transcript rail.</div>
    {:else}
      {#each transcript as turn}
        <TranscriptTurn {turn} />
      {/each}
    {/if}
  </div>
</section>
