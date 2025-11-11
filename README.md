# Habrok Audio Transcription Workflow

Automated audio transcription with speaker diarization for the RUG Habrok HPC cluster. Uses OpenAI Whisper for transcription and pyannote.audio for speaker identification.

---

## 🎯 What This Does

- **Transcribes** audio files (English, Dutch, 90+ languages)
- **Identifies speakers** (SPEAKER_00, SPEAKER_01, etc.)

**Input:** MP3, WAV, M4A, FLAC audio files  
**Output:** Text transcripts with timestamps and speaker labels

---

## 📚 Documentation

### For First-Time Users
👉 **[SSH_SETUP.md](SSH_SETUP.md)** - Set up passwordless SSH access (5 min, one-time)
👉 **[SETUP.md](SETUP.md)** - Complete installation guide (30 minutes)

### For Daily Use
👉 **[QUICK_START.md](QUICK_START.md)** - Copy-paste commands for everyday transcription


## ⚡ Common Commands Reference

### Connect to Habrok
```bash
ssh YOUR_P_NUMBER@login1.hb.hpc.rug.nl
```

### Submit single file job
```bash
cd /scratch/$USER/audio_processing
sbatch run_audio.sh
```
