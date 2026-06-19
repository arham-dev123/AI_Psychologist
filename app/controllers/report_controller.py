from flask import session, request, render_template, redirect, url_for, jsonify
from app import db, mail
from app.models.report import Report
from app.utils import get_severity_category, get_full_form
from flask_mail import Message


def _get_report_field(name, default='N/A', route_value=None):
    value = request.args.get(name, route_value if route_value is not None else default)
    return value if value else default


def get_report_message(form_type, severity_category):
    if form_type == 'no_anxiety':
        if severity_category == 'No significant anxiety symptoms indicated':
            return 'Your responses suggest no significant anxiety symptoms at this time. This result is not a medical diagnosis.'

        return 'Although the initial prediction was No Anxiety Disorder, your responses show some anxiety symptoms. Please complete a specific anxiety screening or consult a mental health professional.'

    return 'This assessment result is based on your self-report responses. This result is not a medical diagnosis.'


RECOMMENDATION_SETS = {
    'gad': {
        'title': 'Personalized Support Plan for General Anxiety Disorder',
        'summary': 'These recommendations focus on reducing excessive worry, improving stress tolerance, and building a steady daily routine.',
        'sections': [
            {
                'heading': 'Daily coping techniques',
                'items': [
                    'Use a short scheduled worry period, then redirect attention to one practical next step.',
                    'Practice slow breathing, mindfulness, or muscle relaxation for a few minutes each day.',
                    'Break large responsibilities into smaller tasks and write down the next action only.'
                ]
            },
            {
                'heading': 'Healthy habits',
                'items': [
                    'Keep a regular sleep schedule and protect wind-down time before bed.',
                    'Add light movement such as walking, stretching, or other exercise you can repeat consistently.',
                    'Eat regular meals, stay hydrated, and notice whether caffeine increases worry or restlessness.'
                ]
            },
            {
                'heading': 'Avoid and monitor',
                'items': [
                    'Avoid repeatedly checking, reassurance-seeking, or researching worries when it increases anxiety.',
                    'Limit alcohol, nicotine, and excessive caffeine if they worsen sleep, tension, or anxious thoughts.',
                    'Seek professional support if worry starts interfering with work, study, relationships, sleep, or daily functioning.'
                ]
            }
        ]
    },
    'sad': {
        'title': 'Personalized Support Plan for Social Anxiety Disorder',
        'summary': 'These recommendations focus on confidence-building, gradual social practice, and reducing avoidance in a supportive way.',
        'sections': [
            {
                'heading': 'Daily coping techniques',
                'items': [
                    'Practice one small social step at a time, such as greeting someone, asking a simple question, or joining a brief conversation.',
                    'Prepare balanced self-talk before social situations, then review what went well afterward.',
                    'Use slow breathing before social interactions to lower physical tension.'
                ]
            },
            {
                'heading': 'Healthy habits',
                'items': [
                    'Stay connected with trusted family or friends who can offer steady support.',
                    'Keep sleep, meals, hydration, and exercise consistent to support emotional regulation.',
                    'Build social confidence gradually instead of forcing sudden high-pressure exposure.'
                ]
            },
            {
                'heading': 'Avoid and monitor',
                'items': [
                    'Avoid withdrawing from all social contact, because avoidance can keep fear strong over time.',
                    'Avoid judging progress by perfection; small steps and repeated practice matter.',
                    'Consider professional help if fear of judgment causes school, work, family, or friendship avoidance.'
                ]
            }
        ]
    },
    'pd': {
        'title': 'Personalized Support Plan for Panic Disorder',
        'summary': 'These recommendations focus on panic attack management, trigger awareness, and reducing fear of body sensations.',
        'sections': [
            {
                'heading': 'Daily coping techniques',
                'items': [
                    'During panic sensations, remind yourself that symptoms usually pass and focus on slow, steady breathing.',
                    'Track possible triggers, body sensations, sleep, caffeine, and stressful events to identify patterns.',
                    'Practice grounding by naming what you see, hear, and feel in the present moment.'
                ]
            },
            {
                'heading': 'Healthy habits',
                'items': [
                    'Maintain regular sleep and movement routines to reduce baseline physical tension.',
                    'Use relaxation practice when calm, not only during panic, so the skill becomes familiar.',
                    'Discuss repeated panic symptoms with a qualified health professional, especially if physical symptoms are new or concerning.'
                ]
            },
            {
                'heading': 'Avoid and monitor',
                'items': [
                    'Avoid avoiding every place connected with a previous panic attack; gradual re-entry may help reduce fear.',
                    'Limit caffeine, nicotine, alcohol, or other substances if they trigger racing heart, poor sleep, or anxiety spikes.',
                    'Seek professional help if panic attacks are repeated, unexpected, or causing major behavior changes.'
                ]
            }
        ]
    },
    'ptsd': {
        'title': 'Personalized Support Plan for Post-Traumatic Stress Symptoms',
        'summary': 'These recommendations focus on safety, grounding, emotional support, and healthy coping after trauma-related stress.',
        'sections': [
            {
                'heading': 'Daily coping techniques',
                'items': [
                    'Use grounding during distress: look around, name where you are, and remind yourself that the trauma is not happening now.',
                    'Try small doses of relaxation such as breathing, stretching, quiet music, or time in nature.',
                    'Plan calming activities after difficult reminders, dreams, or intrusive memories.'
                ]
            },
            {
                'heading': 'Healthy habits',
                'items': [
                    'Stay connected with carefully chosen trusted people instead of isolating when symptoms increase.',
                    'Keep a predictable sleep routine and reduce alcohol, tobacco, and caffeine if they worsen sleep.',
                    'Use creative, recreational, or meaningful activities to rebuild routine and positive mood.'
                ]
            },
            {
                'heading': 'Avoid and monitor',
                'items': [
                    'Avoid using alcohol or substances to numb trauma reminders, because this can worsen recovery over time.',
                    'Do not force yourself to discuss traumatic details before you feel safe and supported.',
                    'Consider trauma-informed professional support if symptoms persist, worsen, or interfere with relationships, sleep, work, or daily life.'
                ]
            }
        ]
    },
    'no_anxiety': {
        'title': 'Wellness Recommendations for Continued Emotional Health',
        'summary': 'This assessment does not indicate significant anxiety symptoms. These recommendations support continued mental wellbeing and resilience.',
        'sections': [
            {
                'heading': 'Maintain wellbeing',
                'items': [
                    'Continue regular sleep, balanced meals, hydration, and physical activity.',
                    'Schedule relaxing activities you enjoy, such as reading, music, walking, prayer, meditation, or time in nature.',
                    'Stay connected with supportive friends, family, or trusted people in your community.'
                ]
            },
            {
                'heading': 'Build resilience',
                'items': [
                    'Set realistic priorities and allow yourself to say no when commitments become too heavy.',
                    'Practice gratitude or positive reflection to notice what is going well.',
                    'Use brief breathing or mindfulness exercises during normal stressful days.'
                ]
            },
            {
                'heading': 'When to check in',
                'items': [
                    'Pay attention to major changes in sleep, appetite, concentration, mood, or daily functioning.',
                    'Reach out early to a trusted person or health professional if distress lasts or begins affecting daily life.',
                    'Keep using healthy habits even when you feel well; prevention and consistency are protective.'
                ]
            }
        ]
    }
}


