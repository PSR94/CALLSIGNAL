<script lang="ts">
  export let kind: string;
  export let placeholder: string;
</script>

<span class="inline-flex items-center rounded-full border border-cyan-500/30 bg-cyan-500/10 px-2 py-0.5 text-[11px] font-semibold uppercase tracking-[0.2em] text-cyan-200">
  {kind} → {placeholder}
</span>
