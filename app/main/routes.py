import datetime
import calendar
from json import loads
from flask import render_template, url_for, redirect, jsonify, request
#from flask_weasyprint import HTML
from gsheet import authentication, get_row, get_all, get_new, get_id, entry_update, get_country
from app.main import bp
import app


@bp.route('/')
@bp.route('/index')
def index():
    all = get_all()
    legs = get_new(range="Legs!A:Y")
    regs = get_new(range="Regs!A:Y")
    consultation = get_new(range="Consultations!A:Y")
    latest_addition = loads(all.loc[all['nature'].str.contains("New")].sort_values("date_entry").iloc[:5].to_json(orient="records"))
    latest_development = loads(all.loc[all['nature'].str.contains("Update")].sort_values("date_entry").iloc[:5].to_json(orient="records"))
    for x in latest_development:
        main = all.loc[all['internal_id'].str.contains(x['internal_id'])].loc[all['nature'].str.contains('New')]
        x["country"] = main.iloc[0]['country']
        x["title"] = main.iloc[0]['title']
        x["initiative_type"] = main.iloc[0]['initiative_type']
    return render_template('index.html', legs=legs, regs=regs, consultation=consultation, latest_addition=latest_addition, latest_development=latest_development)

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

@bp.route('/jurisdiction/<country>')
def jurisdiction(country):
    information = get_country(str(country))
    data = get_all()
    all = data.loc[data['country'].str.contains(country)]
    legs = loads(all.loc[all['nature'].str.contains("New")].loc[all['initiative_type'].str.contains("Legislative Process")].to_json(orient="records"))
    regs = loads(all.loc[all['nature'].str.contains("New")].loc[all['initiative_type'].str.contains("Regulatory Process")].to_json(orient="records"))
    consultation = loads(all.loc[all['nature'].str.contains("New")].loc[all['initiative_type'].str.contains("Public Consultation/Hearing")].to_json(orient="records"))
    latest_addition = loads(all.loc[all['nature'].str.contains("New")].sort_values("date_entry").iloc[:5].to_json(orient="records"))
    latest_development = loads(all.loc[all['nature'].str.contains("Update")].sort_values("date_entry").iloc[:5].to_json(orient="records"))
    for x in latest_development:
        main = all.loc[all['internal_id'].str.contains(x['internal_id'])].loc[all['nature'].str.contains('New')]
        x["country"] = main.iloc[0]['country']
        x["title"] = main.iloc[0]['title']
        x["initiative_type"] = main.iloc[0]['initiative_type']

    return render_template('jurisdiction.html', information=information[0], legs=legs, regs=regs, consulation=consultation, latest_addition=latest_addition, latest_development=latest_development)


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