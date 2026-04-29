const maybeEnv = (import.meta as ImportMeta & { env?: Record<string, string | undefined> }).env;
export const API_BASE_URL = maybeEnv?.PUBLIC_API_BASE_URL || 'http://127.0.0.1:8088';
