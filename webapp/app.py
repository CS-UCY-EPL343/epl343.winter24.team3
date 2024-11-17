from flask import Flask, render_template, url_for, redirect, session, request, flash
# import db  # TO

app: Flask = Flask(__name__)
app.secret_key = 'team3'

# Maybe add try...except blocks for db.  # TO

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # from remember me
        if 'username' in session:
            return redirect(url_for('index'))
        
        # If not log in
        return render_template('login.html')

    elif request.method == 'POST': 
        # get data
        username: str = request.form['username']
        password: str = request.form['password']
        # If the credentials are incorrect
        if not db.validate_user(username, password): # TO
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

        # Else the credentials are correct, update the session
        remember_me: bool = bool(int(request.form['remember_me']))
        session['username'] = username
        session['UID'] = db.get_user_id(username) # TO
        # if remember me is true, set the session lifetime
        if remember_me:
            from datetime import timedelta
            app.permanent_session_lifetime = timedelta(days= 150)
            session.modified = True
            session.permanent = True
        # goto index page
        return redirect(url_for('viewInventory'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return redirect(url_for('register'))
    
    elif request.method == 'POST': 
        # get data
        username: str = request.form['username']
        password: str = request.form['password']
        password_confirmation: str = request.form['password_confirmation']

        # validate data
        if password != password_confirmation:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))
        if len(password) not in range(6, 15):
            flash('Password must be between 6 and 15 characters long.', 'error')
            return redirect(url_for('register'))

        if not db.set_user(username, password): # TO
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))

        # goto index page
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        username: str = session.pop('username', None).title()
        session.pop('UID')
        flash(f'{username} has logged out succesfully.', 'info')
    return redirect(url_for('login'))

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

@app.route('/', methods=['GET', 'POST'])
def viewInventory():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        # Have to send the data to the frond
        inventory_data: list[dict] = db.getInventoryData(session.get('UID')) # TO
        quick_switch_users: list[dict] = db.getQuickSwitchUsers(session.get('UID')) # TO
        return render_template('viewInventory.html', inventory_data= inventory_data, quick_switch_users= quick_switch_users)

    elif request.method == 'POST':
         # TO SEARCH AND FILTER


        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs: 
            return redirect(url_for('viewInventory'))
        elif cqs == 'switch':
            return redirect(url_for('viewInventory'))

        # get data
        # UID
        item_UID: str = request.form['item_uid']
        # Name
        item_name: str = request.form['item_name']
        if item_name is None or len(item_name) == 0 or len(item_name) > N:
            flash('Invalid item name.', 'error')
            return redirect(url_for('viewInventory'))
        # Size
        item_size: str = request.form['item_size']
        try:
            if int(item_size) < 0:
                flash('Invalid size value.', 'error')
                return redirect(url_for('viewInventory'))
        except ValueError:
            flash('Invalid size value.', 'error')
            return redirect(url_for('viewInventory'))
        # Category
        item_category: str = request.form['item_category']
        if item_category is None or len(item_category) == 0 or len(item_category) > N:
            flash('Invalid category value.', 'error')
            return redirect(url_for('viewInventory'))
        # Supplier
        item_supplier: str = request.form['item_supplier']
        if item_supplier is None or len(item_supplier) == 0 or len(item_supplier) > N:
            flash('Invalid supplier value.', 'error')
            return redirect(url_for('viewInventory'))
        # MinReq
        item_min_requirement: str = request.form['item_min_requirement']
        try:
            if int(item_min_requirement) < 0:
                flash('Invalid minimum requirement value.', 'error')
                return redirect(url_for('viewInventory'))
        except ValueError:
            flash('Invalid minimum requirement value.', 'error')
            return redirect(url_for('viewInventory'))
        # Photo
        item_photo: str = request.form['item_photo']
        if len(item_photo) > N:
            flash('Invalid photo value.', 'error')
            return redirect(url_for('viewInventory'))
        # Quantity
        item_quantity: str = request.form['item_quantity']
        try:
            if int(item_quantity) < 0:
                flash('Invalid quantity value.', 'error')
                return redirect(url_for('viewInventory'))
        except ValueError:
            flash('Invalid quantity value.', 'error')
            return redirect(url_for('viewInventory'))
        # Update the DB
        db.updateEntry(item_UID, item_name, item_size, item_category, item_supplier, item_min_requirement, item_photo, item_quantity)
        flash('Item updated successfully','success') # TO
        return redirect(url_for('viewInventory'))

@app.route('/report', methods=['GET', 'POST'])
def viewReport():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        quick_switch_users: list[dict] = db.getQuickSwitchUsers(session.get('UID')) # TO
        report: list[dict] = db.generateReport(session.get('UID')) # TO
        return render_template('viewReport.html', report= report, quick_switch_users= quick_switch_users)

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs: 
            return redirect(url_for('viewReport'))
        elif cqs == 'switch':
            return redirect(url_for('viewInventory'))
         # TO
        return redirect(url_for('viewReport'))

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        quick_switch_users: list[dict] = db.getQuickSwitchUsers(session.get('UID')) # TO
        pending_transactions: list[dict] = db.getPendingTransactions(session.get('UID')) # TO
        return render_template('transactions.html', pending_transactions= pending_transactions, quick_switch_users= quick_switch_users)

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs: 
            return redirect(url_for('transactions'))
        elif cqs == 'switch':
            return redirect(url_for('viewInventory'))

         # TO SEARCH AND FILTER
        
        # New transaction to be made
        if request.form['startTransaction'] is not None:
            to_user: str = request.form['to_user']
            if not (to_UID := db.user_exists(to_user)):
                flash('User does not exist.', 'error')
                return redirect(url_for('transactions'))

            item_UID: str = request.form['item_uid']
            quantity: str = request.form['quantity']
            try:
                if int(quantity) < 0:
                    flash('Invalid quantity value.', 'error')
                    return redirect(url_for('transactions'))
            except ValueError:
                flash('Invalid quantity value.', 'error')
                return redirect(url_for('transactions'))

            # Add the transaction to pending transactions
            db.addTransaction(session.get('UID'), to_UID, item_UID, quantity) # TO
            flash('Transaction made successfully.', 'info')
            return redirect(url_for('transactions'))

        # To answer to transaction
        if request.form['answerTransaction'] is not None:
            transaction_id: str = request.form['transaction_id']
            if not db.transaction_exists(transaction_id):
                flash('Transaction does not exist.', 'error')
                return redirect(url_for('transactions'))
            answer: bool = bool(int(request.form['answer']))

            # Update the transaction in pending transactions
            db.answerTransaction(transaction_id, answer) # TO
            flash('Transaction answer submitted successfully.', 'info')
            return redirect(url_for('transactions'))

        return redirect(url_for('transactions'))

@app.route('/bulkIncrease', methods=['GET', 'POST'])
def bulkIncrease():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        quick_switch_users: list[dict] = db.getQuickSwitchUsers(session.get('UID')) # TO
        #
        return render_template('bulkIncrease.html', quick_switch_users= quick_switch_users)

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs: 
            return redirect(url_for('bulkIncrease'))
        elif cqs == 'switch':
            return redirect(url_for('viewInventory'))

        # SEARCH

        # Bulk increase
        # I want the whole list

        return redirect(url_for('bulkIncrease'))
        

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