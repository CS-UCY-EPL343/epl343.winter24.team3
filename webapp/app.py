from flask import Flask, render_template, url_for, redirect, session, request, flash, jsonify
from flask_wtf.csrf import CSRFProtect, generate_csrf, CSRFError
# import db  # TO
# ADD For all inputs checks of type  # TO
# Add the N  # TO
# Maybe add try...except blocks for db.  # TO
# <input type="hidden" name="csrf_token" value="{{ csrf_token }}">  # TO

app: Flask = Flask(__name__)
app.secret_key = 'team3'
app.config['SECRET_KEY'] = 'team3_key_super_secret'
csrf = CSRFProtect(app)

@app.before_request
def before_request():
    csrf_token = generate_csrf()
    app.jinja_env.globals['csrf_token'] = csrf_token

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash('CSRF token missing or incorrect', 'error')
    return redirect(url_for('logout'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()  # Get the search query
    if not query:
        return jsonify([]), 200  # Return an empty list if the query is blank

    try:
        # Perform the search using your database
        results = db.search_inventory(query)
        return jsonify(results), 200  # Send the results back as JSON
    except Exception as e:
        return jsonify({"error": "Server error occurred"}), 500

def CheckQuickSwitch() -> bool|str:
    # Check if quick switch is called
    if request.form.get('quickSwitch') is not None:
        new_username: str = request.form.get('quickSwitchUser')
        # if the user does not have the account in their quick switch list
        if new_username not in db.getQuickSwitchUsers(session.get('UID')): # TO
            flash('You have no access in this account.', 'error')
            return True

        # else change the session details
        session['username'] = new_username
        session['UID'] = db.get_user_id(new_username) # TO
        flash('Quick switch successful.', 'info')
        # Back to the main page
        return 'switch'

    # Check if a new quick switch is added
    if request.form.get('addQuickSwitch') is not None:
        new_username: str = request.form.get('addQuickSwitchUser_Username')
        password: str = request.form.get('addQuickSwitchUser_Password')

        # Validate details
        if not db.validate_user(new_username, password): # TO
            flash('Invalid username or password.', 'error')
            return True

        # Check if the user already exists in quick switch list
        if new_username in db.getQuickSwitchUsers(session.get('UID')): # TO
            flash('User already exists in quick switch.', 'error')
        # else add the user to quick switch list
        else:
            db.addQuickSwitchUser(session.get('UID'), new_username) # TO
            flash('Quick switch user added successfully.', 'info')
        # Back to the main page
        return True
    # If nothing happened
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # from remember me
        if 'username' in session:
            return redirect(url_for('viewInventory'))
        
        # If not log in
        return render_template('login.html'), 200

    elif request.method == 'POST': 
        # get data
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        # If the credentials are incorrect
        if not db.validate_user(username, password): # TO
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'), 401)

        # Else the credentials are correct, update the session
        remember_me: bool = bool(int(request.form.get('remember_me')))
        session['username'] = username
        session['UID'] = db.get_user_id(username) # TO
        # if remember me is true, set the session lifetime
        if remember_me:
            from datetime import timedelta
            app.permanent_session_lifetime = timedelta(days= 150)
            session.modified = True
            session.permanent = True
        # goto index page
        return redirect(url_for('viewInventory'), 200)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return redirect(url_for('register'), 200)
    
    elif request.method == 'POST': 
        # get data
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        password_confirmation: str = request.form.get('password_confirmation')

        # validate data
        if  username is None or password is None or password_confirmation is None:
            flash('All fields are required.', 'error')
            return redirect(url_for('register'), 400)
        # if username is taken.
        if db.isUsernameTaken(username): # TO
            flash('Username already exists.', 'error')
            return redirect(url_for('register'), 409)
        # if passwords do not match.
        if password != password_confirmation:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'), 400)
        # if password is not between 6 and 15 characters.
        if len(password) not in range(6, 15):
            flash('Password must be between 6 and 15 characters long.', 'error')
            return redirect(url_for('register'), 400)
        # Setting the user
        if not db.set_user(username, password): # TO
            flash('An error has occurred.')
            return redirect(url_for('register'), 400)

        # goto index page
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        username: str = session.pop('username', None).title()
        session.pop('UID')
        flash(f'{username} has logged out succesfully.', 'info')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def viewInventory():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        # Have to send the data to the frond
        inventory_data: list[dict] = db.getInventoryData(session.get('UID')) # TO
        quick_switch_users: list[dict] = db.getQuickSwitchUsers(session.get('UID')) # TO
        category_options = db.getCategoryOptions(session.get('UID')) # TO
        supplier_options = db.getSupplierOptions(session.get('UID')) # TO
        return render_template('viewInventory.html', inventory_data= inventory_data, quick_switch_users= quick_switch_users,
                                category_options= category_options, supplier_options= supplier_options), 200

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs: 
            return redirect(url_for('viewInventory'))
        elif cqs == 'switch':
            return redirect(url_for('viewInventory'), 200)

        # get data
        if request.form.get('updateEntry') or request.form.get('createEntry'):
            # UID
            item_UID: str = request.form.get('item_uid', None)
            # Name
            item_name: str = request.form.get('item_name')
            if item_name is None or len(item_name) == 0 or len(item_name) > N:
                flash('Invalid item name.', 'error')
                return redirect(url_for('viewInventory'), 400)
            # Size
            item_size: str = request.form.get('item_size')
            try:
                if int(item_size) < 0:
                    flash('Invalid size value.', 'error')
                    return redirect(url_for('viewInventory'), 400)
            except ValueError:
                flash('Invalid size value.', 'error')
                return redirect(url_for('viewInventory'), 200)
            # Category
            item_category: str = request.form.get('item_category')
            if item_category is None or len(item_category) == 0 or len(item_category) > N:
                flash('Invalid category value.', 'error')
                return redirect(url_for('viewInventory'), 400)
            # Supplier
            item_supplier: str = request.form.get('item_supplier')
            if item_supplier is None or len(item_supplier) == 0 or len(item_supplier) > N:
                flash('Invalid supplier value.', 'error')
                return redirect(url_for('viewInventory'), 400)
            # MinReq
            item_min_requirement: str = request.form.get('item_min_requirement')
            try:
                if int(item_min_requirement) < 0:
                    flash('Invalid minimum requirement value.', 'error')
                    return redirect(url_for('viewInventory'), 400)
            except ValueError:
                flash('Invalid minimum requirement value.', 'error')
                return redirect(url_for('viewInventory'), 400)
            # Photo
            item_photo: str = request.form.get('item_photo')
            if len(item_photo) > N:
                flash('Invalid photo value.', 'error')
                return redirect(url_for('viewInventory'), 400)
            # Quantity
            item_quantity: str = request.form.get('item_quantity')
            try:
                if int(item_quantity) < 0:
                    flash('Invalid quantity value.', 'error')
                    return redirect(url_for('viewInventory'), 400)
            except ValueError:
                flash('Invalid quantity value.', 'error')
                return redirect(url_for('viewInventory'), 400)
            
            # Update the DB # TO
            db.updateEntry(item_UID, item_name, item_size, item_category, item_supplier, item_min_requirement, item_photo, item_quantity)
            db.createEntry(item_name, item_size, item_category, item_supplier, item_min_requirement, item_photo, item_quantity)
            
            flash('Item updated successfully','success') # TO

        # Get the filter values
        category: str = request.form.get('filterCategory', '')
        supplier: str = request.form.get('filterSupplier', '')
        quantity_filter: str = request.form.get('filterQuantity', '')
        if category + supplier + quantity_filter != '':
            # Fetch the filtered inventory from the DB
            filtered_data = db.getFilteredInventory(session.get('UID'), category, supplier, quantity_filter) # TO

            # Fetch category and supplier options from the DB
            category_options = db.getCategoryOptions(session.get('UID')) # TO
            supplier_options = db.getSupplierOptions(session.get('UID')) # TO

            # Pass the data to the template
            return render_template('viewInventory.html', inventory_data=filtered_data,
                category_options=category_options, supplier_options=supplier_options), 200

        return redirect(url_for('viewInventory'), 200)

@app.route('/report', methods=['GET', 'POST'])
def viewReport():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        quick_switch_users: list[dict] = db.getQuickSwitchUsers(session.get('UID')) # TO
        report: list[dict] = db.generateReport(session.get('UID')) # TO
        return render_template('viewReport.html', report= report, quick_switch_users= quick_switch_users), 200

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs: 
            return redirect(url_for('viewReport'), 200)
        elif cqs == 'switch':
            return redirect(url_for('viewInventory'))
        
         # TO If the user can do anything here

        return redirect(url_for('viewReport'))

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        quick_switch_users: list[dict] = db.getQuickSwitchUsers(session.get('UID')) # TO
        pending_transactions: list[dict] = db.getPendingTransactions(session.get('UID')) # TO
        return render_template('transactions.html', pending_transactions= pending_transactions,
                        quick_switch_users= quick_switch_users), 200

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs: 
            return redirect(url_for('transactions'), 200)
        elif cqs == 'switch':
            return redirect(url_for('viewInventory'))

         # TO SEARCH AND FILTER
        
        # New transaction to be made
        if request.form.get('startTransaction') is not None:
            to_user: str = request.form.get('to_user')
            if not (to_UID := db.user_exists(to_user)):
                flash('User does not exist.', 'error')
                return redirect(url_for('transactions'), 400)

            item_UID: str = request.form.get('item_uid')
            quantity: str = request.form.get('quantity')
            try:
                if int(quantity) < 0:
                    flash('Invalid quantity value.', 'error')
                    return redirect(url_for('transactions'), 400)
            except ValueError:
                flash('Invalid quantity value.', 'error')
                return redirect(url_for('transactions'), 400)

            # Add the transaction to pending transactions
            db.addTransaction(session.get('UID'), to_UID, item_UID, quantity) # TO
            flash('Transaction made successfully.', 'info')
            return redirect(url_for('transactions'), 400)

        # To answer to transaction
        if request.form.get('answerTransaction') is not None:
            transaction_id: str = request.form.get('transaction_id')
            if not db.transaction_exists(transaction_id):
                flash('Transaction does not exist.', 'error')
                return redirect(url_for('transactions'), 400)
            answer: bool = bool(int(request.form.get('answer')))

            # Update the transaction in pending transactions
            db.answerTransaction(transaction_id, answer) # TO
            flash('Transaction answer submitted successfully.', 'info')
            return redirect(url_for('transactions'), 200)

        return redirect(url_for('transactions'), 200)

@app.route('/bulkIncrease', methods=['GET', 'POST'])
def bulkIncrease():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        quick_switch_users: list[dict] = db.getQuickSwitchUsers(session.get('UID')) # TO
        # TO
        return render_template('bulkIncrease.html', quick_switch_users= quick_switch_users)

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs: 
            return redirect(url_for('bulkIncrease'), 200)
        elif cqs == 'switch':
            return redirect(url_for('viewInventory'))

        # Bulk increase
        # Check if the submit button was pressed
        if 'submitBulkIncrease' in request.form:
            # Retrieve the submitted products and quantities
            product_uids = request.form.getlist('productUID')  # A list of product IDs
            product_quantities = request.form.getlist('productQuantity')  # A list of quantities

            # Process each product with its quantity
            for product_uid, quantity in zip(product_uids, product_quantities):
                if quantity and int(quantity) > 0:
                    # Update the database or perform the bulk increase operation here
                    try:
                        db.IncreaseQuantity(product_uid, int(quantity))
                    except Exception as e:
                        print(e)
                        flash('Error increasing quantity for product: {product_uid}', 'error')

            flash('Bulk increase successful!', 'success')
            return redirect(url_for('viewInventory'))

        return redirect(url_for('bulkIncrease'), 200) 

@app.route('/bulkDecrease', methods=['GET', 'POST'])
def bulkDecrease():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        quick_switch_users: list[dict] = db.getQuickSwitchUsers(session.get('UID')) # TO
        # TO
        return render_template('bulkDecrease.html', quick_switch_users= quick_switch_users)

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs: 
            return redirect(url_for('bulkDecrease'), 200)
        elif cqs == 'switch':
            return redirect(url_for('viewInventory'))

        # Bulk decrease
        # Check if the submit button was pressed
        if 'submitBulkDecrease' in request.form:
            # Retrieve the submitted products and quantities
            product_uids = request.form.getlist('productUID')  # A list of product IDs
            product_quantities = request.form.getlist('productQuantity')  # A list of quantities

            # Process each product with its quantity
            for product_uid, quantity in zip(product_uids, product_quantities):
                if quantity and int(quantity) > 0:
                    # Update the database or perform the bulk decrease operation here
                    try:
                        # Check if the quantity is greater than the decrease quantity.
                        qnt = db.getQuantity(product_uid)
                        if qnt < int(quantity):
                            flash('Not enough stock for product: {product_uid}', 'error')
                            continue
                        db.DecreaseQuantity(product_uid, int(quantity))
                    except Exception as e:
                        print(e)
                        flash('Error decreasing quantity for product: {product_uid}', 'error')

            flash('Bulk decrease successful!', 'success')
            return redirect(url_for('viewInventory'))

        return redirect(url_for('bulkDecrease'), 200) 


@app.route('/_', methods=['GET', 'POST'])
def _():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        quick_switch_users: list[dict] = db.getQuickSwitchUsers(session.get('UID')) # TO
        #
        return render_template('_.html', quick_switch_users= quick_switch_users)

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs: 
            return redirect(url_for('_'))
        elif cqs == 'switch':
            return redirect(url_for('viewInventory'))
        #
        return redirect(url_for('_'))


if __name__ == '__main__':
    app.run(debug=True)