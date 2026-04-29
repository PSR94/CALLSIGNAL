import { writable } from 'svelte/store';
import { createCall, endCall, escalateCall, fetchCall, fetchCalls, fetchEscalationQueue, fetchQuality, fetchReport, fetchScenarios, fetchSignals, fetchTimeline, fetchTranscript, handoffCall, resolveCall, startCall } from '$lib/api/callApi';
import { openCallStream } from '$lib/api/streamClient';
import type { CallEvent, CallSummary, ScenarioDefinition } from '$lib/api/call-contracts';

export type TranscriptTurn = { turn_id: string; speaker: string; text: string; redacted_text: string; sequence: number; is_partial: boolean };

export type LiveCallState = {
  connectionStatus: 'idle' | 'connecting' | 'open' | 'closed' | 'error';
  activeCall: CallSummary | null;
  events: CallEvent[];
  transcript: TranscriptTurn[];
  signals: any;
  quality: any;
  report: any;
  scenarios: ScenarioDefinition[];
  recentCalls: CallSummary[];
  escalationQueue: any[];
  error: string | null;
};

const initialState: LiveCallState = {
  connectionStatus: 'idle',
  activeCall: null,
  events: [],
  transcript: [],
  signals: null,
  quality: null,
  report: null,
  scenarios: [],
  recentCalls: [],
  escalationQueue: [],
  error: null
};

function createLiveCallStore() {
  const { subscribe, set, update } = writable<LiveCallState>(initialState);
  let socketCloser: (() => void) | null = null;

  async function refreshCatalogs() {
    const [scenarios, recentCalls, escalationQueue] = await Promise.all([fetchScenarios(), fetchCalls(), fetchEscalationQueue()]);
    update((state) => ({ ...state, scenarios, recentCalls, escalationQueue }));
  }

  async function connect(callId: string) {
    socketCloser?.();
    update((state) => ({ ...state, connectionStatus: 'connecting', error: null, events: [], transcript: [], signals: null, quality: null, report: null }));
    const stream = openCallStream(callId, (event) => {
      update((state) => {
        const transcript = [...state.transcript];
        if (event.event_type.startsWith('transcript_')) {
          transcript.push({
            turn_id: event.payload.turn_id,
            speaker: event.payload.speaker,
            text: event.payload.text,
            redacted_text: event.payload.redacted_text ?? event.payload.text,
            sequence: event.sequence,
            is_partial: event.event_type === 'transcript_partial'
          });
        }
        return { ...state, events: [...state.events, event], transcript };
      });
    }, (status) => update((state) => ({ ...state, connectionStatus: status })));
    socketCloser = stream.close;
  }

  async function openDemoCall(scenarioId?: string) {
    const selected = scenarioId ?? (await fetchScenarios())[0]?.scenario_id;
    const created = await createCall(selected);
    const callId = created.call_id;
    update((state) => ({ ...state, activeCall: created, error: null }));
    await connect(callId);
    const started = await startCall(callId);
    const refreshedCall = await fetchCall(callId);
    update((state) => ({ ...state, activeCall: { ...refreshedCall, state: started.state }, error: null }));
    return callId;
  }

  async function hydrate(callId: string) {
    const [activeCall, timeline, transcript, signals, quality, report] = await Promise.all([
      fetchCall(callId),
      fetchTimeline(callId),
      fetchTranscript(callId),
      fetchSignals(callId),
      fetchQuality(callId),
      fetchReport(callId)
    ]);
    update((state) => ({ ...state, activeCall, events: timeline, transcript: transcript.map((turn: any) => ({ turn_id: turn.turn_id, speaker: turn.speaker, text: turn.text, redacted_text: turn.redacted_text, sequence: turn.sequence, is_partial: turn.is_partial })), signals, quality, report }));
  }

  async function runAction(action: 'resolve' | 'escalate' | 'handoff' | 'end', callId: string, payload?: any) {
    if (action === 'resolve') await resolveCall(callId, payload.resolution_code, payload.summary);
    if (action === 'escalate') await escalateCall(callId, payload.reason);
    if (action === 'handoff') await handoffCall(callId);
    if (action === 'end') await endCall(callId);
    const [activeCall, timeline, transcript, signals, quality, report, recentCalls, escalationQueue] = await Promise.all([
      fetchCall(callId),
      fetchTimeline(callId),
      fetchTranscript(callId),
      fetchSignals(callId),
      fetchQuality(callId),
      fetchReport(callId),
      fetchCalls(),
      fetchEscalationQueue()
    ]);
    update((state) => ({
      ...state,
      activeCall,
      events: timeline,
      transcript: transcript.map((turn: any) => ({ turn_id: turn.turn_id, speaker: turn.speaker, text: turn.text, redacted_text: turn.redacted_text, sequence: turn.sequence, is_partial: turn.is_partial })),
      signals,
      quality,
      report,
      recentCalls,
      escalationQueue
    }));
  }

  return {
    subscribe,
    refreshCatalogs,
    connect,
    openDemoCall,
    hydrate,
    runAction,
    stopStream: () => socketCloser?.()
  };
}

export const liveCallStore = createLiveCallStore();
