#!/usr/bin/env python3
"""
Transcription + diarization optimized for Habrok GPUs.
"""

import os
import sys
import argparse
from pathlib import Path
import torch
import whisper
from pyannote.audio import Pipeline

def transcribe_audio(audio_path, model_size="large-v3", language="en", device="cuda"):
    """Transcribe audio using Whisper."""
    print(f"Loading Whisper model: {model_size} on {device}")
    model = whisper.load_model(model_size, device=device)
    
    print(f"Transcribing: {audio_path}")
    result = model.transcribe(
        str(audio_path),
        language=language,
        verbose=True
    )
    
    return result

def diarize_audio(audio_path, hf_token, device="cuda"):
    """Perform speaker diarization."""
    print("Loading diarization pipeline...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        token=hf_token
    )
    
    if device == "cuda" and torch.cuda.is_available():
        pipeline.to(torch.device("cuda"))
    
    print(f"Diarizing: {audio_path}")
    diarization = pipeline(str(audio_path))
    
    return diarization

def merge_transcription_and_diarization(transcription, diarization):
    """Merge Whisper segments with speaker labels."""
    segments = transcription['segments']
    speaker_segments = []
    
    # pyannote 4.0: Use exclusive mode (no overlaps)
    annotation = diarization.exclusive_speaker_diarization
    
    # Iterate over the annotation
    diarization_list = []
    for segment, _, speaker in annotation.itertracks(yield_label=True):
        diarization_list.append((segment.start, segment.end, speaker))
    
    # Match transcription with speakers
    for whisper_seg in segments:
        seg_start = whisper_seg['start']
        seg_end = whisper_seg['end']
        seg_text = whisper_seg['text']
        
        best_overlap = 0
        best_speaker = "UNKNOWN"
        
        for dia_start, dia_end, speaker_label in diarization_list:
            overlap_start = max(seg_start, dia_start)
            overlap_end = min(seg_end, dia_end)
            overlap = max(0, overlap_end - overlap_start)
            
            if overlap > best_overlap:
                best_overlap = overlap
                best_speaker = speaker_label
        
        speaker_segments.append({
            'start': seg_start,
            'end': seg_end,
            'speaker': best_speaker,
            'text': seg_text.strip()
        })
    
    return speaker_segments

def format_output(segments, format_type="txt"):
    """Format the output."""
    if format_type == "txt":
        lines = []
        current_speaker = None
        
        for seg in segments:
            if seg['speaker'] != current_speaker:
                lines.append(f"\n[{seg['speaker']}]")
                current_speaker = seg['speaker']
            
            timestamp = f"[{seg['start']:.1f}s - {seg['end']:.1f}s]"
            lines.append(f"{timestamp} {seg['text']}")
        
        return "\n".join(lines)
    
    elif format_type == "json":
        import json
        return json.dumps(segments, indent=2, ensure_ascii=False)
    
    elif format_type == "srt":
        lines = []
        for i, seg in enumerate(segments, 1):
            start_time = format_timestamp_srt(seg['start'])
            end_time = format_timestamp_srt(seg['end'])
            lines.append(f"{i}")
            lines.append(f"{start_time} --> {end_time}")
            lines.append(f"[{seg['speaker']}] {seg['text']}")
            lines.append("")
        
        return "\n".join(lines)

def format_timestamp_srt(seconds):
    """Convert seconds to SRT timestamp."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe and diarize audio on Habrok"
    )
    parser.add_argument("audio_file", type=str, help="Path to audio file")
    parser.add_argument("--output-dir", type=str, default="./output", help="Output directory")
    parser.add_argument("--model", type=str, default="large-v3", help="Whisper model size")
    parser.add_argument("--language", type=str, default="en", help="Audio language")
    parser.add_argument("--hf-token", type=str, help="Hugging Face token")
    parser.add_argument("--format", type=str, default="txt", choices=["txt", "json", "srt"])
    parser.add_argument("--skip-diarization", action="store_true")
    
    args = parser.parse_args()
    
    audio_path = Path(args.audio_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)
    
    hf_token = args.hf_token or os.environ.get("HF_TOKEN")
    if not args.skip_diarization and not hf_token:
        print("Error: Hugging Face token required")
        sys.exit(1)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Using device: {device}")
    
    transcription = transcribe_audio(audio_path, args.model, args.language, device)
    
    base_name = audio_path.stem
    transcription_file = output_dir / f"{base_name}_transcript.txt"
    with open(transcription_file, 'w', encoding='utf-8') as f:
        f.write(transcription['text'])
    print(f"✅ Transcription saved: {transcription_file}")
    
    if args.skip_diarization:
        return
    
    diarization = diarize_audio(audio_path, hf_token, device)
    
    print("🔄 Merging...")
    segments = merge_transcription_and_diarization(transcription, diarization)
    
    output_file = output_dir / f"{base_name}_diarized.{args.format}"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(format_output(segments, args.format))
    
    speakers = set(seg['speaker'] for seg in segments)
    print(f"✅ Output: {output_file}")
    print(f"🎤 Speakers: {speakers}")

if __name__ == "__main__":
    main()
