from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

from models import Activity, City, Stop, Trip, User, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'odoo-ldce-hackathon-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///globetrotter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


# --- DATABASE SEEDING UTILITY ---
def seed_database():
  if not City.query.first():
    c1 = City(
        name='Paris',
        country='France',
        region='Europe',
        cost_index=4,
        popularity=95,
        image_url='paris.jpg',
    )
    c2 = City(
        name='Tokyo',
        country='Japan',
        region='Asia',
        cost_index=4,
        popularity=98,
        image_url='tokyo.jpg',
    )
    c3 = City(
        name='Kyoto',
        country='Japan',
        region='Asia',
        cost_index=3,
        popularity=85,
        image_url='kyoto.jpg',
    )

    db.session.add_all([c1, c2, c3])
    db.session.commit()

    # Add sample activities
    a1 = Activity(
        city_id=c1.id,
        name='Louvre Museum Tour',
        category='Sightseeing',
        cost=25.0,
        duration_hours=3.0,
        description='See the Mona Lisa.',
    )
    a2 = Activity(
        city_id=c1.id,
        name='Seine River Cruise',
        category='Adventure',
        cost=40.0,
        duration_hours=1.5,
        description='Evening boat ride.',
    )
    a3 = Activity(
        city_id=c2.id,
        name='TeamLab Planets',
        category='Culture',
        cost=30.0,
        duration_hours=2.5,
        description='Immersive art museum.',
    )

    db.session.add_all([a1, a2, a3])

    # Create admin user
    admin_user = User(
        email='admin@globetrotter.com',
        name='Admin Evaluator',
        role='admin',
        password_hash=generate_password_hash('admin123'),
    )
    db.session.add(admin_user)
    db.session.commit()


# --- AUTHENTICATION ROUTES ---
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
      login_user(user)
      flash('Logged in successfully!', 'success')
      return redirect(url_for('dashboard'))
    flash('Invalid email or password.', 'danger')
  return render_template('login.html')  # Expects template or use inline block


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter_by(email=email).first():
      flash('Email already registered.', 'warning')
      return redirect(url_for('signup'))

    new_user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role='user',
    )
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    flash('Account created successfully!', 'success')
    return redirect(url_for('dashboard'))
  return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Logged out successfully.', 'info')
  return redirect(url_for('login'))


# --- CORE APP ROUTES ---
@app.route('/')
@login_required
def dashboard():
  user_trips = (
      Trip.query.filter_by(user_id=current_user.id)
      .order_by(Trip.start_date.desc())
      .limit(5)
      .all()
  )
  popular_cities = City.query.order_by(City.popularity.desc()).limit(4).all()
  return render_template(
      'dashboard.html', trips=user_trips, popular_cities=popular_cities
  )


@app.route('/trips')
@login_required
def my_trips():
  trips = Trip.query.filter_by(user_id=current_user.id).all()
  return render_template('my_trips.html', trips=trips)


@app.route('/trips/new', methods=['GET', 'POST'])
@login_required
def create_trip():
  if request.method == 'POST':
    name = request.form.get('name')
    description = request.form.get('description')
    start_date = datetime.strptime(
        request.form.get('start_date'), '%Y-%m-%d'
    ).date()
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
    budget = float(request.form.get('budget_limit', 1000.0))

    trip = Trip(
        user_id=current_user.id,
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget_limit=budget,
    )
    db.session.add(trip)
    db.session.commit()
    flash('Trip created! Now add your stops.', 'success')
    return redirect(url_for('itinerary_builder', trip_id=trip.id))
  return render_template('create_trip.html')


@app.route('/trips/<int:trip_id>/builder', methods=['GET', 'POST'])
@login_required
def itinerary_builder(trip_id):
  trip = Trip.query.get_or_404(trip_id)
  if trip.user_id != current_user.id:
    return redirect(url_for('dashboard'))

  cities = City.query.all()
  if request.method == 'POST':
    city_id = int(request.form.get('city_id'))
    start_date = datetime.strptime(
        request.form.get('start_date'), '%Y-%m-%d'
    ).date()
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()

    stop = Stop(
        trip_id=trip.id,
        city_id=city_id,
        start_date=start_date,
        end_date=end_date,
        order_index=len(trip.stops) + 1,
    )
    db.session.add(stop)
    db.session.commit()
    flash('Stop added successfully!', 'success')
    return redirect(url_for('itinerary_builder', trip_id=trip.id))
  return render_template('itinerary_builder.html', trip=trip, cities=cities)


