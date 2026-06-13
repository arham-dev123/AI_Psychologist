from math import ceil

from flask import app
from app import db
from datetime import datetime
from bson import ObjectId

# from config import Config

class Report:
    def __init__(
        self,
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
    ):
        self.user_email = user_email
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.contact_number = contact_number
        self.height = height
        self.weight = weight
        self.blood_group = blood_group
        self.date_of_birth = date_of_birth
        self.issue_date = issue_date
        self.gender = gender
        self.nationality = nationality
        self.form_type = form_type
        self.total_score = total_score
        self.severity_category = severity_category
        self.date = datetime.now()

    def save(self):
        collection = db['reports']
        report_data = {
            'user_email': self.user_email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'contact_number': self.contact_number,
            'height': self.height,
            'weight': self.weight,
            'blood_group': self.blood_group,
            'date_of_birth': self.date_of_birth,
            'issue_date': self.issue_date,
            'gender': self.gender,
            'nationality': self.nationality,
            'form_type': self.form_type,
            'total_score': self.total_score,
            'severity_category': self.severity_category,
            'date': self.date
        }
        collection.insert_one(report_data)

    @staticmethod
    def get_user_reports(user_email, page=1):
        collection = db['reports']
        total_reports = collection.count_documents({'user_email': user_email})
        total_pages = ceil(total_reports / 6)

        start_index = (page - 1) * 6
        user_reports = list(collection.find({'user_email': user_email}).skip(start_index).limit(6))

        return user_reports, total_pages

    @staticmethod
    def delete_report(report_id, user_email):
        collection = db['reports']
        result = collection.delete_one({'_id': ObjectId(report_id), 'user_email': user_email})
        return result.deleted_count > 0
