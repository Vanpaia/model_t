from flask import render_template, url_for, redirect, jsonify, request
from flask_weasyprint import HTML
from gsheet import authentication, get_row, get_all, get_id
from app.main import bp
import app

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/legs/<id>')
def legs(id):
    history = get_id(str(id))
    legislation_base = history[0]
    legislation_history = []
    for x in history:
        if x["nature"] == "Update":
            if len(x["related_id"]) > 0:
                legislation_base["related_id"] = x["related_id"]
            elif len(x["document_id"]) > 0:
                legislation_base["document_id"] = x["document_id"]
            elif len(x["native_title"]) > 0:
                legislation_base["native_title"] = x["native_title"]
            elif len(x["title"]) > 0:
                legislation_base["title"] = x["title"]
            elif len(x["initiative_type"]) > 0:
                legislation_base["initiative_type"] = x["initiative_type"]
            elif len(x["legally_binding"]) > 0:
                legislation_base["legally_binding"] = x["legally_binding"]
            elif len(x["issue"]) > 0:
                legislation_base["issue"] = x["issue"]
            elif len(x["sub_issue"]) > 0:
                legislation_base["sub_issue"] = x["sub_issue"]
            elif len(x["likelihood"]) > 0:
                legislation_base["likelihood"] = x["likelihood"]
            elif len(x["impact_score"]) > 0:
                legislation_base["impact_score"] = x["impact_score"]
            elif len(x["adoption_year"]) > 0:
                legislation_base["adoption_year"] = x["adoption_year"]
            elif len(x["adoption_month"]) > 0:
                legislation_base["adoption_month"] = x["adoption_month"]
            elif len(x["enforcement_year"]) > 0:
                legislation_base["enforcement_year"] = x["enforcement_year"]
            elif len(x["enforcement_month"]) > 0:
                legislation_base["enforcement_month"] = x["enforcement_month"]
            elif len(x["relevant_links"]) > 0:
                legislation_base["relevant_links"] = x["relevant_links"]
            elif len(x["date_first_introduction"]) > 0:
                legislation_base["date_first_introduction"] = x["date_first_introduction"]
    return render_template('legislation.html', legislation_base = legislation_base)

@bp.route('/create_report/<id>')
def create_report(id):
    legislation = get_row(str(id))

    return render_template('report.html', legislation = legislation)
@bp.route('/report/<id>')
def report(id):
    legislation = get_row(str(id))
    pdf = HTML(url_for('main.create_report', id=id)).write_pdf()
    with open('test.pdf', 'wb') as save_pdf:
        save_pdf.write(pdf)

    return render_template('report.html', legislation = legislation)