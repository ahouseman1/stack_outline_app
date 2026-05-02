from flask import Blueprint, render_template

from .models import Techs
from .models import Users
from .models import Inventory
from .models import Tickets

main = Blueprint("main", __name__)


@main.route("/")
def createticket():
    records = Techs.query.order_by(Techs.techEmployeeID.desc()).all()
    return render_template("createticket.html", records=records)
