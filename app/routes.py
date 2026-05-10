import datetime
from flask import Blueprint, redirect, render_template, request, url_for

from .models import Techs
from .models import Users
from .models import Inventory
from .models import Tickets

from .extensions import db

from datetime import datetime, date


main = Blueprint("main", __name__)


@main.route("/", methods=["GET","POST"])
def createticket():
    if request.method == "POST":
        if request.form.get("startTicket") is not None:
            userID = request.form.get("userID")

            if not userID:
                return "Please select a user", 400

            return redirect(url_for("main.submitticket", userID=userID))
        elif request.form.get("submitTicket") is not None:
            createSubmittingUser = request.form.get("submitTicket")
            createTicketText = request.form.get("ticketText")
            createTicketItem = request.form.get("userDevice")
            createTicketDate = date.today()

            newTicket = Tickets(submittingUser = createSubmittingUser, ticketText=createTicketText, ticketItem = createTicketItem, assignedTech = None, ticketDate = createTicketDate)
            db.session.add(newTicket)
            db.session.commit()

    users = Users.query.order_by(Users.userEmployeeID.desc()).all()

    return render_template("createticket.html", users=users)


@main.route("/submitticket/<int:userID>", methods=["GET","POST"])
def submitticket(userID):

    user = Users.query.get_or_404(userID)

    if request.method == "POST":
        print("hi") # filler till I work on backend

    userDevices = Inventory.query.filter_by(assignedUser=user.userEmployeeID).all()

    return render_template("createticket2.html", user=user, userDevices=userDevices)

@main.route("/ticketmanagement", methods=["GET","POST"])
def ticketmanagement():
    if request.method == "POST":
        if request.form.get("viewTicket") is not None:
            
            ticketID = request.form.get("viewTicket")

            if not ticketID:
                return "Invalid Ticket", 400
            else:
                return redirect(url_for("main.ticketdetails", ticketID=ticketID))
        elif request.form.get("viewTechTicket") is not None:
            
            ticketID = request.form.get("viewTechTicket")

            if not ticketID:
                return "Invalid Ticket", 400
            else:
                return redirect(url_for("main.ticketdetails", ticketID=ticketID))
        elif request.form.get("edit") is not None:
            editTicketID = request.form.get("edit")
            editTicket = Tickets.query.get(editTicketID)
            editTicket.assignedTech = request.form.get("techAssignment")
            db.session.commit()
        elif request.form.get("delete") is not None:
            deleteTicketID = request.form.get("delete")
            deleteUser = Tickets.query.get(deleteTicketID)
            db.session.delete(deleteUser)
            db.session.commit()


        else:
            return "Invalid Ticket", 400


    techs = Techs.query.order_by(Techs.techEmployeeID.desc()).all()
    users = Users.query.order_by(Users.userEmployeeID.desc()).all()
    items = Inventory.query.order_by(Inventory.itemID.desc()).all()
    tickets = Tickets.query.order_by(Tickets.ticketID.desc()).all()

    return render_template("ticketmanagement.html", techs=techs, users=users, items=items, tickets=tickets)

@main.route("/ticketmanagement/<int:ticketID>")
def ticketdetails(ticketID):

    ticket = Tickets.query.get_or_404(ticketID)
    techs = Techs.query.order_by(Techs.techEmployeeID.desc()).all()
    return render_template("ticketdetails.html", ticket=ticket, techs=techs, ticketID = ticketID)

@main.route("/employeemanagement")
def employeemanagement():
     return render_template("employeemanagement.html")

@main.route("/employeemanagement/usermanagement", methods=["GET","POST"])
def usermanagement():
    if request.method == "POST":
        if request.form.get("delete") is not None:
            deleteUserID = request.form.get("delete")
            deleteUser = Users.query.get(deleteUserID)
            db.session.delete(deleteUser)
            db.session.commit()
        elif request.form.get("edit") is not None:
            userID = request.form.get("edit")
            return redirect(url_for("main.edituser", userID = userID))
        elif request.form.get("submitedits") is not None:
            editUserID = request.form.get("hiddenUserID")
            editUser = Users.query.get(editUserID)
            editUser.userName = request.form.get("userName")
            db.session.commit()

    users = Users.query.order_by(Users.userEmployeeID.desc()).all()
    return render_template("usermanagement.html", users=users)

@main.route("/employeemanagement/usermanagement/edit/<int:userID>", methods=["GET","POST"])
def edituser(userID):

    user = Users.query.get_or_404(userID)
    return render_template("edituser.html", user=user, userID=userID)


