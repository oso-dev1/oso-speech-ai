import logging
from functools import lru_cache
from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp

import gradio as gr
from faster_whisper import WhisperModel


LOGGER = logging.getLogger(__name__)
LANGUAGES = {"ar": "Arabic", "fa": "Persian"}
EXPORTS = TemporaryDirectory(prefix="oso-speech-ai-")


@lru_cache(maxsize=1)
def get_model():
    return WhisperModel("base", device="cpu", compute_type="int8")


def transcribe(audio_path: str | None, language: str):
    if not audio_path:
        return "", "Upload an audio file to get started.", None
    if language != "auto" and language not in LANGUAGES:
        return "", "Choose Auto-detect, Arabic, or Persian.", None

    try:
        model = get_model()
    except Exception:
        LOGGER.exception("Could not load the Whisper model")
        message = "Could not load Whisper. Check your internet connection and see the terminal for details."
        return "", message, None

    try:
        segments, info = model.transcribe(
            audio_path,
            language=None if language == "auto" else language,
            task="transcribe",
            vad_filter=True,
        )
        transcript = " ".join(segment.text.strip() for segment in segments).strip()
    except Exception:
        LOGGER.exception("Transcription failed")
        message = "Could not transcribe this file. Try a playable WAV or MP3 and see the terminal for details."
        return "", message, None

    if not transcript:
        return "", "No speech was found. Try a clearer recording.", None

    language_name = LANGUAGES.get(info.language, info.language)
    status = (
        f"Detected {language_name} ({info.language_probability:.0%})."
        if language == "auto"
        else f"Transcribed as {language_name}."
    )
    try:
        folder = Path(mkdtemp(dir=EXPORTS.name))
        export = folder / "transcript.txt"
        export.write_text(transcript + "\n", encoding="utf-8")
    except OSError:
        LOGGER.exception("Could not write the transcript export")
        return transcript, f"{status} Download unavailable. You can still copy the text.", None

    return transcript, status, str(export)


def build_demo():
    with gr.Blocks(title="OSO Speech AI", analytics_enabled=False) as demo:
        gr.Markdown(
            "# OSO Speech AI\n"
            "Transcribe Arabic and Persian recordings locally with Whisper. "
            "Choose the spoken language or let the model detect it."
        )
        with gr.Row():
            with gr.Column():
                audio = gr.File(
                    label="1. Upload a recording",
                    file_types=[
                        ".wav", ".mp3", ".m4a", ".flac", ".ogg", ".opus", ".aac", ".webm"
                    ],
                    type="filepath",
                )
                language = gr.Dropdown(
                    label="2. Spoken language",
                    choices=[
                        ("Auto-detect", "auto"),
                        ("Arabic · العربية", "ar"),
                        ("Persian · فارسی", "fa"),
                    ],
                    value="auto",
                )
                submit = gr.Button("Transcribe", variant="primary")
                gr.Markdown("The first transcription downloads the Whisper model (about 148 MB).")

            with gr.Column():
                transcript = gr.Textbox(
                    label="Transcript",
                    placeholder="Your transcript will appear here.",
                    lines=9,
                    rtl=True,
                    interactive=False,
                    buttons=["copy"],
                )
                status = gr.Textbox(label="Status", interactive=False)
                download = gr.File(label="Download transcript (.txt)", interactive=False)

        submit.click(transcribe, [audio, language], [transcript, status, download])

    return demo.queue(default_concurrency_limit=1)


if __name__ == "__main__":
    build_demo().launch(server_name="127.0.0.1", share=False, max_file_size="100mb")
