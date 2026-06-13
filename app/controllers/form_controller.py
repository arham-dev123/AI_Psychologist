from flask import redirect, request, jsonify, render_template, url_for
from app import db
from app.utils import calculate_total_score

def get_form(form_type):
    form_data = db.severity_forms.find_one({form_type: {"$exists": True}}, {form_type: 1, '_id': 0})
    if form_data:
        content = form_data[form_type]
        
        # Normalize the content if it's a list (missing options and 'questions' key wrapper)
        if isinstance(content, list):
            normalized_questions = []
            for item in content:
                text = item.get('questions', item.get('text', ''))
                options = item.get('options', [
                    {"text": "Not at all", "value": "0"},
                    {"text": "Several days", "value": "1"},
                    {"text": "More than half the days", "value": "2"},
                    {"text": "Nearly every day", "value": "3"}
                ])
                normalized_questions.append({
                    "text": text,
                    "options": options
                })
            content = {"questions": normalized_questions}
        elif isinstance(content, dict) and "questions" in content:
            normalized_questions = []
            for item in content["questions"]:
                text = item.get('questions', item.get('text', ''))
                options = item.get('options', [
                    {"text": "Not at all", "value": "0"},
                    {"text": "Several days", "value": "1"},
                    {"text": "More than half the days", "value": "2"},
                    {"text": "Nearly every day", "value": "3"}
                ])
                normalized_questions.append({
                    "text": text,
                    "options": options
                })
            content["questions"] = normalized_questions
            
        return jsonify({form_type: content})
        
    else:
        return jsonify({"error": "Form not found"}), 404

def form(form_type):
    # form_type = request.args.get('form_type', 'gad') 
    return render_template('form.html', formType=form_type)

def submit_form():
    form_data = request.get_json()
    answers = form_data.get('answers', [])
    form_type = form_data.get('formType')

    total_score = calculate_total_score(form_data)

    return jsonify({'totalScore': total_score, 'formType': form_type})

def details(total_score, form_type):
    if request.method == "POST":
        report_fields = {
            'total_score': total_score,
            'form_type': form_type,
            'first_name': request.form.get('first_name', '').strip(),
            'last_name': request.form.get('last_name', '').strip(),
            'age': request.form.get('age', '').strip(),
            'contact_number': request.form.get('contact_number', '').strip(),
            'height': request.form.get('height', '').strip(),
            'weight': request.form.get('weight', '').strip(),
            'blood_group': request.form.get('blood_group', '').strip(),
            'date_of_birth': request.form.get('date_of_birth', '').strip(),
            'issue_date': request.form.get('issue_date', '').strip(),
            'gender': request.form.get('gender', '').strip(),
            'nationality': request.form.get('nationality', '').strip()
        }
        redirect_url = url_for('report.save_report', **report_fields)
        return redirect(redirect_url)
    else:
        return render_template('details.html', total_score=total_score, form_type=form_type)
