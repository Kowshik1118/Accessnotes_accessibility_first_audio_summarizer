# AccessNotes — Accessibility-first audio summarizer

A local desktop application that turns an existing audio **transcript** into readable study notes. It has no external dependencies, API, cloud service, server, database, or account requirement.

## Why transcript input?

Accurate audio transcription needs a speech-recognition model. This intentionally simple, privacy-first project does not upload audio or bundle a large model. Generate or obtain a transcript with consent, then open/paste it here.

## Run

```powershell
python main.py
```

## Outputs

- Extractive quick summary
- Key terms and frequency
- Questions found in the source
- Word count and reading-ease estimate
- Large-text mode
- Local export to `.txt`

## Limitations

Review the output against the original transcript. Automated extraction can omit context, mis-rank important sentences, and cannot replace captions, speaker identification, or descriptions of important non-speech/visual information.
