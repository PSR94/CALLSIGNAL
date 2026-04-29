import { describe, expect, it } from 'vitest';
import { callLabel, callSummarySchema, scenarioSchema } from './call-contracts';

describe('call contracts', () => {
  it('parses a call summary', () => {
    const call = callSummarySchema.parse({
      call_id: 'call-1',
      scenario_id: 'billing_dispute',
      state: 'active',
      caller_name: null,
      current_intent: 'billing_question',
      intent_confidence: 0.91,
      summary: null,
      resolution_code: null,
      started_at: null,
      ended_at: null,
      created_at: '2026-04-27T00:00:00Z',
      updated_at: '2026-04-27T00:00:00Z'
    });

    expect(callLabel(call)).toContain('billing_question');
  });

  it('parses a scenario definition', () => {
    const scenario = scenarioSchema.parse({
      scenario_id: 'appointment_reschedule',
      title: 'Appointment reschedule',
      caller_persona: 'routine_policy_holder',
      problem_type: 'scheduling',
      turns: [{ turn_id: 't1', speaker: 'caller', text: 'I need to reschedule', kind: 'final' }],
      expected_intents: ['appointment_request'],
      expected_redactions: [],
      expected_escalation: [],
      expected_quality: 'resolved'
    });

    expect(scenario.turns).toHaveLength(1);
  });
});
