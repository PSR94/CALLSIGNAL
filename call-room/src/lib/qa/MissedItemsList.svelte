<script lang="ts">
  export let items: string[] = [];
</script>

<section class="panel p-5">
  <h2 class="mb-3 text-lg font-semibold text-white">Missed rubric items</h2>
  <div class="flex flex-wrap gap-2">
    {#if items.length}
      {#each items as item}
        <span class="rounded-full border border-rose-500/30 bg-rose-500/10 px-3 py-1 text-xs font-semibold text-rose-200">{item}</span>
      {/each}
    {:else}
      <span class="text-sm text-slate-500">None.</span>
    {/if}
  </div>
</section>