@main.route("/employeemanagement/techmanagement",methods=["GET","POST"])
def techmanagement():

    if request.method == "POST":
        if request.form.get("delete") is not None:
            deleteTechID = request.form.get("delete")
            deleteTech = Techs.query.get(deleteTechID)
            db.session.delete(deleteTech)
            db.session.commit()
        elif request.form.get("edit") is not None:
            techID = request.form.get("edit")
            return redirect(url_for("main.edittech", techID = techID))
        elif request.form.get("viewTechTickets") is not None:
            techID = request.form.get("viewTechTickets")
            return redirect(url_for("main.viewtickets", techID=techID))
        elif request.form.get("submitedits") is not None:
            editTechID = request.form.get("hiddenTechID")
            editTech = Techs.query.get(editTechID)
            editTech.techName = request.form.get("techName")
            db.session.commit()


    techs = Techs.query.order_by(Techs.techEmployeeID.desc()).all()
    return render_template("techmanagement.html", techs=techs)

@main.route("/employeemanagement/techmanagement/edit/<int:techID>",methods=["GET","POST"])
def edittech(techID):

    tech = Techs.query.get_or_404(techID)
    return render_template("edittech.html", tech=tech)

@main.route("/employeemanagement/techmanagement/tickets/<int:techID>")
def viewtickets(techID):
    tech = Techs.query.get_or_404(techID)

    tickets= Tickets.query.filter_by(assignedTech = tech.techEmployeeID).all()

    return render_template("techtickets.html", tickets=tickets, tech=tech)

@main.route("/employeemanagement/createemployee",methods=["GET","POST"])
def createemployee():

    if request.method == "POST":
        employeeType = request.form.get("employeeType")
        employeeName = request.form.get("employeeName")

        if employeeType == "tech":
            newTech = Techs(techName = employeeName)
            db.session.add(newTech)
            db.session.commit()

        elif employeeType == "user":
            newUser = Users(userName = employeeName)
            db.session.add(newUser)
            db.session.commit()
        else:
            return "Invalid employee type", 400



    return render_template("createemployee.html")

@main.route("/inventorymanagement",methods=["GET","POST"])
def inventorymanagement():

    if request.method == "POST":
        if request.form.get("submitedits") is not None:
            editItemID = request.form.get("submitedits")
            editItem = Inventory.query.get(editItemID)
            editItem.itemDescription = request.form.get("itemDescription")
            editItem.assignedUser = request.form.get("itemAssignment")
            editRotationDate = datetime.strptime(request.form.get("itemRotationDate"), "%Y-%m-%d").date()
            editItem.rotationDate = editRotationDate
            db.session.commit()
        elif request.form.get("submitcreation") is not None:
            newItemDescription = request.form.get("createItemDescription")
            itemAssignmentInput = request.form.get("createItemAssignment")

            if itemAssignmentInput == -1:
                newItemAssignment = None
            else:
                newItemAssignment = itemAssignmentInput
            itemRotationDateInput = request.form.get("createItemRotationDate")
            newItemRotationDate = datetime.strptime(itemRotationDateInput, "%Y-%m-%d").date()

            newItem = Inventory(itemDescription = newItemDescription, assignedUser = newItemAssignment, rotationDate = newItemRotationDate)
            db.session.add(newItem)
            db.session.commit()

        elif request.form.get("delete") is not None:
            deleteItemID = request.form.get("delete")
            deleteItem = Inventory.query.get(deleteItemID)
            db.session.delete(deleteItem)
            db.session.commit()

        elif request.form.get("edit") is not None:
            itemID = request.form.get("edit")
            return redirect(url_for("main.edititem", itemID = itemID))
        else:
            return "Invalid Submission", 400



    items = Inventory.query.order_by(Inventory.itemID.desc()).all()
    users = Users.query.order_by(Users.userEmployeeID.desc()).all()
    return render_template("inventorymanagement.html", items=items, users=users)

@main.route("/inventorymanagement/createitem")
def createitem():

    users = Users.query.order_by(Users.userEmployeeID.desc()).all()
    return render_template("createitem.html", users=users)

@main.route("/inventorymanagement/edititem/<int:itemID>")
def edititem(itemID):

    item = Inventory.query.get_or_404(itemID)
    users = Users.query.order_by(Users.userEmployeeID.desc()).all()
    return render_template("edititem.html", item=item, users=users)




