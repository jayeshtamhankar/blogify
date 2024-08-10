from flask import Flask, render_template, redirect, url_for, request, flash, session
from config import Config
import bcrypt
from data import read_user_data, write_user_data, read_blog_data, write_blog_data
from helpers import generate_id, time_stamp
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/home')
def home():

    blog_data = read_blog_data()

    blog_posts = []

    for blog_container in blog_data:
        for blog in blog_container['blogs']:
            blog_post = {
                'blog_id': blog['head']['blog_id'],
                'blog_author': blog['body']['author'],
                'publish_data': datetime.strptime(blog['head']['publish_data'], '%d/%m/%y-%H:%M:%S').strftime("%d/%m/%Y"),
                'blog_title': blog['body']['title'],
                'blog_introduction': blog['body']['introduction'],
                'blog_content': blog['body']['content'],
                'blog_conclusion': blog['body']['conclusion'],
            }
            blog_posts.append(blog_post)

    return render_template('home.html', blog_posts=blog_posts)


@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/sign_up_form', methods=['GET', 'POST'])
def sign_up_form():
    user_id = generate_id()
    name = request.form.get('Name')
    gender = request.form.get('Gender')
    date_of_birth = request.form.get('Date_Of_Birth')
    contact_number = request.form.get('Contact_Number')
    email = request.form.get('Email')
    username = request.form.get('Username')
    password = request.form.get('Password')
    confirm_password = request.form.get('Confirm_Password')
    created_at = time_stamp()

    if not name:
        flash('Please enter your name.', 'warning')
        return redirect(url_for('sign_up'))
        
    if not gender:
        flash('Please select your gender.', 'warning')
        return redirect(url_for('sign_up'))
        
    if not date_of_birth:
        flash('Please enter your date of birth.', 'warning')
        return redirect(url_for('sign_up'))
        
    if not contact_number:
        flash('Please enter your contact number.', 'warning')
        return redirect(url_for('sign_up'))
        
    if not email:
        flash('Please enter your email address.', 'warning')
        return redirect(url_for('sign_up'))
        
    if not username:
        flash('Please choose a username.', 'warning')
        return redirect(url_for('sign_up'))

    if not password:
        flash('Please choose a password.', 'warning')
        return redirect(url_for('sign_up'))
        
    if not confirm_password:
        flash('Please confirm your password.', 'warning')
        return redirect(url_for('sign_up'))
        
    if password != confirm_password:
        flash('Passwords do not match. Please try again.', 'warning')
        return redirect(url_for('sign_up'))
        
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = {
        'user id': user_id,
        'name': name,
        'gender': gender,
        'date_of_birth': date_of_birth,
        'contact_number': contact_number,
        'email': email,
        'username': username,
        'password': hashed_password,
        'createdAt': created_at
    }

    user_data = read_user_data()
    user_data.append(new_user)

    write_user_data(user_data)

    return redirect(url_for('sign_up'))
    

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')


@app.route('/sign_in_form', methods=['GET', 'POST'])
def sign_in_form():
    user_data = read_user_data()

    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        for user in user_data:
            if username == user['username']:
                if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    session['logged_in'] = True
                    session['user_id'] = user['user id'] 
                    return redirect(url_for('home')) 
                else:
                    flash('Invalid credentials. Please try again.', 'warning')
                    return redirect(url_for('sign_in'))
            else:
                flash('User not found. Please sign up first.', 'warning')  
        return redirect(url_for('sign_in'))


@app.route('/profile')
def profile():
    if session.get('logged_in'):
        user_id = session.get('user_id')

        user_data = read_user_data()
        blog_data = read_blog_data()

        blog_posts = []

        for user in user_data:
            if user['user id'] == user_id:
                user_info = {
                    "name": user['name'],
                    "gender": user['gender'],
                    "date_of_birth": user['date_of_birth'],
                    "contact_number": user['contact_number'],
                    "email": user['email'],
                    "username": user['username']
                }

        for blog_container in blog_data:
            for blog in blog_container['blogs']:
                if blog['head']['author_id'] == user_id:

                    blog_post = {
                        'blog_id': blog['head']['blog_id'],
                        'blog_author': blog['body']['author'],
                        'publish_data': datetime.strptime(blog['head']['publish_data'], '%d/%m/%y-%H:%M:%S').strftime("%d/%m/%Y"),
                        'blog_title': blog['body']['title'],
                        'blog_introduction': blog['body']['introduction'],
                        'blog_content': blog['body']['content'],
                        'blog_conclusion': blog['body']['conclusion'],
                    }

                    blog_posts.append(blog_post)

        return render_template('profile.html', user_info=user_info, blog_posts=blog_posts)
    else:
        return redirect(url_for('sign_in'))


