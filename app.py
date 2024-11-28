from flask import Flask, render_template, url_for, redirect, session, request, flash, jsonify
from db import db

app: Flask = Flask(__name__)
app.secret_key = 'team3'
app.config['SECRET_KEY'] = 'team3_key_super_secret'

@app.route('/search', methods=['GET'])
def search():
    query: str = request.args.get('query', '').strip()  # Get the search query
    if not query:
        return jsonify([])  # Return an empty list if the query is blank

    try:
        # Perform the search using your database
        results = db.search_inventory(session.get('UID'), query)
        return jsonify(results)  # Send the results back as JSON
    except Exception as e:
        print(e)
        return jsonify({"error": "Server error occurred"})
    
@app.route('/selectedItem', methods=['GET'])
def selectedItem():
    entryID = request.args.get('EntryID', '').strip()
    if not entryID:
        return jsonify({'error': 'EntryID not provided'}), 400

    try:
        # Fetch updated data
        entry_data = db.get_entry(session.get('UID'), entryID)
        quick_switch_users = db.get_quick_switch_users(session.get('UID'))
        category_options = db.get_category_options(session.get('UID'))
        supplier_options = db.get_supplier_options(session.get('UID'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Render the full inventory.html template
    rendered_template = render_template(
        'inventory.html',
        inventory_data=entry_data,
        quick_switch_users=quick_switch_users,
        category_options=category_options,
        supplier_options=supplier_options
    )
    return jsonify({'html': rendered_template})

@app.route('/updateQuantity', methods=['POST'])
def update_quantity():
    data = request.get_json()
    entry_id = data.get('entryID')
    quantity = data.get('quantity')

    if not entry_id or quantity is None:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        # Update the quantity in the database
        db.update_quantity(entry_id, quantity)
        return jsonify({'success': True, 'entryID': entry_id, 'quantity': quantity})
    except Exception as e:
        print(f"Error updating quantity: {e}")
        return jsonify({'error': 'Failed to update quantity'}), 500

@app.route('/updateEntry', methods=['POST'])
def update_entry():
    try:
        data = request.get_json()  # Parse JSON from request
        
        # Extract fields
        item_uid = data.get('u_item_uid')
        item_photo = data.get('u_item_photo')
        item_name = data.get('u_item_name')
        item_size = data.get('u_item_size')
        item_category = data.get('u_item_category')
        item_supplier = data.get('u_item_supplier')
        item_min_requirement = data.get('u_item_min_requirement')

        # Validation
        if not all([item_uid, item_name, item_size, item_supplier, item_min_requirement]):
            return jsonify({'error': 'All fields are required'}), 400

        db.update_entry(entry_id=item_uid, name=item_name, size=item_size, category=item_category, supplier=item_supplier, minreq=item_min_requirement, photo=item_photo)

        return jsonify({'message': 'Item updated successfully'}), 200

    except Exception as e:
        print(f"Error updating item: {e}")
        return jsonify({'error': 'An error occurred while updating the item.'}), 500


def CheckQuickSwitch() -> bool|str:
    # Check if quick switch is called
    quick_switch_users: list[str] = db.get_quick_switch_users(session.get('UID')) # TO
    for user in quick_switch_users:
        if request.form.get(user) == user:
            print('Switching user.')
            new_username: str = request.form.get(user)
            try:
                # if the user does not have the account in their quick switch list
                if new_username not in quick_switch_users:
                    flash('You have no access in this account.')
                    print('You have no access in this account.')
                    return True
            except Exception as e:
                print(e)
                flash('Error occurred while checking quick switch.')
                print('Error occurred while checking quick switch.')
                return True

            # else change the session details
            session['username'] = new_username
            try:
                session['UID'] = db.get_user_uid(new_username) # TO
            except Exception as e:
                print(e)
                flash('Error occurred while changing session details.')
                print('Error occured while changing session details.')
                return True
            
            session.modified = True
            print('Quick switch successful.')
            # Back to the main page
            return 'switch'

    # Check if a new quick switch is added
    if request.form.get('addQuickSwitchUser') == 'addQuickSwitchUser':
        new_username: str = request.form.get('addQuickSwitchUser_Username')
        password: str = request.form.get('addQuickSwitchUser_Password')

        # Validate details
        try:
            if not db.validate_user(new_username, password): # TO
                flash('Invalid username or password.')
                print('Invalid username or password.')
                return True
        except Exception as e:
            print(e)
            flash('Error occurred while validating user details.')
            print('Error occurred while validating user details.')
            return True

        try:
            # Check if the user already exists in quick switch list
            if new_username in db.get_quick_switch_users(session.get('UID')): # TO
                flash('User already exists in quick switch.')
                print('User already exists in quick switch.')
            # else add the user to quick switch list
            else:
                db.add_quick_switch_user(session.get('UID'), new_username) # TO
                print('Quick switch user added successfully.')
        except Exception as e:
            print(e)
            flash('Error occurred while adding quick switch user.')
            print('Error occurred while adding quick switch user.')
            return True
        # Back to the main page
        return True
    # If nothing happened
    return False

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # from remember me
        if 'username' in session:
            return redirect(url_for('inventory'))
        
        # If not log in
        return render_template('login.html')

    elif request.method == 'POST': 
        # get data
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        
        # If the credentials are incorrect
        try:
            if not db.validate_user(username, password): # TO
                flash('Invalid username or password.')
                print('Invalid username or password.')
                return redirect(url_for('login'))
        except Exception as e:
            print(e)
            flash('Error occurred while validating user details.')
            return redirect(url_for('login'))

        # Else the credentials are correct, update the session
        remember_me: bool = request.form.get('remember_me') or False

        session['username'] = username
        try:
            session['UID'] = db.get_user_uid(username)
        except Exception as e:
            print(e)
            flash('Error occurred while changing session details.')
            return redirect(url_for('login'))
        
        # # if remember me is true, set the session lifetime
        # if remember_me:
        #     from datetime import timedelta
        #     app.permanent_session_lifetime = timedelta(days= 150)
        #     session.modified = True
        #     session.permanent = True

        # goto main page
        print('login successful')
        return redirect(url_for('inventory'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST': 
        # get data
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        password_confirmation: str = request.form.get('password_confirmation')

        # validate data
        if  username is None or password is None or password_confirmation is None:
            flash('All fields are required.')
            print('All fields are required.')
            return redirect(url_for('register'))
        
        # if username is taken.
        try:
            if db.user_exists(username): # TO
                flash('Username already exists.')
                print('Username already exists.')
                return redirect(url_for('register'))
        except Exception as e:
            print(e)
            flash('Error occurred while checking username availability.')
            print('Error occurred while checking username availability.')
            return redirect(url_for('register'))
        
        # if passwords do not match.
        if password != password_confirmation:
            flash('Passwords do not match.')
            print('Passwords do not match.')
            return redirect(url_for('register'))
        
        # if password is not between 6 and 15 characters.
        if len(password) not in range(6, 15):
            flash('Password must be between 6 and 15 characters long.')
            print('Password must be between 6 and 15 characters long.')
            return redirect(url_for('register'))
        
        # Setting the user
        try:
            if not db.set_user(username, password): # TO
                flash('An error has occurred.')
                print('An error has occurred.')
                return redirect(url_for('register'))
        except Exception as e:
            print(e)
            flash('Error occurred while setting user details.')
            print('Error occurred while setting user details.')
            return redirect(url_for('register'))

        # goto index page
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        username: str = session.pop('username', None).title()
        session.pop('UID')
        flash(f'{username} has logged out succesfully.')
        print(f'{username} has logged out succesfully.')
        session.modified = True 
    return redirect(url_for('login'))

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        # Have to send the data to the frond
        try:
            inventory_data: list[dict] = db.get_inventory_data(session.get('UID')) # TO
            quick_switch_users: list[str] = db.get_quick_switch_users(session.get('UID')) # TO
            category_options: list[str] = db.get_category_options(session.get('UID')) # TO
            supplier_options: list[str] = db.get_supplier_options(session.get('UID')) # TO
        except:
            flash('An error occurred while retrieving data.')
            print('An error occurred while retrieving data.')
            return redirect(url_for('inventory'))
        
        return render_template('inventory.html', inventory_data= inventory_data, quick_switch_users= quick_switch_users,
                                category_options= category_options, supplier_options= supplier_options)

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs == True: 
            return redirect(url_for('inventory'))
        elif cqs == 'switch':
            return redirect(url_for('inventory'))

        # get data
        if request.form.get('createEntry'):
            # Name
            item_name: str = request.form.get('item_name')
            if item_name is None or len(item_name) == 0 or len(item_name) > 30:
                flash('Invalid item name.')
                print('Invalid item name.')
                return redirect(url_for('inventory'))
            
            # Size
            item_size: str = request.form.get('item_size')
            try:
                if int(item_size) < 0:
                    flash('Invalid size value.')
                    print('Invalid size value.')
                    return redirect(url_for('inventory'))
            except ValueError:
                flash('Invalid size value.')
                print('Invalid size value.')
                return redirect(url_for('inventory'))
            
            # Category
            item_category: str = request.form.get('item_category')
            if item_category is None or len(item_category) == 0 or len(item_category) > 20:
                flash('Invalid category value.')
                print('Invalid category value.')
                return redirect(url_for('inventory'))
            
            # Supplier
            item_supplier: str = request.form.get('item_supplier')
            if item_supplier is None or len(item_supplier) == 0 or len(item_supplier) > 30:
                flash('Invalid supplier value.')
                print('Invalid supplier value.')
                return redirect(url_for('inventory'))
            
            # MinReq
            item_min_requirement: str = request.form.get('item_min_requirement')
            try:
                if int(item_min_requirement) < 0:
                    flash('Invalid minimum requirement value.')
                    print('Invalid minimum requirement value.')
                    return redirect(url_for('inventory'))
            except ValueError:
                flash('Invalid minimum requirement value.')
                print('Invalid minimum requirement value.')
                return redirect(url_for('inventory'))
            
            # Photo
            item_photo: str = request.form.get('item_photo')
            if len(item_photo) > 260:
                flash('Invalid photo value.')
                print('Invalid photo value.')
                return redirect(url_for('inventory'))
            
            # Quantity
            item_quantity: str = request.form.get('item_quantity')
            try:
                if int(item_quantity) < 0:
                    flash('Invalid quantity value.')
                    print('Invalid quantity value.')
                    return redirect(url_for('inventory'))
            except ValueError:
                flash('Invalid quantity value.')
                print('Invalid quantity value.')
                return redirect(url_for('inventory'))
            
            # Update the DB # TO
            try:
                db.create_entry(session['UID'], item_name, item_size, item_category, item_supplier, item_min_requirement, item_photo, item_quantity)
                print('Item created successfully.')
            except Exception as e:
                print(e)
                flash('Error occurred while updating entry data.')
                print('Error occurred while updating entry data.')
                return redirect(url_for('inventory'))

        # Get the filter values
        category: str = request.form.get('filterCategory', '')
        supplier: str = request.form.get('filterSupplier', '')
        quantity_filter: str = request.form.get('filterQuantity', '')
        if category + supplier + quantity_filter != '':
            try:
                # Fetch the filtered inventory from the DB
                filtered_data = db.get_filtered_inventory(session.get('UID'), category, supplier, quantity_filter) # TO # TO # TO # TO
                # Fetch options from the DB
                category_options = db.get_category_options(session.get('UID')) # TO
                supplier_options: list[str] = db.get_supplier_options(session.get('UID')) # TO
                quick_switch_users: list[str] = db.get_quick_switch_users(session.get('UID')) # TO   
            except Exception as e:
                print(e)
                flash('An error occurred while retrieving data.')
                print('An error occurred while retrieving data.')
                return redirect(url_for('inventory'))
                 
            # Pass the data to the template
            return render_template('inventory.html', inventory_data=filtered_data, quick_switch_users=quick_switch_users,
                    category_options=category_options, supplier_options=supplier_options)

        return redirect(url_for('inventory'))

@app.route('/report', methods=['GET', 'POST'])
def report():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        try:
            quick_switch_users: list[str] = db.get_quick_switch_users(session.get('UID')) # TO
            report: list[dict] = db.generate_report(session.get('UID')) # TO
        except Exception as e:
            print(e)
            flash('Error occurred while retrieving report data.')
            print('Error occurred while retrieving report data.')
            return redirect(url_for('report'))
        
        return render_template('report.html', report= report, quick_switch_users= quick_switch_users)

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs == True: 
            return redirect(url_for('report'))
        elif cqs == 'switch':
            return redirect(url_for('inventory'))
        
         # TO If the user can do anything here

        return redirect(url_for('report'))

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        try:
            quick_switch_users: list[str] = db.get_quick_switch_users(session.get('UID')) # TO
            pending_transactions: list[dict] = db.get_pending_transactions(session.get('UID')) # TO
        except Exception as e:
            print(e)
            flash('Error occurred while retrieving transaction data.')
            print('Error occurred while retrieving transaction data.')
            return redirect(url_for('transactions'))
        
        return render_template('transactions.html', pending_transactions= pending_transactions,
                        quick_switch_users= quick_switch_users)

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs == True: 
            return redirect(url_for('transactions'))
        elif cqs == 'switch':
            return redirect(url_for('inventory'))
        
        # New transaction to be made
        if request.form.get('startTransaction') is not None:
            to_user: str = request.form.get('to_user')
            # Receiving user does not exist.
            try:
                if not (to_UID := db.user_exists(to_user)):
                    flash('User does not exist.')
                    return redirect(url_for('transactions'))
            except Exception as e:
                print(e)
                flash('Error occurred while checking user existence.')
                print('Error occurred while checking user existence.')
                return redirect(url_for('transactions'))

            item_UID: str = request.form.get('item_uid')
            quantity: str = request.form.get('quantity')
            try:
                if int(quantity) < 0:
                    flash('Invalid quantity value.')
                    print('Invalid quantity value.')
                    return redirect(url_for('transactions'))
            except ValueError:
                flash('Invalid quantity value.')
                print('Invalid quantity value.')
                return redirect(url_for('transactions'))

            # Add the transaction to pending transactions
            try:
                db.addTransaction(session.get('UID'), to_UID, item_UID, quantity) # TO
            except Exception as e:
                print(e)
                flash('Error occurred while adding transaction.')
                print('Error occurred while adding transaction.')
                return redirect(url_for('transactions'))
            
            print('Transaction made successfully.')
            return redirect(url_for('transactions'))

        # To answer to transaction
        if request.form.get('answerTransaction') is not None:
            transaction_id: str = request.form.get('transaction_id')
            try:
                if not db.transaction_exists(transaction_id):
                    flash('Transaction does not exist.')
                    print('Transaction does not exist')
                    return redirect(url_for('transactions'))
            except Exception as e:
                print(e)
                flash('Error occurred while checking transaction existence.')
                print('Error occurred while checking transaction existence.')
                return redirect(url_for('transactions'))
            
            try:
                answer: bool = bool(int(request.form.get('answer')))
            except ValueError:
                flash('Invalid answer value.')
                print('Invalid answer value.')
                return redirect(url_for('transactions'))
            
            # Update the transaction in pending transactions
            try:
                db.answer_transaction(transaction_id, answer) # TO
            except Exception as e:
                print(e)
                flash('Error occurred while updating the transaction.')
                print('Error occurred while updating the transaction.')
                return redirect(url_for('transactions'))
            
            flash('Transaction answer submitted successfully.')
            print('Transaction answer submitted successfully.')
            return redirect(url_for('transactions'))

        return redirect(url_for('transactions'))

@app.route('/bulkIncrease', methods=['GET', 'POST'])
def bulkIncrease():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        try:
            quick_switch_users: list[str] = db.get_quick_switch_users(session.get('UID')) # TO
        except Exception as e:
            print(e)
            flash('An error occurred while retrieving data.')
            print('An error occurred while retrieving data.')
            return redirect(url_for('bulkIncrease'))
        # TO
        return render_template('bulkIncrease.html', quick_switch_users= quick_switch_users)

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs == True: 
            return redirect(url_for('bulkIncrease'))
        elif cqs == 'switch':
            return redirect(url_for('inventory'))

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
                        db.increase_quantity(product_uid, int(quantity))
                    except Exception as e:
                        print(e)
                        flash('Error increasing quantity for product: {product_uid}')
                        print('Error increasing quantity for product: {product_uid}')

            flash('Bulk increase successful!', 'success')
            print('Bulk increase successful!')
            return redirect(url_for('inventory'))

        return redirect(url_for('bulkIncrease')) 

@app.route('/bulkDecrease', methods=['GET', 'POST'])
def bulkDecrease():
    # If not logged in
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'GET':
        try:
            quick_switch_users: list[str] = db.get_quick_switch_users(session.get('UID')) # TO
        except Exception as e:
            print(e)
            flash('An error occurred while retrieving data.')
            print('An error occurred while retrieving data.')
            return redirect(url_for('bulkDecrease'))
        # TO
        return render_template('bulkDecrease.html', quick_switch_users= quick_switch_users, to_be_removed_items= [])

    elif request.method == 'POST':
        # Check quick switch or add new quick switch user
        cqs = CheckQuickSwitch()
        if cqs == True: 
            return redirect(url_for('bulkDecrease'))
        elif cqs == 'switch':
            return redirect(url_for('inventory'))

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
                        qnt = db.get_quantity(product_uid)
                        if qnt < int(quantity):
                            flash('Not enough stock for product: {product_uid}')
                            continue
                        db.decrease_quantity(product_uid, int(quantity))
                    except Exception as e:
                        print(e)
                        flash('Error decreasing quantity for product: {product_uid}')
                        print('Error decreasing quantity for product: {product_uid}')

            print('Bulk decrease successful!')
            return redirect(url_for('inventory'))

        return redirect(url_for('bulkDecrease')) 

if __name__ == '__main__':
    app.run(debug=True)