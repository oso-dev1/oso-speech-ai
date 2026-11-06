# OSO Speech AI

OSO Speech AI is a local demo that transcribes Arabic (العربية) and Persian (فارسی) recordings. It uses a Gradio web interface and the multilingual Whisper Base model through faster-whisper. The model runs on your CPU and needs no API key.

## Run locally

Extract the ZIP and open a terminal inside the `oso-speech-ai` folder. Use 64-bit Python 3.12.

**Windows (PowerShell)**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

**macOS or Linux**

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open the local URL printed in the terminal, usually `http://127.0.0.1:7860`. Press `Ctrl+C` in the terminal to stop the app.

## Transcribe a recording

1. Upload a WAV, MP3, M4A, FLAC, OGG, Opus, AAC, or WebM file, up to 100 MB.
2. Choose **Arabic**, **Persian**, or **Auto-detect**. Automatic detection can also report other languages supported by Whisper.
3. Select **Transcribe**. The text appears in a right-to-left box in the spoken language.
4. Use the copy icon or download `transcript.txt`, a UTF-8 text file.

The first transcription needs an internet connection to download the [multilingual Base model](https://huggingface.co/Systran/faster-whisper-base) (about 148 MB). The model is cached for later runs. Audio is processed on your computer. A separate FFmpeg installation is generally unnecessary because [faster-whisper](https://github.com/SYSTRAN/faster-whisper) decodes the audio with PyAV.

## Try a quick sample

Start with a short, clear recording in each language. For example, record `مرحبًا، هذا اختبار لتحويل الصوت إلى نص باللغة العربية` and `سلام، این یک آزمایش برای تبدیل گفتار به متن فارسی است`. Select the matching language for each recording, then try **Auto-detect**. Open the exported text file and compare it with the text shown in the app. Dialect, background noise, and recording quality can affect the wording.

## Troubleshooting

- **Model loading failed** — Check your internet connection, then retry the first transcription. The terminal shows the detailed error.
- **Empty or unexpected transcript** — Try a longer, clearer clip and select the spoken language explicitly.
- **The recording cannot be decoded** — Check that the file plays, or save another copy as WAV or MP3.

To add the demo to a GitHub repository, upload the extracted project files, including `.gitignore`.
## Project Screenshots

### Application Preview
![OSO Speech AI](OSO%20Speech%20AI%20Local%20Transcription%20Interface.png)

### Persian Transcription Test
![Persian Transcription](Screenshot%202026-11-06%20181103.png)
