# Redaction design

Redaction runs before transcript text reaches the safe UI projection. The backend detects email addresses, phone numbers, member IDs, policy IDs, claim IDs, payment-like numbers, and token-shaped values.

The system stores redaction events separately from the safe transcript so review screens can explain why text was masked without leaking the original value back into the console.
