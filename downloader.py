#!/usr/bin/env python

import sys
import os
from pexpect import run
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'I Want To DownLoad Youtube Video!'
bootstrap = Bootstrap(app)
manager = Manager(app)


class SearchForm(Form):
    url = StringField("just tell me the youtube url!", validators=[DataRequired()])
    submit = SubmitField("submit")


class DownloadForm(Form):
    video_type1 = StringField('video code?', validators=[DataRequired()])
    video_type2 = StringField('audio code?', validators=[DataRequired()])
    submit = SubmitField("download!")


@app.route('/show')
def show():
    show_dir = os.listdir('/download')
    return render_template('show.html', show_dir=show_dir)


@app.route('/download', methods=['GET', 'POST'])
def download():
    video_type1, video_type2 = None, None
    form = DownloadForm()
    if form.validate_on_submit():
        video_type1 = form.video_type1.data
        video_type2 = form.video_type2.data
        url = session.get('url')
        os.chdir("/download")
        run("youtube-dl -f  %s+%s %s" %(video_type1, video_type2, url))
        flash('success!')
        return redirect(url_for('show'))
    return render_template('download.html', form=form, video_list=session.get('video_list'))


@app.route('/', methods=['GET', 'POST'])
def index():
    url = None
    form = SearchForm()
    if form.validate_on_submit():
        url = form.url.data
        video_list = os.popen("youtube-dl -F %s" %url)
        video_line = video_list.readlines()
        session['video_list'] = video_line[5:]
        session['url'] = url
        return redirect(url_for('download'))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    manager.run()
