
import os
import json
import random

# Define video folders and output paths
video_folders = {
    "Definitive": "/Users/pavana/Desktop/Definitive-Daisee",
    "Opposing": "/Users/pavana/Desktop/Conflict-Daisee"
}

output_paths = {
    "Definitive": "/mnt/data/definitive_annotations_combined.json",
    "Opposing": "/mnt/data/opposing_annotations_combined.json"
}

# Updated QA templates with emotion recognition and facial cues
qa_templates_combined = {
    "Definitive": [
        ("What emotion is clearly depicted in the video based on the person's facial expression?",
         "The person appears distinctly sad, with downturned lips and a lowered gaze."),
        ("Which emotion can be confidently identified from the facial expressions in the video?",
         "The individual shows anger, characterized by furrowed brows and tightened lips."),
        ("Identify the dominant emotion shown by the person in this video and describe the facial cues.",
         "The video reflects fear, visible through widened eyes and tense expressions."),
        ("What is the most apparent emotional state exhibited by the person in the video?",
         "The person looks clearly angry, with intense eye contact and clenched jaw."),
        ("How can you tell the person's emotional state in this video?",
         "The person is visibly fearful, shown by widened eyes and a slightly open mouth."),
        ("What specific emotion is the person showing and how?",
         "The individual is clearly sad, with slow movements and a downward gaze."),
        ("Based on the facial expressions, what emotion dominates this video?",
         "The dominant emotion is happiness, seen in a wide smile and relaxed eyes.")
    ],
    "Opposing": [
        ("What contradictory emotions are displayed in the video, and how are they visible on the face?",
         "Yes, the person smiles slightly but has tense brows, indicating mixed happiness and anger."),
        ("Describe the opposing emotional expressions shown in the video through facial behavior.",
         "The individual’s eyes reflect fear, but their mouth shows signs of a smile."),
        ("What emotional conflict is visible in the person’s face throughout the video?",
         "The dominant expression is sad, but there are brief upward lip movements suggesting conflicting emotion."),
        ("Which conflicting emotions are portrayed in the person's face?",
         "The video shows a combination of sadness and a forced smile, indicating mixed emotions."),
        ("How do the person's facial features reflect emotional inconsistency?",
         "Furrowed brows suggest anger, while a partial smile hints at underlying happiness."),
        ("What makes the emotional cues in this video contradictory?",
         "The person seems fearful with tense posture, but smiles intermittently."),
        ("Explain the emotional contrast observed in the video.",
         "Anger is evident from the person's jaw tension, yet their eyes show warmth.")
    ]
}

# Helper to infer emotion label from the answer
def infer_emotion(answer):
    for emotion in ['happy', 'fear', 'sad', 'angry', 'neutral']:
        if emotion in answer.lower():
            return emotion
    return "unknown"

# Function to generate and save annotations
def generate_annotations(category):
    folder = video_folders[category]
    templates = qa_templates_combined[category]
    annotations = []

    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.lower().endswith(('.mp4', '.avi', '.mov')):
                q1, a1 = random.choice(templates)
                emotion = infer_emotion(a1)
                q2 = "What is the primary emotion depicted in this video?"
                a2 = f"The emotion shown is {emotion}."
                annotations.append({
                    "video_id": filename,
                    "QA": [
                        {"q": q1, "a": a1},
                        {"q": q2, "a": a2}
                    ]
                })

    with open(output_paths[category], "w") as f:
        json.dump(annotations, f, indent=2)

# Generate for both categories
generate_annotations("Definitive")
generate_annotations("Opposing")

output_paths["Definitive"], output_paths["Opposing"]