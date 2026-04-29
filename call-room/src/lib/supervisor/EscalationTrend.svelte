<script lang="ts">
  export let rows: { window: number; score: number }[] = [];
</script>

<section class="panel p-5">
  <h2 class="mb-4 text-lg font-semibold text-white">Quality trend</h2>
  <svg viewBox="0 0 640 240" class="h-56 w-full">
    <polyline
      fill="none"
      stroke="#42a5ff"
      stroke-width="4"
      points={rows.map((row, index) => `${40 + index * 92},${200 - row.score}`).join(' ')}
    />
    {#each rows as row, index}
      <circle cx={40 + index * 92} cy={200 - row.score} r="6" fill="#3be0a2" />
      <text x={40 + index * 92} y="220" text-anchor="middle" fill="#94a3b8" font-size="11">{row.window}</text>
    {/each}
  </svg>
</section>
