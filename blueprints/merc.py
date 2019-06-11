
from flask import Blueprint, render_template, request as req, redirect, session
import models.model as model
merc = Blueprint('merc',__name__, template_folder="../templates", static_folder="../static")

@merc.route('/market', methods=['GET','POST'])
@merc.route('/store', methods=['GET','POST'])
def market():
    if model.get_info_player(session['username']):
        if req.args.get('buy', '') == "":
            hunterlist = model.hunterlist()
            infoplayer = model.get_info_player(session['username'])
            return render_template('system/hunterlist.html', data={'hunterlist': hunterlist, 'infoplayer': infoplayer})
        else:
            hunterid = req.args.get('buy', '')
            result = model.buyhunter(hunterid, session['username'])
            if result == True:
                return redirect('/market')
            else:
                return """
                Insufficent Cash<br>
                <a href='/market'>Back</a>
                """
    else:
        return "BAD USERNAME: {} not allowed, 403 FORBIDDEN, ".format(session['username']), 403

@merc.route('/members')
def myhunter():
    if model.get_info_player(session['username']):
        infoplayer = model.get_info_player(session['username'])
        hunterlist = model.myhunter( session['username'] )
        return render_template('player/myhunter.html', data={'hunterlist': hunterlist, 'infoplayer': infoplayer})
    else:
        return "BAD USERNAME: {} not allowed, 403 FORBIDDEN, ".format(session['username']), 403


@merc.route('/operations')
def operations():
    if model.get_info_player(session['username']):
        enemies = model.enemies()
        myhunter = model.myhunter( session['username'] )
        return render_template("system/operations.html", data={'enemies':enemies,'myhunter': myhunter})
    else:
        return "BAD USERNAME: {} not allowed, 403 FORBIDDEN, ".format(session['username']), 403


@merc.route('/fight')
def fight():
    if model.get_info_player(session['username']):
        enemy = req.args.get('enemy')
        hunter = req.args.get('hunter')

        battle_log, winner = model.fight(enemy,hunter, session['username'])
        return render_template('system/report.html', data={'log':battle_log, 'winner':winner})
    else:
        return "BAD USERNAME: {} not allowed, 403 FORBIDDEN, ".format(session['username']), 403

