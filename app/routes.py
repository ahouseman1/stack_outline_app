from flask import Blueprint, redirect, render_template, request, url_for

from .models import Techs
from .models import Users
from .models import Inventory
from .models import Tickets

main = Blueprint("main", __name__)


@main.route("/", methods=["GET","POST"])
def createticket():
    if request.method == "POST":
        userID = request.form.get("userID")

        if not userID:
            return "Please select a user", 400

        return redirect(url_for("submitticket", userID=userID))

    users = Users.query.order_by(Users.userEmployeeID.desc()).all()

    return render_template("createticket.html", users=users)


@main.route("/submitticket/<int:userID>", methods=["GET","POST"])
def submitticket(userID):

    user = Users.query.get_or_404(userID)

    if request.method == "POST":
        deviceID = request.form.get("DeviceID")

    userDevices = Inventory.query.filter_by(assignedUser=user.employeeID).all()

    return render_template("createticket2.html", user=user, userDevices=userDevices)

@main.route("/ticketmanagement")
def ticketmanagement():
    techs = Techs.query.order_by(Techs.techEmployeeID.desc()).all()
    users = Users.query.order_by(Users.userEmployeeID.desc()).all()
    items = Inventory.query.order_by(Inventory.itemID.desc()).all()
    tickets = Tickets.query.order_by(Tickets.ticketID.desc()).all()

    return render_template("ticketmanagement.html", techs=techs, users=users, items=items, tickets=tickets)

@main.route("/employeemanagement")
def employeemanagement():
     return render_template("employeemanagement.html")

@main.route("/employeemanagement/usermanagement")
def usermanagement():
     users = Users.query.order_by(Users.userEmployeeID.desc()).all()
     return render_template("usermanagement.html", users=users)










@main.route("/inventorymanagement")
def inventorymanagement():
    items = Inventory.query.order_by(Inventory.itemID.desc()).all()
    return render_template("inventorymanagement.html", items=items)