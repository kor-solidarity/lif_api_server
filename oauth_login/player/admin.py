from flask import redirect, url_for, flash, render_template, request
from ..player.models import *
import json
from oauth_login import app, login_manager


@app.route('/admin/crew')
def crew_admin():
    """
    make admin page on crew.

    :return:
    """
    return