@app.route('/edit_profile')
def edit_profile():
    if session.get('logged_in'):
        user_id = session.get('user_id')

        user_data = read_user_data()

        for user in user_data:
            if user['user id'] == user_id: 
                return render_template('edit_profile.html', user=user)
    else:
        return redirect(url_for('sign_in'))


@app.route('/edit_basic_details', methods=['GET', 'POST'])
def edit_basic_details():
    if session.get('logged_in'):
        user_id = session.get('user_id')

        user_data = read_user_data()

        for user in user_data:
            if user['user id'] == user_id:
                if request.method == 'POST':
                    new_name = request.form.get('Name')
                    new_gender = request.form.get('Gender')
                    new_date_of_birth = request.form.get('Date_Of_Birth')
                    
                    updated_at = time_stamp()

                    user['updated_at'] = updated_at
                    
                    if new_name:
                        user['name'] = new_name
                    if new_gender:
                        user['gender'] = new_gender
                    if new_date_of_birth:
                        user['date_of_birth'] = new_date_of_birth

                    write_user_data(user_data)
                    return redirect(url_for('edit_profile'))
                
    return redirect(url_for('edit_profile'))


@app.route('/add_blog', methods=['GET', 'POST'])
def add_blog():
    if session.get('logged_in'):
        return render_template('add_blog.html')
    else:
        return redirect(url_for('sign_in'))


@app.route('/add_blog_form', methods=['GET', 'POST'])
def add_blog_form():
    if session.get('logged_in'):
        user_id = session.get('user_id')
        
        user_data = read_user_data()
        blog_data = read_blog_data()
        
        for user in user_data:
            if user['user id'] == user_id:
                if request.method == 'POST':
                    title = request.form.get('Title')
                    introduction = request.form.get('Introduction')
                    content = request.form.get('Content')
                    conclusion = request.form.get('Conclusion')
                    
                    blog_id = generate_id()
                    publish_date = time_stamp()
                    author_id = user['user id']
                    author_name = user['name']

                    new_blog = {
                        'head': {
                            'blog_id': blog_id,
                            'author_id': author_id,
                            'publish_data': publish_date,
                        },
                        'body': {
                            'author': author_name,
                            'title': title,
                            'introduction': introduction,
                            'content': content,
                            'conclusion': conclusion
                        },
                        'footer': {
                        }
                    }

                    blog_data[0]['blogs'].append(new_blog)
                    write_blog_data(blog_data)

    return redirect(url_for('add_blog'))


@app.route('/view_blog')
@app.route('/view_blog/<blog_id>')
def view_blog(blog_id=None):

    if not blog_id:
        print('You must provide a blog')
        return redirect(url_for('home'))

    blog_data = read_blog_data()

    for blog_container in blog_data:
        for blog in blog_container['blogs']:
            if blog['head']['blog_id'] == blog_id:
                return render_template('view_blog.html', blog=blog)


@app.route('/edit_blog')
@app.route('/edit_blog/<blog_id>')
def edit_blog(blog_id=None):

    if session.get('logged_in'):
        blog_data = read_blog_data()

        if not blog_id:
            print('You must provide a blog')
            return redirect(url_for('home'))
        
        for blog_container in blog_data:
            for blog in blog_container['blogs']:
                if blog['head']['blog_id'] == blog_id:
                    return render_template('edit_blog.html', blog=blog)
        
        return render_template('edit_blog.html')
        

@app.route('/edit_blog_form/<blog_id>', methods=['GET', 'POST'])
def edit_blog_form(blog_id=None):
    if session.get('logged_in'):
        user_id = session.get('user_id')
        blog_data = read_blog_data()

        if not blog_id:
            print('You must provide a blog')
            return redirect(url_for('home'))
        
        for blog_container in blog_data:
            for blog in blog_container['blogs']:
                if blog['head']['blog_id'] == blog_id and blog['head']['author_id'] == user_id:
                    if request.method == 'POST':
                        title = request.form.get('Title')
                        introduction = request.form.get('Introduction')
                        content = request.form.get('Content')
                        conclusion = request.form.get('Conclusion')

                        updated_at = time_stamp()

                        blog['body']['title'] = title
                        blog['body']['introduction'] = introduction
                        blog['body']['content'] = content
                        blog['body']['conclusion'] = conclusion
                        blog['head']['updated_at'] = updated_at

                        write_blog_data(blog_data)

                        return redirect(url_for('edit_blog', blog_id=blog_id))


@app.route('/delete_blog/<blog_id>')
def delete_blog(blog_id=None):
    
    user_id = session.get('user_id')

    blog_data = read_blog_data()

    for blog_container in blog_data:
        for blog in blog_container['blogs']:
            if blog['head']['blog_id'] == blog_id and blog['head']['author_id'] == user_id:
                blog_container['blogs'].remove(blog)
                write_blog_data(blog_data)
                return redirect(url_for('profile'))

@app.route('/sign_out')
def sign_out():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2525,  debug=True)
