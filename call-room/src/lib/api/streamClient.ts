import { API_BASE_URL } from './runtime';
import type { CallEvent } from './call-contracts';

export function openCallStream(callId: string, onEvent: (event: CallEvent) => void, onStatus?: (status: 'connecting' | 'open' | 'closed' | 'error') => void) {
  const wsUrl = API_BASE_URL.replace(/^http/, 'ws') + `/stream/calls/${callId}`;
  const socket = new WebSocket(wsUrl);

  socket.onopen = () => onStatus?.('open');
  socket.onclose = () => onStatus?.('closed');
  socket.onerror = () => onStatus?.('error');
  socket.onmessage = (message) => onEvent(JSON.parse(message.data) as CallEvent);

  return {
    socket,
    close: () => socket.close()
  };
}
