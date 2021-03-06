# http://flask-sqlalchemy.pocoo.org/2.1/

import utils
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define our models

class Banks(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    slug = db.Column(db.String(40), unique=True)
    bank_name = db.Column(db.String(40))
    long_name = db.Column(db.String(255))
    country = db.Column(db.String(2))

    def __repr__(self):
        return '<Bank {} from {}>'.format(self.bank_name, self.country)

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.slug = utils.slugify(self.bank_name + '-' + self.country)


# VISA, Mastercard, Amex, JCB
class CardTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type_name = db.Column(db.String(255), unique=True)
    digits = db.Column(db.Integer, default=16)

    def __repr__(self):
        return '<CardType {}>'.format(self.type_name)


# CreditCard Model
class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    slug = db.Column(db.String(255), unique=True)
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card_types.id'))

    bank = db.relationship('Banks', backref=db.backref('cards'))
    type = db.relationship('CardTypes', backref=db.backref('cards'))

    card_name = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(3), nullable=False)

    # Usually there's a basic annual interest rate,
    # and a higher rate for cash withdrawals
    interest_rate = db.Column(db.Float) # APR
    # Some cards have a variable rate
    max_interest_rate = db.Column(db.Float)

    balance_transfer = db.Column(db.String(255))
    balance_transfer_interest_rate = db.Column(db.Float)

    cash_withdraw_interest_rate = db.Column(db.Float)
    cash_withdraw_fee = db.Column(db.String(40))
    interest_free_days = db.Column(db.Integer) # in days if ballance is paid in full

    opening_fee = db.Column(db.Float)
    yearly_fee = db.Column(db.Float)
    monthly_fee = db.Column(db.Float)
    other_fees = db.Column(db.String(255))

    # Cards have a minimum repayment amount
    minimum_repayment_percent = db.Column(db.Integer)
    minimum_repayment_sum = db.Column(db.Float)
    minimum_repayment = db.Column(db.String(255))

    additional_charges = db.Column(db.Text) # dormancy fee, statement copy,
    foreign_usage = db.Column(db.Text) # eg. non-sterling fee
    default_charges = db.Column(db.Text) # late payment, over-limit, returned payment

    min_credit_limit = db.Column(db.Integer)
    max_credit_limit = db.Column(db.Integer)
    credit_limit_comment = db.Column(db.String(255))

    # Renews every X years
    renew_years = db.Column(db.Integer)
    allows_additional_cards = db.Column(db.Boolean)

    # Most cards offer some sort of promotion,
    # like the first three months interest free, or more cashback.
    promotion = db.Column(db.Text)
    promo_duration = db.Column(db.Integer) # promotion duration in months
    rewards = db.Column(db.Text) # regular rewards after the promotion period has expired
    
    interest_free_installments = db.Column(db.Integer) # number of installments
    travel_insurance = db.Column(db.String(255)) # some cards offer insurance on travel
    purchase_protection = db.Column(db.Integer) # number of days for purchase protection

    # Most cards have eligibility criteria
    eligibility_employment_months = db.Column(db.Integer) # minimum employment period in months
    eligibility_min_salary = db.Column(db.Float)
    eligibility = db.Column(db.Text) # additional description of eligibility criteria

    internet_banking = db.Column(db.String(255))
    sms_notif = db.Column(db.String(255))
    is_contactless = db.Column(db.Boolean())

    offer_url = db.Column(db.String(255))

    comments = db.Column(db.Text)

    last_update = db.Column(db.DateTime)

    def __repr__(self):
        return '<Card {} from {} in {}>'.format(self.card_name, self.bank.bank_name, self.currency)

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.slug = utils.slugify(self.bank.bank_name + '-' + self.card_name)
