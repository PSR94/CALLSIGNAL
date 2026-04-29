<script lang="ts">
  import '../app.postcss';
  import '$lib/styles/voice-surface.css';
</script>

<svelte:head>
  <title>CALLSIGNAL</title>
  <meta name="description" content="Real-time voice operations console for support, intake, escalation, and quality review." />
</svelte:head>

<div class="mx-auto min-h-screen max-w-[1600px] px-4 py-4 sm:px-6 lg:px-8">
  <header class="panel mb-4 flex flex-wrap items-center justify-between gap-4 px-5 py-4">
    <div>
      <div class="text-xs uppercase tracking-[0.32em] text-cyan-300">CALLSIGNAL</div>
      <div class="text-sm text-slate-400">Live voice operations platform</div>
    </div>
    <nav class="flex flex-wrap gap-2 text-sm text-slate-300">
      <a class="rounded-full border border-slate-800 px-4 py-2 hover:border-cyan-400 hover:text-white" href="/">Voice workspace</a>
      <a class="rounded-full border border-slate-800 px-4 py-2 hover:border-cyan-400 hover:text-white" href="/supervisor">Supervisor board</a>
      <a class="rounded-full border border-slate-800 px-4 py-2 hover:border-cyan-400 hover:text-white" href="/history">Call history</a>
      <a class="rounded-full border border-slate-800 px-4 py-2 hover:border-cyan-400 hover:text-white" href="/queue">Escalation queue</a>
      <a class="rounded-full border border-slate-800 px-4 py-2 hover:border-cyan-400 hover:text-white" href="/qa">QA center</a>
    </nav>
  </header>
  <slot />
</div>
