<script lang="ts">
  export let state: string;

  const palette: Record<string, string> = {
    idle: 'border-slate-600 bg-slate-900 text-slate-300',
    connecting: 'border-amber-500/30 bg-amber-500/10 text-amber-200',
    active: 'border-cyan-500/30 bg-cyan-500/10 text-cyan-200',
    extracting: 'border-blue-500/30 bg-blue-500/10 text-blue-200',
    escalation_pending: 'border-amber-500/30 bg-amber-500/10 text-amber-200',
    handoff_ready: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200',
    resolved: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200',
    escalated: 'border-rose-500/30 bg-rose-500/10 text-rose-200',
    ended: 'border-slate-600 bg-slate-900 text-slate-300',
    failed: 'border-rose-500/30 bg-rose-500/10 text-rose-200'
  };
</script>

<span class={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] ${palette[state] ?? palette.idle}`}>
  {state.replaceAll('_', ' ')}
</span>
