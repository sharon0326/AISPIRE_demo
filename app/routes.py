from datetime import timedelta

from flask import render_template, request, session, url_for, redirect, flash
from app import app
from app.forms import LoginForm, RegistrationForm
from app.generation import generate_montage_outlines, generate_narrative_outlines, generate_full_essay
from flask_login import current_user, login_user,logout_user,login_required
import sqlalchemy as sa
from app import db
from app.models import User, EssayHistory


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('collect_info'))

    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = db.session.scalar(
                sa.select(User).where(
                    sa.or_(
                        User.username == form.username.data,
                        User.email == form.username.data
                    )
                )
            )

            if not user or not user.check_password(form.password.data):
                flash('Invalid username/email or password', 'danger')
                return redirect(url_for('login'))

            login_user(user, remember=form.remember_me.data, duration=timedelta(days=30))
            next_page = request.args.get('next')
            return redirect(next_page or url_for('collect_info'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Login error: {str(e)}')
            flash('Authentication service unavailable. Please try later.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', title='Sign In', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pass
    return render_template('register.html')


@app.route('/register/individual', methods=['GET', 'POST'])
def register_individual():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        terms_agreed = request.form.get('terms')

        errors = []
        # Validation checks
        if not all([fullname, email, password]):
            errors.append('All fields are required')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        if User.query.filter_by(username=fullname).first():
            errors.append('Username already taken')
        if not terms_agreed:
            errors.append('You must agree to the terms')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register_individual.html')

        try:
            user = User(
                user_type='individual',
                username=fullname,
                email=email,
                company_name=None
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Individual account created successfully!', 'success')
            return redirect(url_for('collect_info'))

        except Exception as e:
            db.session.rollback()
            flash('Error creating account. Please try again.', 'danger')
            app.logger.error(f'Registration error: {str(e)}')
            return render_template('register_individual.html')

    return render_template('register_individual.html')


@app.route('/register/business', methods=['GET', 'POST'])
def register_business():
    if request.method == 'POST':
        company = request.form.get('company')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        terms_agreed = request.form.get('terms')

        errors = []

        # Validation checks
        if not all([company, fullname, email, password]):
            errors.append('All fields are required')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        if User.query.filter_by(username=fullname).first():
            errors.append('Username already taken')
        if User.query.filter_by(company_name=company).first():
            errors.append('Company name already registered')
        if not terms_agreed:
            errors.append('You must agree to the terms')

        # Early return on validation errors
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register_business.html')

        try:
            user = User(
                user_type='business',
                company_name=company,
                username=fullname,
                email=email
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            flash('Business account created successfully!', 'success')
            return redirect(url_for('collect_info'))

        except Exception as e:
            db.session.rollback()
            flash('Database error: Account creation failed', 'danger')
            app.logger.error(f'Registration error: {str(e)}')
            return render_template('register_business.html')  # Return immediately

    return render_template('register_business.html')

#@app.route('/', methods=['GET', 'POST'])
#@app.route('/index', methods=['GET', 'POST'])
@app.route('/collect-info', methods=['GET', 'POST'])
@login_required
def collect_info():
    if request.method == 'POST':
        session['essay_data'] = {
            'topic': request.form['topic'],
            'word_limit': str(request.form['word_limit']),
            'notes': request.form['notes'],
            'outline_narrative': "",
            'outline_montage': "",
            'selected_outline': ""
        }
        outline_narrative = generate_narrative_outlines(
            session['essay_data']['notes'],
            session['essay_data']['topic']
        )
        outline_montage = generate_montage_outlines(
            session['essay_data']['notes'],
            session['essay_data']['topic']
        )

        # Store full outlines in session
        session['essay_data']['outline_narrative'] = outline_narrative
        session['essay_data']['outline_montage'] = outline_montage
        session.modified = True

        return render_template('gen_outlines.html',
                               outline_narrative=outline_narrative,
                               outline_montage= outline_montage)
    return render_template('collect_info.html')

@app.route('/select-outline', methods=['POST'])
@login_required
def select_outline():
    essay_data = session.get('essay_data', {})
    selected_type = request.form['outline_choice']

    essay_data['outline_type'] = selected_type
    # Store chosen outline content
    if selected_type == 'narrative':
        essay_data['selected_outline'] = essay_data['outline_narrative']
    else:
        essay_data['selected_outline'] = essay_data['outline_montage']

    session['essay_data'] = essay_data
    return redirect(url_for('generate_essay'))

@app.route('/generate-essay', methods=['GET'])
@login_required
def generate_essay():
    essay_data = session.get('essay_data', {})

    required_keys = ['topic', 'notes', 'word_limit', 'outline_type', 'selected_outline']
    if not all(key in essay_data for key in required_keys):
        return redirect(url_for('index'))

    # Generate essay with all parameters
    essay = generate_full_essay(
        topic=essay_data['topic'],
        notes=essay_data['notes'],
        word_limit=essay_data['word_limit'],
        outline_type=essay_data['outline_type'],
        selected_outline=essay_data['selected_outline']
    )

    new_essay = EssayHistory(
        user_id=current_user.id,
        topic=essay_data['topic'],
        notes=essay_data['notes'],
        word_limit=essay_data['word_limit'],
        outline_type=essay_data['outline_type'],
        selected_outline=str(essay_data['selected_outline']),
        generated_essay=str(essay)
    )
    db.session.add(new_essay)
    db.session.commit()

    session.pop('essay_data', None)

    return render_template('gen_essay.html', essay=essay)