@app.route('/trips/<int:trip_id>/budget')
@login_required
def trip_budget(trip_id):
  trip = Trip.query.get_or_404(trip_id)
  # Calculate automatic cost breakdown
  total_activity_cost = 0
  for stop in trip.stops:
    for activity in stop.activities:
      total_activity_cost += activity.cost

  # Mock estimate costs for stays & transport based on days/cities
  estimated_stay_cost = len(trip.stops) * 120.0
  estimated_transport_cost = max(0, (len(trip.stops) - 1)) * 150.0
  total_cost = total_activity_cost + estimated_stay_cost + estimated_transport_cost

  is_overbudget = total_cost > trip.budget_limit

  return render_template(
      'budget.html',
      trip=trip,
      activity_cost=total_activity_cost,
      stay_cost=estimated_stay_cost,
      transport_cost=estimated_transport_cost,
      total_cost=total_cost,
      is_overbudget=is_overbudget,
  )


@app.route('/shared/<int:trip_id>')
def public_itinerary(trip_id):
  trip = Trip.query.get_or_404(trip_id)
  if not trip.is_public and (
      not current_user.is_authenticated or trip.user_id != current_user.id
  ):
    flash('This trip is private.', 'danger')
    return redirect(url_for('dashboard'))
  return render_template('public_itinerary.html', trip=trip)


@app.route('/cities/search', methods=['GET'])
def city_search():
  query = request.args.get('q', '')
  region = request.args.get('region', '')
  cities_query = City.query
  if query:
    cities_query = cities_query.filter(City.name.ilike(f'%{query}%'))
  if region:
    cities_query = cities_query.filter_by(region=region)
  cities = cities_query.all()

  # Return JSON if requested via fetch/AJAX, otherwise render template
  if request.headers.get('Accept') == 'application/json':
    return jsonify([{c.id, c.name, c.country, c.cost_index} for c in cities])
  return render_template('city_search.html', cities=cities)

@app.route('/activities/search', methods=['GET'])
def activity_search():
  category = request.args.get('category', '')
  max_cost = request.args.get('max_cost', type=float)
  city_id = request.args.get('city_id', type=int)

  query = Activity.query
  if category:
    query = query.filter_by(category=category)
  if max_cost:
    query = query.filter(Activity.cost <= max_cost)
  if city_id:
    query = query.filter_by(city_id=city_id)

  activities = query.all()
  return render_template('activity_search.html', activities=activities)

@app.route('/trips/<int:trip_id>/copy', methods=['POST'])
@login_required
def copy_trip(trip_id):
  original_trip = Trip.query.get_or_404(trip_id)
  if not original_trip.is_public and original_trip.user_id != current_user.id:
    flash('Cannot copy private trip.', 'danger')
    return redirect(url_for('dashboard'))

  new_trip = Trip(
      user_id=current_user.id,
      name=f'Copy of {original_trip.name}',
      description=original_trip.description,
      start_date=original_trip.start_date,
      end_date=original_trip.end_date,
      budget_limit=original_trip.budget_limit,
      is_public=False,
  )
  db.session.add(new_trip)
  db.session.commit()

  for stop in original_trip.stops:
    new_stop = Stop(
        trip_id=new_trip.id,
        city_id=stop.city_id,
        order_index=stop.order_index,
        start_date=stop.start_date,
        end_date=stop.end_date,
    )
    new_stop.activities = (
        stop.activities
    )  # Copy the many-to-many relationship
    db.session.add(new_stop)
  db.session.commit()

  flash('Itinerary successfully cloned to your account!', 'success')
  return redirect(url_for('my_trips'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  if request.method == 'POST':
    current_user.name = request.form.get('name')
    current_user.email = request.form.get('email')
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))
  return render_template('profile.html')

@app.route('/trips/<int:trip_id>/timeline')
@login_required
def trip_timeline(trip_id):
  trip = Trip.query.get_or_404(trip_id)
  if trip.user_id != current_user.id and not trip.is_public:
    flash('Unauthorized access.', 'danger')
    return redirect(url_for('dashboard'))
  # Sort stops chronologically
  sorted_stops = sorted(trip.stops, key=lambda s: s.start_date)
  return render_template('timeline.html', trip=trip, stops=sorted_stops)

@app.route('/admin')
@login_required
def admin_dashboard():
  if current_user.role != 'admin':
    flash('Unauthorized access.', 'danger')
    return redirect(url_for('dashboard'))

  total_users = User.query.count()
  total_trips = Trip.query.count()
  total_cities = City.query.count()
  return render_template(
      'admin.html',
      total_users=total_users,
      total_trips=total_trips,
      total_cities=total_cities,
  )


# --- ERROR HANDLERS ---
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
    seed_database()
  app.run(debug=True, port=5000)