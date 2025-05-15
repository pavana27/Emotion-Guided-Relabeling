import os
import cv2
import shutil
import glob
import pandas as pd
from deepface import DeepFace


def extract_emotions_valence_arousal(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    emotion_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        try:
            analysis = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False,
                prog_bar=False
            )
            if isinstance(analysis, list):
                analysis = analysis[0]
            dominant_emotion = analysis['dominant_emotion']
            valence = analysis['emotion'].get('happy', 0) - analysis['emotion'].get('sad', 0)
            arousal = sum([abs(v) for v in analysis['emotion'].values()]) / len(analysis['emotion'])
            emotion_data.append({
                'frame': frame_count,
                'dominant_emotion': dominant_emotion,
                'valence': valence,
                'arousal': arousal
            })
        except Exception as e:
            print(f"Error analyzing frame {frame_count} in {video_path}: {e}")

        frame_count += 1

    cap.release()
    return pd.DataFrame(emotion_data)


def process_videos_from_folder(folder_path, output_directory):
    video_files = glob.glob(os.path.join(folder_path, '*.*'))

    for video_file in video_files:
        print(f"Processing {video_file}...")
        df = extract_emotions_valence_arousal(video_file)

        if 'dominant_emotion' in df.columns:
            dominant_emotion = df['dominant_emotion'].mode()[0]
            target_dir = os.path.join(output_directory, dominant_emotion)
            os.makedirs(target_dir, exist_ok=True)

            base_name = os.path.basename(video_file)
            video_target_path = os.path.join(target_dir, base_name)

            shutil.move(video_file, video_target_path)
            print(f"Moved to {video_target_path}")

            csv_name = os.path.splitext(base_name)[0] + '.csv'
            csv_path = os.path.join(target_dir, csv_name)
            df.to_csv(csv_path, index=False)
        else:
            print(f"No 'dominant_emotion' found for {video_file}, skipping.")


if __name__ == "__main__":
    folder_path = "/Users/pavana/Desktop/Student-Enagagement/Daisee-VA/"
    output_directory = "/Users/pavana/Desktop/DAISEE-by-emotion/"
    process_videos_from_folder(folder_path, output_directory)
