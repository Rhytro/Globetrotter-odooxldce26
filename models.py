from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for Stop and Activity (Many-to-Many)
stop_activity = db.Table(
    'stop_activity',
    db.Column('stop_id', db.Integer, db.ForeignKey('stop.id'), primary_key=True),
    db.Column(
        'activity_id', db.Integer, db.ForeignKey('activity.id'), primary_key=True
    ),
)


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True, nullable=False)
  password_hash = db.Column(db.String(256), nullable=False)
  name = db.Column(db.String(100), nullable=False)
  role = db.Column(
      db.String(50), default='user'
  )  # 'user' or 'admin' for analytics dashboard
  created_at = db.Column(
      db.DateTime, default=db.func.current_timestamp()
  )

  # Relationships
  trips = db.relationship(
      'Trip', backref='user', cascade='all, delete-orphan', lazy=True
  )


class City(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  country = db.Column(db.String(100), nullable=False)
  region = db.Column(db.String(100), nullable=False)
  cost_index = db.Column(
      db.Integer, default=3
  )  # 1 (Budget) to 5 (Luxury)
  popularity = db.Column(db.Integer, default=50)  # 1-100 scale
  image_url = db.Column(db.String(255), nullable=True)

  # Relationships
  activities = db.relationship(
      'Activity', backref='city', cascade='all, delete-orphan', lazy=True
  )


class Trip(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  name = db.Column(db.String(150), nullable=False)
  description = db.Column(db.Text, nullable=True)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date, nullable=False)
  budget_limit = db.Column(db.Float, default=1500.0)
  is_public = db.Column(db.Boolean, default=False)
  created_at = db.Column(
      db.DateTime, default=db.func.current_timestamp()
  )

  # Relationships
  stops = db.relationship(
      'Stop', backref='trip', cascade='all, delete-orphan', lazy=True
  )


class Stop(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
  city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
  order_index = db.Column(db.Integer, default=0)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date, nullable=False)

  # Relationships
  city = db.relationship('City')
  activities = db.relationship(
      'Activity',
      secondary=stop_activity,
      lazy='subquery',
      backref=db.backref('stops', lazy=True),
  )


class Activity(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
  name = db.Column(db.String(150), nullable=False)
  category = db.Column(
      db.String(50), nullable=False
  )  # Sightseeing, Food, Adventure, Culture
  cost = db.Column(db.Float, default=0.0)
  duration_hours = db.Column(db.Float, default=2.0)
  description = db.Column(db.Text, nullable=True)