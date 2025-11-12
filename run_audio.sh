#!/bin/bash
#SBATCH --job-name=audio_diarize
#SBATCH --time=01:30:00
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

python /scratch/$USER/audio_processing/transcribe_and_diarize.py \
  /scratch/$USER/whisper/input/YOUR_FILE.mp3 \
  --output-dir /scratch/$USER/whisper/output \
  --language en \
  --format txt

echo "Job complete!"
