create table if not exists call_sessions (
  call_id text primary key,
  scenario_id text not null,
  caller_name text,
  state text not null,
  current_intent text,
  intent_confidence real,
  summary text,
  resolution_code text,
  started_at text,
  ended_at text,
  escalation_reason_json text,
  handoff_packet_json text,
  quality_json text,
  created_at text not null,
  updated_at text not null
);

create table if not exists call_events (
  event_id text primary key,
  call_id text not null,
  sequence integer not null,
  event_type text not null,
  timestamp text not null,
  payload_json text not null
);

create table if not exists transcript_frames (
  id text primary key,
  call_id text not null,
  turn_id text not null,
  speaker text not null,
  text text not null,
  normalized_text text not null,
  is_partial integer not null,
  sequence integer not null,
  source text not null,
  redacted_text text not null,
  redaction_matches_json text not null,
  created_at text not null
);

create table if not exists redaction_events (
  id text primary key,
  call_id text not null,
  turn_id text not null,
  sequence integer not null,
  redaction_kind text not null,
  original_value text not null,
  placeholder text not null,
  created_at text not null
);
