#This program processes a folder of videos to analyze facial emotions in each one, extract the dominant emotion, 
# and generate a CSV file with valence/arousal values. 
# It then moves each video into a new folder named after its dominant emotion (e.g., happy/, sad/) and 
# renames it to a simplified format like happy_1.mp4.
# #output video files and csv are in /Users/pavana/Desktop/Student-Enagagement/DAISEE/by-emotion/ 
#input to this program is the balanced daisee dataset of four original affective states
import cv2
import pandas as pd
from deepface import DeepFace
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import shutil
from collections import defaultdict
#this is for displayed emotion


#Circumplex Model of Affect developed by psychologist James A. Russell (1980).
# Emotion mapping to valence and arousal
"""
emotion_mapping = {
    'angry': {'valence': -0.6, 'arousal': 0.7},
    'disgust': {'valence': -0.6, 'arousal': 0.3},
    'fear': {'valence': -0.7, 'arousal': 0.8},
    'happy': {'valence': 0.8, 'arousal': 0.7},
    'sad': {'valence': -0.7, 'arousal': 0.4},
    'surprise': {'valence': 0.4, 'arousal': 0.8},
    'neutral': {'valence': 0.0, 'arousal': 0.0}
}
"""
#Cowen & Keltner (2017) Emotion-to-Valence/Arousal Mapping:
emotion_mapping = {
    'happy':    {'valence':  0.9, 'arousal': 0.7},
    'angry':    {'valence': -0.7, 'arousal': 0.6},
    'sad':      {'valence': -0.6, 'arousal': 0.4},
    'fear':     {'valence': -0.7, 'arousal': 0.9},
    'disgust':  {'valence': -0.8, 'arousal': 0.4},
    'surprise': {'valence':  0.5, 'arousal': 0.8},
    'neutral':  {'valence':  0.0, 'arousal': 0.0}
}

