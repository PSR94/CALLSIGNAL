import { z } from 'zod';

export const callSummarySchema = z.object({
  call_id: z.string(),
  scenario_id: z.string(),
  state: z.string(),
  caller_name: z.string().nullable().optional(),
  current_intent: z.string().nullable().optional(),
  intent_confidence: z.number().nullable().optional(),
  summary: z.string().nullable().optional(),
  resolution_code: z.string().nullable().optional(),
  quality_score: z.number().nullable().optional(),
  escalation_reasons: z.array(z.string()).default([]),
  started_at: z.string().nullable().optional(),
  ended_at: z.string().nullable().optional(),
  created_at: z.string(),
  updated_at: z.string()
});

export const callEventSchema = z.object({
  event_id: z.string(),
  call_id: z.string(),
  sequence: z.number(),
  event_type: z.string(),
  timestamp: z.string(),
  payload: z.record(z.any())
});

export const scenarioSchema = z.object({
  scenario_id: z.string(),
  title: z.string(),
  caller_persona: z.string(),
  problem_type: z.string(),
  turns: z.array(z.object({ turn_id: z.string(), speaker: z.string(), text: z.string(), kind: z.string().optional() })),
  expected_intents: z.array(z.string()),
  expected_redactions: z.array(z.string()),
  expected_escalation: z.array(z.string()),
  expected_quality: z.string()
});

export const supervisorSummarySchema = z.object({
  total_calls: z.number(),
  active_calls: z.number(),
  escalated_calls: z.number(),
  average_handling_time: z.string(),
  first_call_resolution_rate: z.number(),
  qa_average: z.number()
});

export type CallSummary = z.infer<typeof callSummarySchema>;
export type CallEvent = z.infer<typeof callEventSchema>;
export type ScenarioDefinition = z.infer<typeof scenarioSchema>;
export type SupervisorSummary = z.infer<typeof supervisorSummarySchema>;

export function callLabel(call: CallSummary): string {
  return `${call.call_id} · ${call.current_intent ?? 'unknown'} · ${call.state}`;
}
