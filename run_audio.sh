#!/bin/bash
#SBATCH --job-name=audio_diarize
#SBATCH --time=02:00:00
#SBATCH --partition=gpu
#SBATCH --gpus-per-node=a100:1
#SBATCH --mem=32GB
#SBATCH --output=/scratch/%u/whisper/output/slurm-%j.out
#SBATCH --mail-type=END
#SBATCH --mail-user=YOUR.EMAIL@rug.nl

module purge
module load Python/3.10.4-GCCcore-11.3.0
module load CUDA/12.6.0
module load FFmpeg/7.1.1-GCCcore-14.2.0

source /scratch/$USER/audio_processing/venv/bin/activate

# Process ALL audio files in input directory
for AUDIO_FILE in /scratch/$USER/whisper/input/*.{mp3,wav,m4a,flac}; do
    # Skip if no files match
    [ -e "$AUDIO_FILE" ] || continue
    
    echo "=========================================="
    echo "Processing: $(basename "$AUDIO_FILE")"
    echo "=========================================="
    
    python /scratch/$USER/audio_processing/transcribe_and_diarize.py \
      "$AUDIO_FILE" \
      --output-dir /scratch/$USER/whisper/output \
      --language en \
      --format txt
    
    echo "Completed: $(basename "$AUDIO_FILE")"
    echo ""
done

echo "All files processed!"
