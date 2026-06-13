import random
import uuid
from flask import session, request, redirect, url_for, render_template
from app.utils import (
    get_chat_questions,
    clean_conversations,
    LABEL_MAPPING,
    predict,
    is_valid_user_input
)

chat_conversations = {}


def chat():
    if "email" not in session:
        return redirect(url_for('auth.login', next='/chat'))

    if request.method == 'GET':
        chat_session_id = str(uuid.uuid4())
        session['chat_session_id'] = chat_session_id

        chat_conversations[chat_session_id] = {
            'user_responses': [],
            'conversation_history': [],
            'chat_ended': False,
            'waiting_for_ok': False
        }

        questions = get_chat_questions()

        greeting = random.choice([
            "Hello! I am your AI Psychologist",
            "Hi there! I am your AI Psychologist",
            "Greetings! I am your AI Psychologist"
        ])

        chat_conversations[chat_session_id]['conversation_history'].append({
            'sender': 'AI Psychologist',
            'message': greeting
        })

        chat_conversations[chat_session_id]['conversation_history'].append({
            'sender': 'AI Psychologist',
            'message': 'Welcome, I am here to understand your experiences and how they are affecting you. Everything you share will be confidential.'
        })

        chat_conversations[chat_session_id]['conversation_history'].append({
            'sender': 'AI Psychologist',
            'message': "Please answer in a few sentences. Avoid yes/no."
        })

        if questions:
            chat_conversations[chat_session_id]['conversation_history'].append({
                'sender': 'AI Psychologist',
                'message': questions[0]
            })
        else:
            chat_conversations[chat_session_id]['conversation_history'].append({
                'sender': 'AI Psychologist',
                'message': "No questions are available right now. Please contact support."
            })

        return render_template(
            'chat.html',
            username=session.get('name', 'User'),
            messages=chat_conversations[chat_session_id]['conversation_history']
        )

    elif request.method == 'POST':
        chat_session_id = session.get('chat_session_id')

        if not chat_session_id or chat_session_id not in chat_conversations:
            return redirect(url_for('chat.chat'))

        user_response = request.form.get('message', '').strip()

        if chat_conversations[chat_session_id]['waiting_for_ok']:
            if user_response.lower() == "ok":
                return redirect(url_for(
                    'form.form',
                    form_type=chat_conversations[chat_session_id]['predicted_label']
                ))

            chat_conversations[chat_session_id]['conversation_history'].append({
                'sender': 'AI Psychologist',
                'message': "Type 'ok' to proceed to the self-report assessment."
            })

            return render_template(
                'chat.html',
                username=session.get('name', 'User'),
                messages=chat_conversations[chat_session_id]['conversation_history']
            )

        if not is_valid_user_input(user_response):
            chat_conversations[chat_session_id]['conversation_history'].append({
                'sender': 'AI Psychologist',
                'message': "Please explain properly in 2–3 lines so I can understand your condition."
            })

            return render_template(
                'chat.html',
                username=session.get('name', 'User'),
                messages=chat_conversations[chat_session_id]['conversation_history']
            )

        chat_conversations[chat_session_id]['user_responses'].append(user_response)
        chat_conversations[chat_session_id]['conversation_history'].append({
            'sender': 'User',
            'message': user_response
        })

        questions = get_chat_questions()
        num_answered = len(chat_conversations[chat_session_id]['user_responses'])

        if num_answered < len(questions):
            chat_conversations[chat_session_id]['conversation_history'].append({
                'sender': 'AI Psychologist',
                'message': questions[num_answered]
            })

        elif num_answered == len(questions):
            cleaned_text = clean_conversations(
                chat_conversations[chat_session_id]['user_responses']
            )
            predicted_label = predict(cleaned_text)

            short_label = LABEL_MAPPING.get(predicted_label, 'gad')
            chat_conversations[chat_session_id]['predicted_label'] = short_label
            chat_conversations[chat_session_id]['waiting_for_ok'] = True

            chat_conversations[chat_session_id]['conversation_history'].append({
                'sender': 'AI Psychologist',
                'message': f"Predicted disorder: {predicted_label}. Type 'ok' to continue to the self-report assessment."
            })

        return render_template(
            'chat.html',
            username=session.get('name', 'User'),
            messages=chat_conversations[chat_session_id]['conversation_history']
        )