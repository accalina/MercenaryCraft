
from flask import Blueprint, render_template, request as req, redirect, session
import models.model as model
merc = Blueprint('merc',__name__, template_folder="../templates", static_folder="../static")

@merc.route('/market', methods=['GET','POST'])
@merc.route('/store', methods=['GET','POST'])
def market():
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

@merc.route('/members')
def myhunter():
    infoplayer = model.get_info_player(session['username'])
    hunterlist = model.myhunter( session['username'] )
    return render_template('player/myhunter.html', data={'hunterlist': hunterlist, 'infoplayer': infoplayer})


@merc.route('/operations')
def operations():
    enemies = model.enemies()
    myhunter = model.myhunter( session['username'] )
    return render_template("system/operations.html", data={'enemies':enemies,'myhunter': myhunter})


@merc.route('/fight')
def fight():
    enemy = req.args.get('enemy')
    hunter = req.args.get('hunter')

    battle_log, winner = model.fight(enemy,hunter, session['username'])
    return render_template('system/report.html', data={'log':battle_log, 'winner':winner})

