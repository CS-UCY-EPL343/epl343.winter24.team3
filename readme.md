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
- Lastly, the inventory color codes each entry based on the remaining quantity and the minimum requirement given by the user.

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

## Flask Application API Endpoints

### General Endpoints

- **GET `/favicon.ico`**
  - **Description:** Serves the `favicon.ico` from the static directory.

- **GET `/`**
  - **Description:** Index page, Redirects to the login page.

### Authentication

- **GET, POST `/login`**
  - **Description:** Handles user login. Displays the login form on GET and processes login on POST.

- **GET, POST `/register`**
  - **Description:** Handles new user registration. Displays the registration form on GET and processes registration on POST.

- **GET `/logout`**
  - **Description:** Logs out the user and redirects to the login page.

### Inventory Management

- **GET, POST `/inventory`**
  - **Description:** Main inventory page. Displays all inventory items on GET. Handles item creation and filtering on POST.

- **GET `/selectedItem`**
  - **Description:** Fetches and displays detailed data for a selected inventory item.

- **POST `/updateQuantity`**
  - **Description:** Updates the quantity of an inventory item.

- **POST `/updateEntry`**
  - **Description:** Updates detailed information of an inventory item.

### Bulk Operations

- **GET, POST `/bulkIncrease`**
  - **Description:** Manages bulk increases in inventory quantities. Displays current bulk list on GET and processes additions or the final bulk increase on POST.

- **GET, POST `/bulkDecrease`**
  - **Description:** Manages bulk decreases in inventory quantities. Displays current bulk list on GET and processes removals or the final bulk decrease on POST.

- **POST `/removeDecrease`**
  - **Description:** Removes an item from the bulk decrease list.

- **POST `/removeIncrease`**
  - **Description:** Removes an item from the bulk increase list.

### Transaction Handling

- **GET, POST `/transactions`**
  - **Description:** Handles transactions between users. Displays pending transactions on GET and processes transaction responses on POST.

### Reporting

- **GET, POST `/report`**
  - **Description:** Displays generated reports and manages user switching through quick switch functionality.

### Search and Filter

- **GET `/search`**
  - **Description:** Returns search results as JSON based on the user's query.

Each endpoint is designed to support specific functionalities within the inventory management system, facilitating efficient and user-friendly interactions.

