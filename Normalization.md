Functional Dependencies:
	Techs:
		EmployeeID -> Employee Name
	Users:
		EmployeeID -> Employee Name
	Inventory:
		ItemID -> ItemDescription
		ItemID -> AssignedUser
		ItemID -> RotationDate
	Tickets:
		TicketID -> SubmittingUser
		TicketID -> TicketText
		TicketID -> TicketItem
		TicketID -> AssignedTech
		TicketID -> TicketDate
Potential Anomalies:
	Since each table functions on dedicated IDs for each row in the table there should not be any update, Deletion, or Insertion Anomalies
Decomposition:
	The tables do not violate the 3rd normal form. It meets the first normal form as no table has a composite key. It meets the second normal form as each column depends only on the primary key. Finally the third normal form is satisfied as ther are no transitive dependencies in any table.
Updated Schema:
	The schema remains the same, it is already in 3nf