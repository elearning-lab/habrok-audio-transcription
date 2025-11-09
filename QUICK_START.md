# Quick Start Guide - Daily Workflow

After initial setup is complete, use this for everyday transcription tasks.

---

## 🚀 Single File Transcription

### Step 1: Upload Your Audio File

**Via Web Browser (Easiest):**
1. Go to: https://portal.hb.hpc.rug.nl
2. Click **Files** → navigate to `/scratch/YOUR_P_NUMBER/whisper/input/`
3. Click **Upload** → select your audio file
4. Wait for upload to complete

**Via Terminal:**
```bash
scp your_file.mp3 YOUR_P_NUMBER@login1.hb.hpc.rug.nl:/scratch/$USER/whisper/input/
```

---

### Step 2: Submit the Job

**Via Terminal:**
```bash
ssh YOUR_P_NUMBER@login1.hb.hpc.rug.nl
cd /scratch/$USER/audio_processing
sbatch run_audio.sh
```

You'll see: `Submitted batch job 12345678`

---

### Step 3: Check Progress
```bash
squeue -u $USER
```

**What you see:**
- `PD` = Pending (waiting for resources)
- `R` = Running
- Nothing = Job finished

---

### Step 4: Download Results

**Via Web Browser:**
1. Go to: https://portal.hb.hpc.rug.nl
2. Click **Files** → navigate to `/scratch/YOUR_P_NUMBER/whisper/output/`
3. Click on files to download:
   - `FILENAME_transcript.txt` (transcription only)
   - `FILENAME_diarized.txt` (with speakers)

**Via Terminal:**
```bash
scp YOUR_P_NUMBER@login1.hb.hpc.rug.nl:/scratch/$USER/whisper/output/*.txt ~/Downloads/
```

---

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

### Check job status
```bash
squeue -u $USER
```

### View job output (while running)
```bash
tail -f /scratch/$USER/whisper/output/slurm-*.out
```
Press `Ctrl+C` to stop viewing.

### List completed files
```bash
ls /scratch/$USER/whisper/output/
```

### Delete old files (cleanup)
```bash
rm /scratch/$USER/whisper/input/*.mp3
rm /scratch/$USER/whisper/output/*.txt
```

### Cancel a running job
```bash
scancel JOB_ID
```
(Replace JOB_ID with the number from `squeue`)

---

## 🎯 One-Liner Workflow

For experienced users, combine steps:
```bash
scp audio.mp3 p123456@login1.hb.hpc.rug.nl:/scratch/p123456/whisper/input/ && \
ssh p123456@login1.hb.hpc.rug.nl "cd /scratch/p123456/audio_processing && sbatch run_audio.sh"
```

(Replace `p123456` with your p-number)

---

## 📧 Get Email Notifications

Your job script already sends emails when complete. Check your RUG email inbox for:
- Subject: "Slurm Job_id=12345678 Name=audio_diarize Ended"

---

## 🔧 Troubleshooting Quick Fixes

### "Connection refused"
Try alternate login node:
```bash
ssh YOUR_P_NUMBER@login2.hb.hpc.rug.nl
```

### Job stuck in queue
Check status page: https://status.hpc.rug.nl

### Need longer processing time
Edit `run_audio.sh` and change:
```bash
#SBATCH --time=01:00:00
```
to:
```bash
#SBATCH --time=04:00:00
```

### Process different language
Edit `run_audio.sh`, find line with `--language en` and change to:
- Dutch: `--language nl`
- German: `--language de`
- Auto: remove the `--language` line entirely

---

## 💾 File Management Tips

### Keep input folder clean
After successful transcription, move or delete processed audio files.

### Organize by project
```bash
mkdir /scratch/$USER/whisper/input/project_name/
```

Then edit `run_audio.sh` to point to that folder.

### Archive old results
```bash
mkdir /scratch/$USER/whisper/archive/
mv /scratch/$USER/whisper/output/old_* /scratch/$USER/whisper/archive/
```

---

**Questions?** Check:
1. [SETUP.md](SETUP.md) - Initial installation
2. Habrok Wiki: https://wiki.hpc.rug.nl/habrok/
3. Open an issue on this GitHub repository
