<script lang="ts">
  export let priority = 'normal';
</script>

<span class={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] ${priority === 'critical' ? 'border-rose-500/30 bg-rose-500/10 text-rose-200' : priority === 'high' ? 'border-amber-500/30 bg-amber-500/10 text-amber-200' : 'border-slate-700 bg-slate-900 text-slate-300'}`}>
  {priority}
</span>
