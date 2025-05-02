from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

# Database model for transactions
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<Transaction {self.id}>'

