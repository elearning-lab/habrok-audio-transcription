# Habrok Audio Transcription Setup Guide

Automated transcription with speaker diarization for RUG Habrok HPC cluster.

## Prerequisites

1. **Habrok account** - Request via IRIS
2. **Hugging Face account** - Sign up at https://huggingface.co/join
3. **SSH access to Habrok** from your computer's terminal 

---

## One-Time Setup (takes about 30 minutes)

### 1. Get Hugging Face Token

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Name it: `habrok_audio`
4. Type: **Read**
5. Click **Create token**
6. **Copy the token for step 6** (starts with `hf_`)

### 2. Accept Model Terms

Visit these pages and click "Agree":
- https://huggingface.co/pyannote/speaker-diarization-3.1
- https://huggingface.co/pyannote/speaker-diarization-community-1
- https://huggingface.co/pyannote/segmentation-3.0

### 3. Connect to Habrok

Open Terminal (Mac/Linux) or PowerShell (Windows) and log in with your p-number:
```bash
ssh YOUR_P_NUMBER@login1.hb.hpc.rug.nl
```

Enter your password. No characters will show as you type. that is normal. 
Enter your 2FA token from your Authenticator app.

You should now see the Habrok login screen. 

### 4. Create Project Structure
```bash
cd /scratch/$USER/
mkdir -p audio_processing whisper/input whisper/output
cd audio_processing
```

### 5. Install Python Environment
```bash
module load Python/3.10.4-GCCcore-11.3.0
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install openai-whisper pyannote.audio torch torchaudio
```

**This takes 5-10 minutes.**

### 6. Save Your HF Token
```bash
nano ~/.bashrc
```

Add this line at the bottom (paste YOUR token):
```bash
export HF_TOKEN="hf_YOUR_TOKEN_HERE"
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

Load it:
```bash
source ~/.bashrc
```

### 7. Download Scripts

Download files from this repository and upload to Habrok:

**On your computer:**
```bash
scp transcribe_and_diarize.py YOUR_P_NUMBER@login1.hb.hpc.rug.nl:/scratch/$USER/audio_processing/
scp run_audio.sh YOUR_P_NUMBER@login1.hb.hpc.rug.nl:/scratch/$USER/audio_processing/
```

**OR manually:** Download files, then use `scp` or the Habrok web portal file upload.

### 8. Edit Batch Script

On Habrok:
```bash
nano /scratch/$USER/audio_processing/run_audio.sh
```

Change `YOUR.EMAIL@rug.nl` to your actual email address.

Save (for Mac): `Ctrl+O`, `Enter`, `Ctrl+X`

---

## Usage (Every Time)

### 1. Upload Audio File
```bash
scp your_audio.mp3 YOUR_P_NUMBER@login1.hb.hpc.rug.nl:/scratch/$USER/whisper/input/
```

### 2. Submit Job

Connect to Habrok:
```bash
ssh YOUR_P_NUMBER@login1.hb.hpc.rug.nl
cd /scratch/$USER/audio_processing
sbatch run_audio.sh
```

You'll get a job number like: `Submitted batch job 12345`

### 3. Check Status
```bash
squeue -u $USER
```

### 4. Download Results

When complete, download from your computer:
```bash
scp YOUR_P_NUMBER@login1.hb.hpc.rug.nl:/scratch/$USER/whisper/output/* ~/Downloads/
```

---

## Output Files

- `FILENAME_transcript.txt` - Full transcription (no speakers)
- `FILENAME_diarized.txt` - Transcription with speaker labels

Example output:
```
[SPEAKER_00]
[0.0s - 5.2s] Welcome back everyone.
[5.5s - 10.8s] Today we're discussing medical education.

[SPEAKER_01]
[11.0s - 15.3s] Thank you for having me.
```

---

## Troubleshooting

**"Connection refused"** → Try `login2.hb.hpc.rug.nl` or wait 2 minutes

**"FFmpeg not found"** → Check that `run_audio.sh` loads FFmpeg module

**"403 Forbidden"** → Accept model terms at HuggingFace links above

**Job takes too long** → Check `squeue -u $USER` for status

---

## Support

- Habrok documentation: https://wiki.hpc.rug.nl/habrok/
- Habrok status: https://status.hpc.rug.nl
- Issues with this workflow: Open an issue on this GitHub repository
