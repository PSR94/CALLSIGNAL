import { API_BASE_URL } from './runtime';

export async function downloadReport(callId: string, format: 'json' | 'markdown') {
  const response = await fetch(`${API_BASE_URL}/calls/${callId}/report`);
  if (!response.ok) {
    throw new Error(await response.text());
  }
  const report = await response.json();
  return format === 'json' ? JSON.stringify(report, null, 2) : report.markdown as string;
}
