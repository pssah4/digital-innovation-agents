# OWASP LLM Top 10 Checklist

Nur relevant wenn das Projekt LLM-APIs nutzt (z.B. Anthropic, OpenAI).

## LLM01: Prompt Injection

- System-Prompt geschuetzt?
- User-Input wird gefiltert bevor er an LLM geht?
- Indirect Prompt Injection (via Dokumente/Web) bedacht?

## LLM02: Insecure Output Handling

- LLM-Output wird vor Nutzung in Code/UI validiert?
- Keine direkte Ausfuehrung von LLM-generiertem Code?
- Output-Sanitization fuer HTML/DOM?

## LLM03: Training Data Poisoning

- Meist nicht direkt relevant (nutzen Pre-trained Models)
- Falls Fine-Tuning: Trainingsdaten-Integrity pruefen

## LLM04: Model Denial of Service

- Rate Limiting auf LLM-API-Calls?
- Token-Limits gesetzt?
- Timeout-Handling fuer LLM-Requests?
- Cost Controls (Max-Spend)?

## LLM05: Supply Chain Vulnerabilities

- API-Keys sicher gespeichert (nicht im Code)?
- Modell-Versionen gepinnt?
- Fallback bei Provider-Ausfall?

## LLM06: Sensitive Information Disclosure

- PII wird nicht in Prompts gesendet?
- API-Keys nicht in Logs?
- Conversation History Retention Policy?

## LLM07: Insecure Plugin Design

- Tool/Plugin-Execution mit Least Privilege?
- File System Access eingeschraenkt?
- Network Access kontrolliert?

## LLM08: Excessive Agency

- Tools haben minimale Berechtigungen?
- Destructive Operations brauchen Bestaetigung?
- Rate Limits auf Tool-Ausfuehrung?

## LLM09: Overreliance

- LLM-Output wird validiert (nicht blind vertraut)?
- Kritische Entscheidungen brauchen Human Review?
- Hallucination-Detection wo moeglich?

## LLM10: Model Theft

- API-Keys rotiert?
- Rate Limiting verhindert Extraction?
- Zugriffsprotokollierung vorhanden?
