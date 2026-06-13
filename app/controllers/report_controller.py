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
        report_message=report_message
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
