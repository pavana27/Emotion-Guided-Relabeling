# Emotion-Based Dataset Preprocessing and Annotation

This repository provides scripts to process, categorize, and annotate video datasets based on facial emotions, valence, and arousal signals. These tools are designed for preparing emotion-focused datasets such as DAiSEE, EngageNet, or custom collections for use in emotion recognition or VideoQA tasks.

**Script:**  `valence-deep-face.py`
This script processes a folder of video files to extract frame-level facial emotions, and compute valence and arousal using the DeepFace library. It supports datasets like DAiSEE, SED, and UBFC-PHYS. The script uses emotion-to-valence/arousal mappings (based on Cowen & Keltner, 2017) to calculate:

Valence: Weighted sum of emotional positivity/negativity per frame

Arousal: Weighted sum of emotional intensity across categories

For each video:

The dominant emotion is detected per frame

A .csv file is generated containing timestamps, dominant emotion, valence, and arousal

Optional: Videos can be auto-sorted into folders by dominant emotion with renamed files

## 1. Organize Videos by Dominant Emotion

**Script:** `dominant-emotion-sort.py` 

This script processes each video using the DeepFace library to:
- Analyze facial expressions frame by frame
- Calculate valence (happiness − sadness) and arousal (mean emotional intensity)
- Determine the most frequently occurring emotion in each video
- Move each video to a folder named after the dominant emotion (e.g., `happy/`, `angry/`)
- Save a `.csv` per video with frame-wise emotion, valence, and arousal

This enables restructuring engagement-labeled datasets (e.g., DAiSEE) into standard emotion-based categories.

## 2. Generate Annotations for Emotion-Based Video Folders

Once videos are grouped by emotion categories, you can generate annotations using a custom script aligned with your model format (e.g., question-answer pairs for VQA tasks).

## 3. Categorize Videos into Definitive, Likely, and Opposing Emotion Types

**Script:** `emotions.py`

This script processes each `.csv` generated in Step 1 and classifies videos into:
- **Definitive**: Dominant and subdominant emotions are both negative
- **Likely**: Dominant is emotional, subdominant is neutral
- **Opposing**: Dominant and subdominant belong to opposite polarities (e.g., happy vs. sad)

The script moves each video to the respective category folder and prints a summary report.

## 4. Generate QA Annotations for Definitive and Opposing Videos

**Script:** `emotions-annotation.py`

This script creates two QA pairs per video in the `Definitive/` and `Opposing/` folders:
- A descriptive QA from a predefined template (e.g., “The person is clearly sad...”)
- A factual QA (“What is the primary emotion depicted in this video?”)

The output is stored in:
- `definitive_annotations_combined.json`
- `opposing_annotations_combined.json`

Each entry contains `video_id` and a list of two QA pairs, suitable for fine-tuning VideoQA models.

## Recommendation Before Use

Before running any scripts, review them to understand input expectations, file structure, and output format. These scripts rely on consistent naming, directory layout, and DeepFace library behavior. You might encounter some code issues related to data formatting or library versions, but given your expertise, you should be able to resolve them with minor adjustments.
