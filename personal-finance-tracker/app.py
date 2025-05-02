from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/finance_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Database model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<Transaction {self.id}>'

# Home route: list all transactions
@app.route('/')
def index():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('index.html', transactions=transactions)

# Add a new transaction
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            category = request.form['category']
            type = request.form['type']
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            description = request.form.get('description', '')

            new_transaction = Transaction(
                amount=amount,
                category=category,
                type=type,
                date=date,
                description=description
            )
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('add_transaction.html')

# Summary view of income, expenses, and balance
@app.route('/summary')
def summary():
    transactions = Transaction.query.all()
    income = sum(t.amount for t in transactions if t.type == 'income')
    expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income - expense
    return render_template('summary.html', income=income, expense=expense, balance=balance)

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