def get_recommendations(form_type):
    return RECOMMENDATION_SETS.get(form_type, RECOMMENDATION_SETS['gad'])


def share_report():
    recipient_email = request.form.get('recipientEmail')
    pdf_file = request.files.get('pdfBytes')

    if not pdf_file:
        return jsonify({'error': 'PDF file not provided'}), 400

    pdf_bytes = pdf_file.read()

    message = Message('PDF Report', sender='your-email@example.com', recipients=[recipient_email])
    message.body = 'Please find attached the PDF report.'
    message.attach(filename='report.pdf', content_type='application/pdf', data=pdf_bytes)

    try:
        mail.send(message)
        return jsonify({'message': 'Email sent successfully!'})
    except Exception as e:
        print(f'An error occurred: {e}')
        return jsonify({'error': 'Error sending email'}), 500


def save_report(total_score=None, first_name=None, last_name=None, age=None, form_type=None):
    user_email = session.get('email')
    total_score = int(request.args.get('total_score', total_score or 0))
    form_type = _get_report_field('form_type', route_value=form_type)
    first_name = _get_report_field('first_name', route_value=first_name)
    last_name = _get_report_field('last_name', route_value=last_name)
    age = _get_report_field('age', route_value=age)
    contact_number = _get_report_field('contact_number')
    height = _get_report_field('height')
    weight = _get_report_field('weight')
    blood_group = _get_report_field('blood_group')
    date_of_birth = _get_report_field('date_of_birth')
    issue_date = _get_report_field('issue_date')
    gender = _get_report_field('gender')
    nationality = _get_report_field('nationality')
    severity_category = get_severity_category(form_type, total_score)

    report = Report(
        user_email,
        first_name,
        last_name,
        age,
        contact_number,
        height,
        weight,
        blood_group,
        date_of_birth,
        issue_date,
        gender,
        nationality,
        form_type,
        total_score,
        severity_category
    )
    report.save()

    return redirect(url_for(
        'report.view_report',
        total_score=total_score,
        first_name=first_name,
        last_name=last_name,
        age=age,
        contact_number=contact_number,
        height=height,
        weight=weight,
        blood_group=blood_group,
        date_of_birth=date_of_birth,
        issue_date=issue_date,
        gender=gender,
        nationality=nationality,
        form_type=form_type
    ))


