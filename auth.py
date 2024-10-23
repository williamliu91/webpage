import streamlit as st
import hashlib
import sqlite3
import pandas as pd
import base64


# Function to load the image and convert it to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to the locally stored QR code image
qr_code_path = "qrcode.png"  # Ensure the image is in your app directory

# Convert image to base64
qr_code_base64 = get_base64_of_bin_file(qr_code_path)

# Custom CSS to position the QR code close to the top-right corner under the "Deploy" area
st.markdown(
    f"""
    <style>
    .qr-code {{
        position: fixed;  /* Keeps the QR code fixed in the viewport */
        top: 10px;       /* Sets the distance from the top of the viewport */
        right: 10px;     /* Sets the distance from the right of the viewport */
        width: 200px;    /* Adjusts the width of the QR code */
        z-index: 100;    /* Ensures the QR code stays above other elements */
    }}
    </style>
    <img src="data:image/png;base64,{qr_code_base64}" class="qr-code">
    """,
    unsafe_allow_html=True
)


# Function to check if a column exists in a table
def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    return any(column[1] == column_name for column in columns)

# Database initialization with schema update handling
def init_db():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Check if the users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            # Create new table with all columns
            cursor.execute('''CREATE TABLE users (
                            username TEXT PRIMARY KEY,
                            password TEXT NOT NULL,
                            role TEXT DEFAULT 'user')''')
        else:
            # Check if role column exists
            if not column_exists(cursor, 'users', 'role'):
                # Add role column to existing table
                cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
                conn.commit()
        
        # Check if admin account exists
        cursor.execute("SELECT username FROM users WHERE username = ?", ("admin",))
        admin_exists = cursor.fetchone()
        
        # Create admin account if it doesn't exist
        if not admin_exists:
            admin_username = "admin"
            admin_password = hash_password("admin123")
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                         (admin_username, admin_password, "admin"))
        else:
            # Update existing admin account to ensure it has admin role
            cursor.execute("UPDATE users SET role = ? WHERE username = ?", ("admin", "admin"))
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user_to_db(username, password, role='user'):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                      (username, password, role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        st.error("Username already exists.")
        return False
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return False

def check_user_in_db(username):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return False

def verify_user(username, password):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            stored_hashed_password, role = result
            if stored_hashed_password == hash_password(password):
                return True, role
        return False, None
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return False, None

def fetch_all_users_with_passwords():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []

def signup():
    st.title("Member Sign-Up")
    
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Sign Up", key="sign_up"):
        if not new_username or not new_password:
            st.error("Username and password are required.")
        elif check_user_in_db(new_username):
            st.error("Username already exists. Please choose another one.")
        elif new_password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters long.")
        else:
            hashed_password = hash_password(new_password)
            if add_user_to_db(new_username, hashed_password, 'user'):
                st.success(f"Account created successfully for {new_username}! Please log in.")
                st.session_state['show_login'] = True
                st.session_state['logged_in'] = True  # Log the user in
                st.session_state['username'] = new_username  # Set the username for session state
                st.session_state['role'] = 'user'  # Set the role
                st.session_state['current_page'] = "Member Dashboard"  # Redirect to member dashboard

                # Display the "Go" button
                if st.button("Go", key="go_after_signup"):
                    st.success("You are now in the member dashboard.")
                    st.session_state['current_page'] = "Member Dashboard"  # Redirect to member dashboard

def login():
    st.title("Member Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Button label is always "Login" initially
    login_button_label = "Login"

    if st.button(login_button_label, key="login"):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            is_valid, role = verify_user(username, password)
            if is_valid:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['role'] = role
                
                # Redirect based on user role
                if role == 'admin':
                    st.session_state['current_page'] = "Dashboard"  # Redirect to admin dashboard
                    st.success(f"Welcome {username}! Redirecting to dashboard...")
                else:
                    st.success(f"Welcome {username}!")
                    st.session_state['current_page'] = "Member Dashboard"  # Redirect to member dashboard
            else:
                st.error("Invalid username or password")

    # Show the "Go" button for both admin and normal users after successful login
    if st.session_state.get('logged_in'):
        if st.button("Go", key="go_button"):
            if st.session_state['role'] == 'admin':
                st.success("You are now in the admin dashboard.")
                st.session_state['current_page'] = "User Data"  # Redirect to admin dashboard
            else:
                st.success("You are now in the member dashboard.")
                st.session_state['current_page'] = "Member Dashboard"  # Redirect to member dashboard

def logout():
    # Clear all session state related to login
    for key in list(st.session_state.keys()):
        if key in ['logged_in', 'username', 'role', 'current_page']:
            del st.session_state[key]
    st.success("Logged out successfully!")
    st.session_state['current_page'] = "Login"  # Redirect to login page

def member_dashboard():
    st.title("Member Dashboard")
    st.write(f"Welcome to the member dashboard, {st.session_state['username']}!")
    
    if st.session_state.get('role') == 'admin':
        st.write("You have admin privileges!")
    else:
        st.write("You have regular user privileges.")

def view_user_data():
    if not st.session_state.get('logged_in'):
        st.error("Please log in to access this page.")
        return
    
    if st.session_state.get('role') != 'admin':
        st.error("You don't have permission to view this page. Admins only.")
        return

    st.title("User Data")
    user_data = fetch_all_users_with_passwords()
    df = pd.DataFrame(user_data, columns=["Username", "Password", "Role"])
    st.dataframe(df)

def main():
    # Initialize the database
    init_db()

    # Sidebar options
    if st.session_state.get('logged_in'):
        st.sidebar.button("Log Out", on_click=logout)
        st.sidebar.button("User Data", on_click=lambda: st.session_state.update(current_page="User Data"))
    else:
        st.sidebar.button("Sign Up", on_click=lambda: st.session_state.update(current_page="Sign Up"))
        # Show "Sign In" option after successful signup
        if st.session_state.get('show_login'):
            st.sidebar.button("Sign In", on_click=lambda: st.session_state.update(current_page="Login"))

    # Check if the current page is set in session state, otherwise default to login
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Login"

    # Page rendering
    if st.session_state['current_page'] == "Login":
        login()
    elif st.session_state['current_page'] == "Sign Up":
        signup()
    elif st.session_state['current_page'] == "Member Dashboard":
        member_dashboard()
    elif st.session_state['current_page'] == "User Data":
        view_user_data()
    elif st.session_state['current_page'] == "Dashboard":
        st.write("Admin Dashboard Content")  # Placeholder for admin dashboard content

if __name__ == "__main__":
    main()
