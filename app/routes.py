import csv, os
from io import StringIO
from flask import render_template, flash, redirect, url_for
from flask import request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from app import app, db
from app.forms import LoginForm, ExportForm, RegistrationForm
from app.models import User, Scan, AdminView
from werkzeug.urls import url_parse
from sqlalchemy import and_
import xlsxwriter

def write_csv(data_list):
    # delete any possible old files
    os.system("rm -f /tmp/tmp.csv")
    with open("/tmp/tmp.csv", "w+") as csvfile:
        w = csv.writer(csvfile)
        # write header
        w.writerow(('timestamp', 'user', 'badge_id'))

        # write each log item
        for item in data_list:
            # in the db, the order will be: badge_id, user, timestamp
            # so reorder them here to match 
            w.writerow([
                item[2].isoformat(),  # format datetime as string
                item[1],
                item[0],
            ])
    return send_from_directory('/tmp/', 'tmp.csv',
         mimetype='text/csv',
         attachment_filename='scans.csv',
         as_attachment=True)

def write_xlsx(data_list):
    os.system("rm -f /tmp/tmp.xlsx")

    workbook = xlsxwriter.Workbook('/tmp/tmp.xlsx', {'in_memory': True})
    worksheet = workbook.add_worksheet('Door Access Report')

    worksheet.write_row(0, 0, (
        'First Name',
        'Last Name',
        'Card Number',
        'Event Date and Time',
        'Device Name',
        )
    )

    # There must be a more python-y way to do this, that uses data_list.count()
    index = 1
    name_map = {}
    for item in data_list:
        if item.username not in name_map:
            user = User.query.filter_by(username=item.username).first()
            name_map[item.username] = (user.first_name, user.last_name)

        worksheet.write_row(index, 0, (
            name_map[item.username][0],
            name_map[item.username][1],
            item.badge_id,
            item.timestamp.isoformat(),
            item.door_name,
            )
        )

        index += 1

    workbook.close()
    return send_from_directory('/tmp/', 'tmp.xlsx',
        mimetype='application/vnd.openxmlformates-offiedocument.spreadsheetml.sheet',
        attachment_filename='scans.xlsx',
        as_attachment=True)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# can get here without login, but it's empty
@app.route('/admin')
def admin():
    return render_template('admin.html', title='Admin')

@app.route('/export', methods=['GET', 'POST'])
@login_required
def download_log():
    form = ExportForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash( "Invalid data")
        else:
            start_time_dt =  form.start_date.data
            end_time_dt =  form.end_date.data
            # get all (scan, username, badge_id) records > start_time and < end_time
            desired_scans = Scan.query.filter(and_(Scan.timestamp >= start_time_dt,
                Scan.timestamp <= end_time_dt)).all()
            #return write_csv(desired_scans)
            list_of_scans = []
            for this_scan in desired_scans:
                list_of_scans.append(this_scan.to_list())

            if form.export_type.data == 'xlsx':
                return write_xlsx(desired_scans)
            elif form.export_type.data == 'csv':
                return write_csv(list_of_scans)
            else:
                flash("Invalid export type: '%s'" % form.export_type.data)
    return render_template('export.html', title='Export', form=form)

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


