import { API_BASE_URL } from './runtime';
import { callEventSchema, callSummarySchema, scenarioSchema, supervisorSummarySchema, type CallEvent, type CallSummary, type ScenarioDefinition, type SupervisorSummary } from './call-contracts';

async function fetchJson(path: string, init?: RequestInit) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'content-type': 'application/json' },
    ...init
  });
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

export async function fetchScenarios(): Promise<ScenarioDefinition[]> {
  const data = await fetchJson('/demo/scenarios');
  return data.map((entry: unknown) => scenarioSchema.parse(entry));
}

export async function fetchCalls(): Promise<CallSummary[]> {
  const data = await fetchJson('/calls');
  return data.map((entry: unknown) => callSummarySchema.parse(entry));
}

export async function fetchCall(callId: string): Promise<CallSummary> {
  return callSummarySchema.parse(await fetchJson(`/calls/${callId}`));
}

export async function createCall(scenarioId: string, callerName?: string): Promise<CallSummary> {
  const data = await fetchJson('/calls', {
    method: 'POST',
    body: JSON.stringify({ scenario_id: scenarioId, caller_name: callerName ?? null })
  });
  return callSummarySchema.parse(await fetchCall(data.call_id));
}

export async function startCall(callId: string) {
  return fetchJson(`/calls/${callId}/start`, { method: 'POST' });
}

export async function resolveCall(callId: string, resolutionCode: string, summary?: string) {
  return fetchJson(`/calls/${callId}/resolve`, { method: 'POST', body: JSON.stringify({ resolution_code: resolutionCode, summary }) });
}

export async function escalateCall(callId: string, reason: string) {
  return fetchJson(`/calls/${callId}/escalate`, { method: 'POST', body: JSON.stringify({ reason }) });
}

export async function handoffCall(callId: string) {
  return fetchJson(`/calls/${callId}/handoff`, { method: 'POST' });
}

export async function endCall(callId: string) {
  return fetchJson(`/calls/${callId}/end`, { method: 'POST' });
}

export async function fetchTranscript(callId: string) {
  return fetchJson(`/calls/${callId}/transcript`);
}

export async function fetchTimeline(callId: string): Promise<CallEvent[]> {
  const data = await fetchJson(`/calls/${callId}/timeline`);
  return data.map((entry: unknown) => callEventSchema.parse(entry));
}

export async function fetchSignals(callId: string) {
  return fetchJson(`/calls/${callId}/signals`);
}

export async function fetchQuality(callId: string) {
  return fetchJson(`/calls/${callId}/quality`);
}

export async function fetchReport(callId: string) {
  return fetchJson(`/calls/${callId}/report`);
}

export async function exportReport(callId: string) {
  return fetchJson(`/calls/${callId}/report/export`, { method: 'POST' });
}

export async function fetchSupervisorSummary(): Promise<SupervisorSummary> {
  return supervisorSummarySchema.parse(await fetchJson('/supervisor/summary'));
}

export async function fetchIntentMix() {
  return fetchJson('/supervisor/intent-mix');
}

export async function fetchQualityTrend() {
  return fetchJson('/supervisor/quality-trend');
}

export async function fetchEscalationQueue() {
  return fetchJson('/queue/escalations');
}
