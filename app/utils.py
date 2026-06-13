import torch
from app import db
from app import tokenizer, model
from collections import defaultdict
import re  # added for validation


def predict(conversation):
    inputs = tokenizer(
        conversation,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)

    confidence = torch.max(probs).item()

    predicted_class_idx = probs.argmax().item()
    predicted_class = model.config.id2label[predicted_class_idx]

    print("Predicted Class:", predicted_class)
    print("Confidence:", confidence)

    return predicted_class


def get_chat_questions():
    questions_collection = db['modelquestions']
    questions_docs = questions_collection.find({})
    return [doc['question_text'] for doc in questions_docs]


def clean_conversation(text):
    if not text.endswith('.'):
        text += '.'
    lower_text = text.lower().replace(',', '')
    return lower_text


def clean_conversations(conversations):
    cleaned_conversations = [clean_conversation(conv) for conv in conversations]
    return " ".join(cleaned_conversations)


def calculate_total_score(form_data):
    total_score = 0
    for answer in form_data['answers']:
        total_score += int(answer)
    return total_score


def get_severity_category(form_type, total_score):
    conditions = SEVERITY_CONDITIONS.get(form_type, {})
    for severity, score_range in conditions.items():
        if total_score in score_range:
            return severity.capitalize()
    return "Invalid Score"


SEVERITY_CONDITIONS = {
    'gad': {
        'minimal': range(0, 5),
        'mild': range(5, 10),
        'moderate': range(10, 15),
        'severe': range(15, 22)
    },
    'sad': {
        'minimal': range(0, 10),
        'mild': range(10, 20),
        'moderate': range(20, 30),
        'severe': range(30, 40)
    },
    'pd': {
        'minimal': range(0, 10),
        'mild': range(10, 20),
        'moderate': range(20, 30),
        'severe': range(30, 40)
    },
    'ptsd': {
        'minimal': range(0, 16),
        'mild': range(16, 32),
        'moderate': range(32, 48),
        'severe': range(48, 64)
    },
    'no_anxiety': {
        'no significant anxiety symptoms indicated': range(0, 5),
        'anxiety symptoms present - further screening recommended': range(5, 31)
    }
}


LABEL_MAPPING = {
    'General Anxiety Disorder': 'gad',
    'Social Anxiety Disorder': 'sad',
    'Panic Disorder': 'pd',
    'Post Traumatic Stress Disorder': 'ptsd',
    'PTSD': 'ptsd',
    'GAD': 'gad',
    'No Anxiety Disorder': 'no_anxiety',
    'No Anxiety': 'no_anxiety',
    'No Anxiety Symptoms': 'no_anxiety',
}


REVERSE_LABEL_MAPPING = defaultdict(list)

for full_form, short_form in LABEL_MAPPING.items():
    REVERSE_LABEL_MAPPING[short_form].append(full_form)


def get_full_form(short_form_label):
    return REVERSE_LABEL_MAPPING.get(short_form_label, ['default'])


def is_valid_user_input(text: str) -> bool:
    if not text:
        return False

    text = text.strip()

    if len(text) < 20:
        return False

    has_english_letter = any(
        ch.isalpha() and ch.lower() in "abcdefghijklmnopqrstuvwxyz"
        for ch in text
    )

    if not has_english_letter:
        return False

    if len(text.split()) < 5:
        return False

    return True
