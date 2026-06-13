from datetime import datetime, timedelta
import secrets

from flask import current_app, session, redirect, url_for, request, render_template
from flask_mail import Message
from app import mail
from app.models.user import User


RESET_CODE_EXPIRY_MINUTES = 10


def _generate_otp_code():
    return f"{secrets.randbelow(1000000):06d}"


def _clear_reset_session():
    session.pop('password_reset_email', None)
    session.pop('password_reset_verified', None)


def _is_mail_configured():
    return bool(
        current_app.config.get('MAIL_SERVER')
        and current_app.config.get('MAIL_USERNAME')
        and current_app.config.get('MAIL_PASSWORD')
    )


def _send_password_reset_email(recipient_email, otp_code):
    subject = 'AI Psychologist Password Reset Code'
    body = (
        'You requested to reset your password.\n\n'
        f'Please enter this code to continue: {otp_code}\n\n'
        f'This code will expire in {RESET_CODE_EXPIRY_MINUTES} minutes. '
        'If you did not request this, you can safely ignore this email.'
    )

    if not _is_mail_configured():
        print(f"[LOCAL PASSWORD RESET OTP] {recipient_email}: {otp_code}")
        return False

    try:
        message = Message(subject=subject, recipients=[recipient_email], body=body)
        mail.send(message)
        return True
    except Exception as error:
        current_app.logger.warning('Password reset email could not be sent: %s', error)
        return False

def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.authenticate(email, password)
        if user:
            session['email'] = user['email']
            session['name'] = user['name']
            next_url = request.form.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect(url_for("main.dashboard"))
        else:
            return render_template('login.html', error='Invalid email or password')
    else:
        if 'email' in session:
            return redirect(url_for('main.dashboard'))
        return render_template('login.html')

def logout():
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('main.home'))

def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(name, email, password)
        if user.save():
            return render_template('signup.html', response="Registration successful")
        else:
            return render_template('signup.html', response="Email already exists")
    return render_template('signup.html')


def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')

    email = request.form.get('email', '').strip()
    if not email:
        return render_template('forgot_password.html', error='Please enter your registered email address.')

    user = User.find_by_email(email)
    safe_message = 'If an account exists for this email, a password reset code has been sent.'

    if not user:
        _clear_reset_session()
        return render_template('forgot_password.html', success=safe_message)

    otp_code = _generate_otp_code()
    expires_at = datetime.utcnow() + timedelta(minutes=RESET_CODE_EXPIRY_MINUTES)
    User.save_password_reset_code(email, otp_code, expires_at)
    _send_password_reset_email(email, otp_code)

    session['password_reset_email'] = email
    session['password_reset_verified'] = False

    return redirect(url_for('auth.verify_reset_code'))


def verify_reset_code():
    reset_email = session.get('password_reset_email')
    if not reset_email:
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'GET':
        return render_template('verify_reset_code.html', email=reset_email)

    otp_code = request.form.get('otp_code', '').strip()
    if not (otp_code.isdigit() and len(otp_code) == 6):
        return render_template(
            'verify_reset_code.html',
            email=reset_email,
            error='Enter the 6-digit code sent to your email.'
        )

    is_valid, status = User.verify_password_reset_code(reset_email, otp_code)

    if not is_valid:
        if status == 'expired':
            _clear_reset_session()
            return render_template(
                'verify_reset_code.html',
                email=reset_email,
                error='This reset code has expired. Please request a new code.'
            )

        return render_template(
            'verify_reset_code.html',
            email=reset_email,
            error='The reset code is incorrect. Please check your email and try again.'
        )

    session['password_reset_verified'] = True
    return redirect(url_for('auth.reset_password'))


def reset_password():
    reset_email = session.get('password_reset_email')
    reset_verified = session.get('password_reset_verified')

    if not reset_email:
        return redirect(url_for('auth.forgot_password'))

    if not reset_verified:
        return redirect(url_for('auth.verify_reset_code'))

    if not User.has_active_password_reset(reset_email):
        _clear_reset_session()
        return render_template(
            'forgot_password.html',
            error='Your reset session has expired. Please request a new code.'
        )

    if request.method == 'GET':
        return render_template('reset_password.html')

    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if len(new_password) < 8:
        return render_template('reset_password.html', error='Password must be at least 8 characters long.')

    if new_password != confirm_password:
        return render_template('reset_password.html', error='New password and confirmation password do not match.')

    User.update_password(reset_email, new_password)
    _clear_reset_session()

    return redirect(url_for('auth.login', reset='success'))