def view_report(total_score=None, first_name=None, last_name=None, age=None, form_type=None):
    total_score = int(request.args.get('total_score', total_score or 0))
    form_type = _get_report_field('form_type', route_value=form_type)
    first_name = _get_report_field('first_name', route_value=first_name)
    last_name = _get_report_field('last_name', route_value=last_name)
    age = _get_report_field('age', route_value=age)
    contact_number = _get_report_field('contact_number')
    height = _get_report_field('height')
    weight = _get_report_field('weight')
    blood_group = _get_report_field('blood_group')
    date_of_birth = _get_report_field('date_of_birth')
    issue_date = _get_report_field('issue_date')
    gender = _get_report_field('gender')
    nationality = _get_report_field('nationality')
    severity_category = get_severity_category(form_type, total_score)
    predicted_class = get_full_form(form_type)[0]
    report_message = get_report_message(form_type, severity_category)
    recommendations = get_recommendations(form_type)
    return render_template(
        'report.html',
        total_score=total_score,
        first_name=first_name,
        last_name=last_name,
        age=age,
        contact_number=contact_number,
        height=height,
        weight=weight,
        blood_group=blood_group,
        date_of_birth=date_of_birth,
        issue_date=issue_date,
        gender=gender,
        nationality=nationality,
        form_type=predicted_class,
        raw_form_type=form_type,
        severity_category=severity_category,
        report_message=report_message,
        recommendations=recommendations
    )


def delete_report(report_id):
    user_email = session.get('email')
    if not user_email:
        return jsonify({'success': False}), 403

    success = Report.delete_report(report_id, user_email)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 404


def report_management():
    user_email = session.get('email')
    if user_email:
        page = int(request.args.get('page', 1))
        user_reports, total_pages = Report.get_user_reports(user_email, page)
        return render_template('reportManagement.html', reports=user_reports, current_page=page, total_pages=total_pages)
    else:
        return redirect(url_for('auth.login'))
