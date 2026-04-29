import { writable } from 'svelte/store';
import { fetchCalls, fetchEscalationQueue, fetchIntentMix, fetchQualityTrend, fetchSupervisorSummary } from '$lib/api/callApi';

export type SupervisorState = {
  summary: any;
  intentMix: any[];
  qualityTrend: any[];
  escalationQueue: any[];
  recentCalls: any[];
};

const initialState: SupervisorState = {
  summary: null,
  intentMix: [],
  qualityTrend: [],
  escalationQueue: [],
  recentCalls: []
};

function createSupervisorStore() {
  const { subscribe, update } = writable<SupervisorState>(initialState);

  async function refresh() {
    const [summary, intentMix, qualityTrend, escalationQueue, recentCalls] = await Promise.all([
      fetchSupervisorSummary(),
      fetchIntentMix(),
      fetchQualityTrend(),
      fetchEscalationQueue(),
      fetchCalls()
    ]);
    update(() => ({ summary, intentMix, qualityTrend, escalationQueue, recentCalls }));
  }

  return { subscribe, refresh };
}

export const supervisorStore = createSupervisorStore();
