export const ssr = false;

export function load({ params }) {
  return { callId: params.call_id };
}
