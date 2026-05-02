from sqlalchemy.orm import backref
from .extensions import db


class Techs(db.Model):
    techEmployeeID = db.Column(db.Integer, primary_key=True)
    techName = db.Column(db.String(32), nullable=False)

    tickets = db.relationship("Tickets", backref = "techAssigned")

    def __repr__(self):
        return f"<Tech {self.title}>"

class Users(db.Model):
    userEmployeeID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(32), nullable=False)

    assignedDevices = db.relationship("Inventory", backref = "userAssigned")
    createdTickets = db.relationship("Tickets", backref = "creatingUser")


    def __repr__(self):
        return f"<User {self.title}>"

class Inventory(db.Model):
    itemID = db.Column(db.Integer, primary_key=True)
    itemDescription = db.Column(db.String(20), nullable=False)
    assignedUser = db.Column(db.Integer, db.ForeignKey("users.userEmployeeID"), nullable=False)
    rotationDate = db.Column(db.Date)

    itemTickets = db.relationship("Tickets", backref = "ticketDevice")

    def __repr__(self):
        return f"<Inventory {self.title}>"

class Tickets(db.Model):
    ticketID = db.Column(db.Integer, primary_key=True)
    submittingUser = db.Column(db.Integer, db.ForeignKey("users.userEmployeeID"), nullable=False)
    ticketText = db.Column(db.String(100))
    ticketItem = db.Column(db.Integer, db.ForeignKey("inventory.itemID"), nullable=False)
    assignedTech = db.Column(db.Integer, db.ForeignKey("techs.techEmployeeID"), nullable=False)
    ticketDate = db.Column(db.Date, nullable=False)


    def __repr__(self):
        return f"<User {self.title}>"