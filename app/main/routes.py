import datetime
import calendar
from flask import render_template, url_for, redirect, jsonify, request
#from flask_weasyprint import HTML
from gsheet import authentication, get_row, get_all, get_new, get_id, entry_update
from app.main import bp
import app


@bp.route('/')
@bp.route('/index')
def index():
    legs = get_new(range="Legs!A:Y")
    regs = get_new(range="Regs!A:Y")
    consultation = get_new(range="Consultations!A:Y")
    return render_template('index.html', legs=legs, regs=regs, consultation=consultation)

@bp.route('/legs/<id>')
def legs(id):
    history = get_id(str(id), range="Legs!A:Y")
    entry_base = history[0]
    entry_history = []
    entry_update(history=history, entry_base=entry_base, entry_history=entry_history)
    return render_template('legislation.html', entry_base=entry_base, entry_history=entry_history)

@bp.route('/regs/<id>')
def regs(id):
    history = get_id(str(id), range="Regs!A:Y")
    entry_base = history[0]
    entry_history = []
    entry_update(history=history, entry_base=entry_base, entry_history=entry_history)
    enforcement_date = datetime.date(int(entry_base["enforcement_year"]),
                                     list(calendar.month_name).index(entry_base["enforcement_month"]), 1)
    enforcement = {"date": enforcement_date, "now":datetime.date.today()}
    return render_template('regulation.html', entry_base=entry_base, entry_history=entry_history, enforcement=enforcement)

@bp.route('/consultation/<id>')
def consultation(id):
    history = get_id(str(id), range="Consultations!A:Y")
    entry_base = history[0]
    entry_history = []
    closed = False
    entry_update(history=history, entry_base=entry_base, entry_history=entry_history)
    for x in entry_history:
        if x["step"] == "Closed":
            closed = True
    return render_template('consultation.html', entry_base=entry_base, entry_history=entry_history, closed=closed)

"""@bp.route('/create_report/<id>')
def create_report(id):
    legislation = get_row(str(id))

    return render_template('report.html', legislation = legislation)
@bp.route('/report/<id>')
def report(id):
    legislation = get_row(str(id))
    pdf = HTML(url_for('main.create_report', id=id)).write_pdf()
    with open('test.pdf', 'wb') as save_pdf:
        save_pdf.write(pdf)

    return render_template('report.html', legislation = legislation)"""