#use this for sed/daisee dataset
def extract_emotions_valence_arousal(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    frame_count = 0

    data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotions = result[0]['emotion']
        dominant_emotion = result[0]['dominant_emotion']

        # Calculate valence and arousal
        valence, arousal = 0, 0
        total_weight = 0
        for emotion, mapping in emotion_mapping.items():
            weight = emotions[emotion] / 100
            valence += weight * emotion_mapping[emotion]['valence']
            arousal += weight * emotion_mapping[emotion]['arousal']
            total_weight += weight
        
        valence = valence / total_weight if total_weight else 0
        arousal = arousal / total_weight if total_weight else 0

        # Save results
        data.append({
            'timestamp': frame_count / fps,
            'dominant_emotion': dominant_emotion,
            'valence': valence,
            'arousal': arousal,
        })
        frame_count += 1
        """
        # Overlay info on frame
        cv2.putText(frame, f'Emotion: {dominant_emotion}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        cv2.putText(frame, f'Valence: {valence:.2f}', (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
        cv2.putText(frame, f'Arousal: {arousal:.2f}', (10,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

        cv2.imshow('Emotion-Valence-Arousal', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows() 
    """
    # Save data
    df = pd.DataFrame(data)
    #base_name = os.path.basename(video_path)
    #csv_name = os.path.splitext(base_name)[0] + '.csv'
    #csv_path = os.path.join('/Users/pavana/Desktop/UBFC-VA-Results', csv_name)
    #df.to_csv(csv_path, index=False)

    return df
"""
def process_videos_from_folder(folder_path, csv_directory, output_directory):
    video_files = glob.glob(os.path.join(folder_path, '*.*'))
    emotion_index_tracker = defaultdict(int)  # Track index per emotion

    for video_file in video_files:
        print(f"Processing {video_file}...")
        df = extract_emotions_valence_arousal(video_file)

        # Extract base filename and extension
        base_name = os.path.basename(video_file)
        name_wo_ext, ext = os.path.splitext(base_name)

        # Determine the dominant emotion
        if 'dominant_emotion' in df.columns:
            dominant_emotion = df['dominant_emotion'].mode()[0]
            target_dir = os.path.join(output_directory, dominant_emotion)
            os.makedirs(target_dir, exist_ok=True)

            # Update emotion-specific index and rename
            emotion_index_tracker[dominant_emotion] += 1
            new_name = f"{dominant_emotion}_{emotion_index_tracker[dominant_emotion]}"

            # Move and rename video
            video_target_path = os.path.join(target_dir, new_name + ext)
            shutil.move(video_file, video_target_path)
            print(f"Moved and renamed to {video_target_path}")

            # Save CSV with the same name as the video file
            csv_target_path = os.path.join(target_dir, new_name + '.csv')
            df.to_csv(csv_target_path, index=False)
        else:
            print(f"No 'dominant_emotion' column found for {video_file}, skipping.")
"""
#test set 
def process_videos_from_folder(folder_path, csv_directory):
    video_files = glob.glob(os.path.join(folder_path, '*.*'))

    for video_file in video_files:
        print(f"Processing {video_file}...")
        df = extract_emotions_valence_arousal(video_file)

        base_name = os.path.basename(video_file)
        name_wo_ext, _ = os.path.splitext(base_name)

        if 'dominant_emotion' in df.columns:
            # Save CSV with the same name as the original video file (but with .csv)
            csv_target_path = os.path.join(csv_directory, name_wo_ext + '.csv')
            df.to_csv(csv_target_path, index=False)
            print(f"Saved: {csv_target_path}")
        else:
            print(f"No 'dominant_emotion' column found for {video_file}, skipping.")


if __name__ == "__main__":
    #this is for daisee dataset which is balnced meaning equal number of videos in each class
    #folder_path = "/Users/pavana/Desktop/Student-Enagagement/DAISEE/daisee-emotions/"
    #csv_directory = "/Users/pavana/Desktop/Student-Enagagement/DAISEE/daisee-emotions/csv/"
    #output_directory = "/Users/pavana/Desktop/Student-Enagagement/DAISEE/by-emotion/"

    #test - set
    folder_path = "/Users/pavana/Desktop/Student-Enagagement/Daisee-VA/frustration/"
    csv_directory = "/Users/pavana/Desktop/Student-Enagagement/Daisee-VA/frustration/"
    #output_directory = "/Users/pavana/Desktop/Student-Enagagement/DAISEE/by-emotion/"

    #process_videos_from_folder(folder_path, csv_directory, output_directory)
    process_videos_from_folder(folder_path, csv_directory)
"""

def process_videos_from_folder(folder_path, csv_directory):
    video_files = glob.glob(os.path.join(folder_path, '*.*'))
    
    for video_file in video_files:
        print(f"Processing {video_file}...")
        df = extract_emotions_valence_arousal(video_file)
        
        # Extract video file name
        base_name = os.path.basename(video_file)
        csv_name = os.path.splitext(base_name)[0] + '.csv'
        csv_path = os.path.join(csv_directory, csv_name)
        
        df.to_csv(csv_path, index=False)
        print(f"Results saved to {csv_path}")
if __name__ == "__main__":
    #for sed
    #folder_path = '/Users/pavana/Desktop/Student-Enagagement/Datasets/test_sed_videos/final_test_set/test/'
    #for daisee
    #folder_path = '/Users/pavana/Desktop/Student-Enagagement/DAISEE/balanced_daisee/engagement/'
    #folder_path= '/Users/pavana/Desktop/Student-Enagagement/DAISEE/balanced_daisee/frustration/'
    folder_path = '/Users/pavana/Desktop/Student-Enagagement/DAISEE/balanced_daisee/boredom/'
    csv_directory = '/Users/pavana/Desktop/Student-Enagagement/VA-results/daisee/boredom/csv/'
    process_videos_from_folder(folder_path, csv_directory)



#use this for ubfc physics
def process_videos_from_folder(folder_path):
    subfolders = sorted([f.path for f in os.scandir(folder_path) if f.is_dir()])[:10]
    
    for subfolder in subfolders:
        video_files = glob.glob(os.path.join(subfolder, '**', 'processed_T1.mov'), recursive=True) + \
                      glob.glob(os.path.join(subfolder, '**', 'processed_T3.mov'), recursive=True)
        
        for video_file in video_files:
            print(f"Processing {video_file}...")
            df = extract_emotions_valence_arousal(video_file)
            
            # Extract subfolder name
            subfolder_name = os.path.basename(subfolder)
            base_name = os.path.basename(video_file)
            csv_name = f"{subfolder_name}_{base_name}.csv"
            csv_path = os.path.join('/Users/pavana/Desktop/Student-Enagagement/VA-results/ubfc/', csv_name)
            
            df.to_csv(csv_path, index=False)
            print(f"Results saved to {csv_path}")

if __name__ == "__main__":
    folder_path = '/Users/pavana/Desktop/Student-Enagagement/ubfc-processed/'
    process_videos_from_folder(folder_path)
"""