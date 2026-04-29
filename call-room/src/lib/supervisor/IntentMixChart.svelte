<script lang="ts">
  export let rows: { intent: string; count: number }[] = [];
  const colors = ['#42a5ff', '#3be0a2', '#fbbf24', '#fb7185', '#a78bfa'];
</script>

<section class="panel p-5">
  <h2 class="mb-4 text-lg font-semibold text-white">Intent mix</h2>
  <svg viewBox="0 0 640 260" class="h-64 w-full">
    {#each rows as row, index}
      <g transform={`translate(${40 + index * 120}, 40)`}>
        <rect x="0" y="0" width="84" height="160" rx="18" fill="rgba(15,23,42,0.95)" stroke="rgba(71,85,105,0.7)" />
        <rect x="12" y={160 - Math.max(20, row.count * 26)} width="60" height={Math.max(20, row.count * 26)} rx="12" fill={colors[index % colors.length]} opacity="0.92" />
        <text x="42" y="186" text-anchor="middle" fill="#dbeafe" font-size="12">{row.intent}</text>
        <text x="42" y={150 - Math.max(20, row.count * 26)} text-anchor="middle" fill="#f8fafc" font-size="13" font-weight="700">{row.count}</text>
      </g>
    {/each}
  </svg>
</section>
