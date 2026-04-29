<script lang="ts">
  export let notes: string[] = [];
</script>

<section class="panel p-5">
  <h2 class="mb-3 text-lg font-semibold text-white">Coaching notes</h2>
  <ul class="space-y-2 text-sm text-slate-300">
    {#if notes.length}
      {#each notes as note}
        <li class="rounded-2xl border border-slate-800 bg-slate-950/90 p-3 leading-6">{note}</li>
      {/each}
    {:else}
      <li class="text-slate-500">No coaching notes yet.</li>
    {/if}
  </ul>
</section>
