# Stock Tracking web application

We are team 3 and decided to implement the stock tracking web application idea.

# Functionalities

## Functional
- UI has a sliding navigation bar to the left.
- There is an informative bar to the top of the screen, where the user can log out and switch user.

## Authentication
- The system handles authentication for the user's login and register.
- Moreover, the system also handles the quick switch between users.

## Tracking
- The trackventory application keeps track of the stock of each user.
- Each item in the inventory is grouped by its category.
- It enables the users to view all of their entries, edit them, and even change their quantity settings.
- Furthermore, the user can add new entries to their inventory.
- Also, the user can search for a specific product, or even filter their inventory to their needs.

## Product Exchange
- The users can request or even send products to other users.
- The other user, can accept or reject the request.

## Bulk Operations
### Bulk Increase
- The bulk increase operation lets users select multiple products and quantities, before submitting and increasing all of them.
### Bulk Decrease
- The bulk decrease operation lets users select multiple products and quantities, before submitting and decreasing all of them.

## Reports
- The report functionality, shows to the user, all of this week's oscillations in quantitites.

# Implementation
## Sections
We have splitted up the project into sections.
- DataBase
- Back End
- Front End

### Database
The database we chose is SQLite3 from the built-in module of python. SQLite was efficient for our project because there will be one user.

### Back End
The back end is programmed with the Flask framework. Some javascript-ajax functions were required as well.

### Front End
The front end used html, css, and little javascript to visualize the idea. Also the jinja2 engine was used to send data from the db to the front end, through the Flask implementation.

### Docker
The project is dockerized in order to be portable. The functionality does not change, rather it gets better and more stable.

#### TODOs
Implement colour codes.