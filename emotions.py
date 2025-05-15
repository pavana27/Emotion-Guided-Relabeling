import os
import pandas as pd
import shutil
from collections import Counter

# Set your base folder path here
#BASE_FOLDER = '/Users/pavana/Desktop/Student-Enagagement/DAISEE/by-emotion/'
BASE_FOLDER = '/Users/pavana/Desktop/Student-Enagagement/Daisee-VA/frustration/'
# Define output folders
#DEFINITIVE_FOLDER = '/Users/pavana/Desktop/Definitive-Daisee-test'
#LIKELY_FOLDER = '/Users/pavana/Desktop/Likely-Daisee'
#OPPOSING_FOLDER = '/Users/pavana/Desktop/Conflict-Daisee-test'

DEFINITIVE_FOLDER = '/Users/pavana/Desktop/Student-Enagagement/Daisee-VA/frustration/Definitive/'
LIKELY_FOLDER = '/Users/pavana/Desktop/Student-Enagagement/Daisee-VA/frustration/Likely/'
OPPOSING_FOLDER = '/Users/pavana/Desktop/Student-Enagagement/Daisee-VA/frustration/Conflict/'


# Create output folders if they don't exist
os.makedirs(DEFINITIVE_FOLDER, exist_ok=True)
os.makedirs(LIKELY_FOLDER, exist_ok=True)
os.makedirs(OPPOSING_FOLDER, exist_ok=True)

NEGATIVE_EMOTIONS = {'sad', 'fear', 'angry'}
POSITIVE_EMOTIONS = {'happy'}

def classify_video(csv_path):
    df = pd.read_csv(csv_path)
    emotions = df['dominant_emotion'].astype(str).str.lower().tolist()
    total_frames = len(emotions)

    if total_frames == 0:
        print(f"No frames found in {csv_path}")
        return None

    emotion_counts = Counter(emotions)
    most_common = emotion_counts.most_common(2)

    dominant_emotion, _ = most_common[0]
    if len(most_common) > 1:
        subdominant_emotion, _ = most_common[1]
    else:
        subdominant_emotion = 'neutral'

    # Classification rules
    if dominant_emotion in NEGATIVE_EMOTIONS and subdominant_emotion in NEGATIVE_EMOTIONS or \
        (dominant_emotion in POSITIVE_EMOTIONS and subdominant_emotion in POSITIVE_EMOTIONS):
        return 'Definitive'
    elif (dominant_emotion in NEGATIVE_EMOTIONS or dominant_emotion in POSITIVE_EMOTIONS) and subdominant_emotion == 'neutral':
        return 'Likely'
    elif (dominant_emotion in NEGATIVE_EMOTIONS and subdominant_emotion in POSITIVE_EMOTIONS) or \
         (dominant_emotion in POSITIVE_EMOTIONS and subdominant_emotion in NEGATIVE_EMOTIONS):
        return 'Opposing'
    else:
        return 'Unclassified'

def organize_videos(base_folder):
    definitive_count = 0
    likely_count = 0
    opposing_count = 0
    unclassified_count = 0
    unclassified_files = []

    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                base_name = os.path.splitext(file)[0]

                # Look for matching video
                possible_extensions = ['.mp4', '.avi', '.mov']
                video_path = None
                for ext in possible_extensions:
                    candidate = os.path.join(root, base_name + ext)
                    if os.path.exists(candidate):
                        video_path = candidate
                        break

                if not video_path:
                    print(f"Warning: No video found for {csv_path}")
                    continue

                category = classify_video(csv_path)
                if category == 'Unclassified':
                    unclassified_count += 1
                    unclassified_files.append(csv_path)
                    continue

                print(f"Processing {video_path}: Classified as {category}")

                # Copy the video to the corresponding category folder without renaming
                target_folder = {
                    'Definitive': DEFINITIVE_FOLDER,
                    'Likely': LIKELY_FOLDER,
                    'Opposing': OPPOSING_FOLDER
                }.get(category)

                if target_folder:
                    shutil.copy(video_path, os.path.join(target_folder, os.path.basename(video_path)))
                    if category == 'Definitive':
                        definitive_count += 1
                    elif category == 'Likely':
                        likely_count += 1
                    elif category == 'Opposing':
                        opposing_count += 1

    print("\nVideo classification completed.")
    print(f"Total Definitive videos: {definitive_count}")
    print(f"Total Likely videos: {likely_count}")
    print(f"Total Opposing videos: {opposing_count}")
    print(f"Total Unclassified videos: {unclassified_count}")

if __name__ == '__main__':
    organize_videos(BASE_FOLDER)