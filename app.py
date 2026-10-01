import json
import os
import re
import secrets
import warnings
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError
from datetime import datetime, timezone, timedelta
from functools import wraps
import click
import requests
import stripe
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
csrf = CSRFProtect()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    specifications = db.Column(db.JSON, nullable=False, default=dict)
    gallery = db.Column(db.JSON, nullable=False, default=list)
    variant_details = db.Column(db.JSON, nullable=False, default=dict)
    category = db.Column(db.String(40), nullable=False)
    price_cents = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    __table_args__ = (db.CheckConstraint('price_cents > 0'),)
    stock = db.Column(db.Integer, nullable=False, default=30)
    variants = db.Column(db.JSON, nullable=False, default=list)
    translations = db.Column(db.JSON, nullable=False, default=dict)
    badge = db.Column(db.String(30), nullable=False, default="New")
    sku = db.Column(db.String(80), nullable=False, default="")
    def public(self):
        return {k: getattr(self, k) for k in ('id', 'name', 'description', 'category', 'price_cents', 'image', 'available', 'stock', 'variants', 'translations', 'badge', 'sku', 'specifications', 'gallery', 'variant_details')}

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False, default=lambda: secrets.token_urlsafe(32))
    request_key = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    total_cents = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False, default='pending')
    fulfillment_status = db.Column(db.String(30), nullable=False, default='unfulfilled')
    stripe_session = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')

class OrderStatusChange(db.Model):
    __tablename__ = "order_status_changes"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True)
    previous_status = db.Column(db.String(30), nullable=False)
    new_status = db.Column(db.String(30), nullable=False)
    changed_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    order = db.relationship("Order", backref=db.backref("status_changes", order_by="OrderStatusChange.id.desc()", cascade="all, delete-orphan"))


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    price_cents = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    variant = db.Column(db.String(120), nullable=False, default='')
    translations = db.Column(db.JSON, nullable=False, default=dict)
    __table_args__ = (db.CheckConstraint('quantity > 0 AND quantity <= 20'),)

class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    failed_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime)

def notify(app, order):
    token, chat = app.config['TELEGRAM_BOT_TOKEN'], app.config['TELEGRAM_CHAT_ID']
    if not token or not chat:
        return
    try:
        response = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={
            'chat_id': chat, 'text': (f'ShopFlow: new order #{order.id}\n{order.name} · {order.email} · {order.phone}\n{order.address}, {order.city}\n' + '\n'.join(f'{i.name} [{i.variant or "Standard"}] × {i.quantity} — ${i.price_cents*i.quantity/100:.2f}' for i in order.items) + f'\nTotal: ${order.total_cents / 100:.2f} · {order.status}')[:4000]}, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        app.logger.warning('Telegram notification failed; order remains saved.')

def create_app(config=None):
    load_dotenv()
    app = Flask(__name__)
    production = os.getenv('APP_ENV') == 'production'
    secret = os.getenv('SECRET_KEY')
    if production and (not secret or len(secret) < 32):
        raise RuntimeError('Production requires a SECRET_KEY of at least 32 characters.')
    database = os.getenv('DATABASE_URL') or 'sqlite:///shopflow.db'
    if database.startswith('postgres://'):
        database = database.replace('postgres://', 'postgresql+psycopg://', 1)
    elif database.startswith('postgresql://'):
        database = database.replace('postgresql://', 'postgresql+psycopg://', 1)
    if production and database.startswith('sqlite'):
        raise RuntimeError('Production requires PostgreSQL DATABASE_URL.')
    app.config.update(SECRET_KEY=secret or secrets.token_hex(32), SQLALCHEMY_DATABASE_URI=database,
        SQLALCHEMY_TRACK_MODIFICATIONS=False, MAX_CONTENT_LENGTH=64 * 1024,
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_SECURE=production,
        PERMANENT_SESSION_LIFETIME=timedelta(hours=4), BASE_URL=os.getenv('BASE_URL', 'http://127.0.0.1:5000').rstrip('/'),
        STRIPE_SECRET_KEY=os.getenv('STRIPE_SECRET_KEY', ''), STRIPE_WEBHOOK_SECRET=os.getenv('STRIPE_WEBHOOK_SECRET', ''),
        TELEGRAM_BOT_TOKEN=os.getenv('TELEGRAM_BOT_TOKEN', ''), TELEGRAM_CHAT_ID=os.getenv('TELEGRAM_CHAT_ID', ''))
    if config:
        app.config.update(config)
    key = app.config['STRIPE_SECRET_KEY']
    if key and not key.startswith('sk_test_'):
        raise RuntimeError('Only Stripe sk_test_ keys are accepted. Live payments are disabled.')
    if key and not app.config['STRIPE_WEBHOOK_SECRET']:
        app.logger.warning('Incomplete Stripe test configuration; demo checkout is active.')
        app.config['STRIPE_SECRET_KEY'] = ''
        key = ''
    db.init_app(app)
    @app.before_request
    def body_limit():
        request.max_content_length = 9 * 1024 * 1024 if request.path == '/admin/photos' else 64 * 1024
    csrf.init_app(app)
    Migrate(app, db)

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self'; style-src 'self'; script-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        if request.path.startswith(('/api', '/admin', '/order')):
            response.headers['Cache-Control'] = 'no-store'
        return response

    def protected(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not session.get('admin_id') or not db.session.get(AdminUser, session['admin_id']):
                return redirect(url_for('login'))
            return fn(*args, **kwargs)
        return wrapped

    @app.get('/favicon.ico')
    def favicon():
        return redirect(url_for('static', filename='favicon.svg'))

    @app.get('/')
    def index():
        return render_template('store.html')

    @app.get('/api/products')
    def products():
        return jsonify([p.public() for p in db.session.scalars(db.select(Product).where(Product.active.is_(True)).order_by(Product.id))])

    @app.get('/api/products/<int:product_id>')
    def product(product_id):
        p = db.get_or_404(Product, product_id)
        if not p.active:
            abort(404)
        return jsonify(p.public())

    @app.get('/api/config')
    def public_config():
        return jsonify(csrf_token=generate_csrf(), payment_mode='stripe_test' if key else 'mock')

    @app.post('/api/checkout')
    def checkout():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error='Invalid checkout data.'), 400
        customer = data.get('customer', {})
        if not isinstance(customer, dict):
            return jsonify(error='Invalid customer.'), 400
        limits = {'name': (2, 120), 'email': (5, 254), 'phone': (7, 30), 'city': (2, 120), 'address': (5, 250)}
        clean = {}
        for field, (low, high) in limits.items():
            value = customer.get(field)
            if not isinstance(value, str) or not low <= len(value.strip()) <= high:
                return jsonify(error=f'Please provide a valid {field}.', field=field), 400
            clean[field] = value.strip()
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', clean['email']) or not re.fullmatch(r'[+\d ()-]{7,30}', clean['phone']):
            return jsonify(error='Please check your email and phone.'), 400
        items = data.get('items')
        request_key = data.get('request_key')
        if not isinstance(request_key, str) or not re.fullmatch(r'[a-zA-Z0-9-]{16,64}', request_key):
            return jsonify(error='Invalid request key.'), 400
        previous = db.session.scalar(db.select(Order).where(Order.request_key == request_key))
        # Scope retries to this browser session; do not disclose another buyer's order.
        if previous:
            if previous.token not in session.get('order_tokens', []):
                return jsonify(error='Request key already used.'), 409
            return jsonify(url=url_for('order_page', token=previous.token), order_id=previous.id, status=previous.status)
        if not isinstance(items, list) or not 1 <= len(items) <= 40:
            return jsonify(error='Your bag must contain 1–40 product variations.'), 400
        snapshots, seen = [], set()
        for item in items:
            if not isinstance(item, dict) or type(item.get('id')) is not int or type(item.get('quantity')) is not int or not 1 <= item['quantity'] <= 20:
                return jsonify(error='Invalid item quantity.'), 400

            p = db.session.get(Product, item['id'])
            if not p or not p.active or not p.available:
                return jsonify(error='A product is no longer available. Please update your bag.'), 409
            variant = item.get('variant', '')
            if not isinstance(variant, str) or (p.variants and variant not in p.variants) or (not p.variants and variant):
                return jsonify(error='Invalid product variant.'), 400
            identity = (p.id, variant)
            if identity in seen:
                return jsonify(error='Duplicate product variant.'), 400
            seen.add(identity)
            allocated = sum(i.quantity for i in snapshots if i.product_id == p.id) + item['quantity']
            if allocated > p.stock:
                return jsonify(error='Not enough stock. Please update your bag.'), 409
            snapshots.append(OrderItem(product_id=p.id, name=p.name, price_cents=(p.variant_details or {}).get(variant, {}).get('price_cents', p.price_cents), quantity=item['quantity'], variant=variant, translations=p.translations))
        order = Order(**clean, request_key=request_key, items=snapshots, total_cents=sum(i.price_cents * i.quantity for i in snapshots), status='pending' if key else 'demo_paid')
        db.session.add(order)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify(error='This checkout request is already being processed. Please check your orders before retrying.'), 409
        session['order_tokens'] = (session.get('order_tokens', []) + [order.token])[-10:]
        if key:
            try:
                payment = stripe.checkout.Session.create(api_key=key, idempotency_key=request_key, mode='payment', payment_method_types=['card'],
                    customer_email=order.email, metadata={'order_id': str(order.id)},
                    line_items=[{'price_data': {'currency': 'usd', 'unit_amount': i.price_cents, 'product_data': {'name': i.name + (' · ' + i.variant if i.variant else '')}}, 'quantity': i.quantity} for i in order.items],
                    success_url=app.config['BASE_URL'] + url_for('order_page', token=order.token),
                    cancel_url=app.config['BASE_URL'] + url_for('order_page', token=order.token))
                order.stripe_session = payment.id
                db.session.commit()
                target = payment.url
            except stripe.StripeError:
                order.status = 'payment_error'
                db.session.commit()
                notify(app, order)
                return jsonify(error='Test payment service unavailable. Your order is saved; contact the store.', order_id=order.id), 502
        else:
            target = url_for('order_page', token=order.token)
        notify(app, order)
        return jsonify(url=target, order_id=order.id, status=order.status), 201

    @app.get('/order/<token>')
    def order_page(token):
        order = db.session.scalar(db.select(Order).where(Order.token == token))
        if not order:
            abort(404)
        return render_template('order.html', order=order)

    @app.post('/api/stripe/webhook')
    @csrf.exempt
    def webhook():
        if not key:
            abort(503)
        try:
            event = stripe.Webhook.construct_event(request.data, request.headers.get('Stripe-Signature', ''), app.config['STRIPE_WEBHOOK_SECRET'])
        except (ValueError, stripe.SignatureVerificationError):
            abort(400)
        if event.get('livemode'):
            abort(400)
        if event['type'] == 'checkout.session.completed':
            payment = event['data']['object']
            order = db.session.scalar(db.select(Order).where(Order.stripe_session == payment['id']))
            if order and payment.get('payment_status') == 'paid' and payment.get('amount_total') == order.total_cents and payment.get('currency') == 'usd':
                order.status = 'paid_test'
                db.session.commit()
        return jsonify(received=True)

    @app.route('/admin/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            admin = db.session.scalar(db.select(AdminUser).where(AdminUser.username == request.form.get('username', '')[:80]))
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            if admin and admin.locked_until and admin.locked_until > now:
                error = 'Too many attempts. Try again in 15 minutes.'
            elif admin and check_password_hash(admin.password_hash, request.form.get('password', '')):
                admin.failed_attempts = 0
                admin.locked_until = None
                db.session.commit()
                session.clear()
                session['admin_id'] = admin.id
                session.permanent = True
                return redirect(url_for('admin'))
            else:
                if admin:
                    admin.failed_attempts += 1
                    if admin.failed_attempts >= 5:
                        admin.locked_until = now + timedelta(minutes=15)
                        admin.failed_attempts = 0
                    db.session.commit()
                error = 'Invalid username or password.'
        return render_template('login.html', error=error)

    @app.post('/admin/logout')
    @protected
    def logout():
        session.clear()
        return redirect(url_for('login'))

    @app.get('/admin')
    @protected
    def admin():
        return render_template('admin.html', products=db.session.scalars(db.select(Product).order_by(Product.id)).all(), orders=db.session.scalars(db.select(Order).order_by(Order.id.desc()).limit(100)).all())

    @app.post('/admin/photos')
    @protected
    def upload_photo():
        upload = request.files.get('photo')
        if not upload:
            return jsonify(error='Choose a photo'), 400
        data = upload.stream.read(8 * 1024 * 1024 + 1)
        if len(data) > 8 * 1024 * 1024:
            return jsonify(error='Photo is too large'), 413
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error', Image.DecompressionBombWarning)
                with Image.open(BytesIO(data)) as source:
                    if source.format not in ('JPEG', 'PNG', 'WEBP') or getattr(source, 'is_animated', False) or source.width * source.height > 20_000_000:
                        raise ValueError()
                    source.load()
                    image = ImageOps.exif_transpose(source).convert('RGBA' if 'A' in source.getbands() or 'transparency' in source.info else 'RGB')
                    image.thumbnail((2400, 2400))
                    image.info.clear()
                    folder = Path(app.config.get('PRODUCT_UPLOAD_FOLDER', Path(app.static_folder) / 'products' / 'uploads'))
                    folder.mkdir(parents=True, exist_ok=True)
                    name = secrets.token_hex(16) + '.webp'
                    image.save(folder / name, 'WEBP', quality=90)
            return jsonify(url='/static/products/uploads/' + name), 201
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombWarning, Image.DecompressionBombError):
            return jsonify(error='Use a JPG, PNG or WebP photo'), 400

    @app.errorhandler(413)
    def request_too_large(error):
        if request.path == '/admin/photos':
            return jsonify(error='Photo is too large'), 413
        return 'Request too large', 413

    @app.route('/admin/product/new', methods=['GET', 'POST'])
    @app.route('/admin/product/<int:product_id>', methods=['GET', 'POST'])
    @protected
    def edit_product(product_id=None):
        p = db.get_or_404(Product, product_id) if product_id else Product()
        error = None
        if request.method == 'POST':
            try:
                from decimal import Decimal, InvalidOperation
                name, description, category, image = [request.form.get(k, '').strip() for k in ('name', 'description', 'category', 'image')]
                price = Decimal(request.form.get('price', '0'))
                if not price.is_finite() or price != price.quantize(Decimal('.01')) or not 0 < price <= 100000:
                    raise ValueError()
                if not 2 <= len(name) <= 120 or not 5 <= len(description) <= 2000 or not 2 <= len(category) <= 40 or len(image) > 500 or not (image.startswith('/static/') ):
                    raise ValueError()
                p.name, p.description, p.category, p.image, p.price_cents = name, description, category, image, int(price * 100)
                if 'simple_editor' in request.form:
                    specs = {key: request.form.get('spec_'+key, '').strip() for key in ('material','dimensions','features')}
                    if any(len(value) > 500 for value in specs.values()):
                        raise ValueError()
                    p.specifications = {key: value for key, value in specs.items() if value}
                    if 'gallery' in request.form:
                        gallery = [value.strip() for value in request.form.get('gallery','').splitlines() if value.strip()]
                        if len(gallery)>8 or len(set(gallery))!=len(gallery) or any(len(value)>500 or not re.fullmatch(r'/static/(?!.*\.\.)[a-zA-Z0-9_./-]+',value) for value in gallery):
                            raise ValueError()
                        p.gallery = gallery
                p.stock = int(request.form.get('stock', '30'))
                if not 0 <= p.stock <= 100000:
                    raise ValueError()
                variants = request.form.getlist('variant_choices') if 'simple_editor' in request.form else [v.strip() for v in request.form.get('variants', '').split(',') if v.strip()]
                if len(variants) > 30 or any(len(v) > 120 for v in variants) or len(set(variants)) != len(variants):
                    raise ValueError()
                details = {v: dict((p.variant_details or {}).get(v, {})) for v in variants if v in (p.variant_details or {})}
                for index, variant in enumerate(p.variants or []):
                    raw = request.form.get('variant_price_' + str(index))
                    if raw is not None and variant in variants:
                        amount = Decimal(raw)
                        if not amount.is_finite() or amount != amount.quantize(Decimal('.01')) or not 0 < amount <= 100000:
                            raise ValueError()
                        details.setdefault(variant, {})['price_cents'] = int(amount * 100)
                p.variant_details = details
                p.variants = variants
                p.sku = request.form.get('sku', '').strip()[:80]
                p.badge = request.form.get('badge', 'New')
                if p.badge not in ('New','Sale','Bestseller',''):
                    raise ValueError()
                localized = (json.loads(request.form.get('translations', '{}') or '{}') if 'translations' in request.form else {locale: {field: request.form.get(field+'_'+locale, '').strip() for field in ('name','description') if request.form.get(field+'_'+locale, '').strip()} for locale in ('en','ru','uk')})
                if not isinstance(localized, dict) or any(lang not in ('en','ru','uk') or not isinstance(value, dict) or any(k not in ('name','description') or not isinstance(v, str) or len(v)>2000 for k,v in value.items()) for lang,value in localized.items()):
                    raise ValueError()
                if 'simple_editor' in request.form:
                    from product_translation import translate_product
                    localized = translate_product(name, description, p.translations or {})
                p.translations = localized
                p.active, p.available = 'active' in request.form, 'available' in request.form
                db.session.add(p)
                db.session.commit()
                return redirect(url_for('admin'))
            except (ValueError, InvalidOperation, TypeError) as exc:
                db.session.rollback()
                error = str(exc) if str(exc).startswith('Translation service unavailable.') else 'Check fields: positive price with two decimals and a local image URL, valid stock and comma-separated variants.'
        catalog = db.session.scalars(db.select(Product)).all()
        categories = sorted(set(['Sound','Carry','Home','Lifestyle'] + [item.category for item in catalog]))
        variant_categories = {}
        for item in catalog:
            for variant in (item.variants or []):
                variant_categories.setdefault(variant, set()).add(item.category)
        variant_choices = sorted(variant_categories)
        variant_categories = {variant: sorted(values) for variant, values in variant_categories.items()}
        selected_variants = request.form.getlist('variant_choices') if request.method == 'POST' else (p.variants or [])
        return render_template('edit.html', product=p, error=error, categories=categories, variant_choices=variant_choices, selected_variants=selected_variants, variant_categories=variant_categories)

    @app.get('/admin/order/<int:order_id>')
    @protected
    def admin_order(order_id):
        return render_template('order.html', order=db.get_or_404(Order, order_id), is_admin=True)

    @app.post('/admin/order/<int:order_id>/status')
    @protected
    def order_status(order_id):
        order = db.get_or_404(Order, order_id)
        status = request.form.get('status')
        if status not in ('unfulfilled', 'processing', 'shipped', 'cancelled'):
            abort(400)
        if order.fulfillment_status != status:
            db.session.add(OrderStatusChange(order_id=order.id, previous_status=order.fulfillment_status, new_status=status))
            order.fulfillment_status = status
            db.session.commit()
        return redirect(url_for('admin_order', order_id=order.id))

    @app.cli.command('upgrade-demo')
    def upgrade_demo():
        from sqlalchemy import inspect, text
        db.create_all()
        additions = {
            'products': {'variant_details': "JSON NOT NULL DEFAULT '{}'", 'gallery': "JSON NOT NULL DEFAULT '[]'", 'specifications': "JSON NOT NULL DEFAULT '{}'", 'stock': 'INTEGER NOT NULL DEFAULT 30', 'variants': "JSON NOT NULL DEFAULT '[]'", 'translations': "JSON NOT NULL DEFAULT '{}'", 'badge': "VARCHAR(30) NOT NULL DEFAULT 'New'", 'sku': "VARCHAR(80) NOT NULL DEFAULT ''"},
            'order_items': {'variant': "VARCHAR(120) NOT NULL DEFAULT ''", 'translations': "JSON NOT NULL DEFAULT '{}'"},
            'orders': {'fulfillment_status': "VARCHAR(30) NOT NULL DEFAULT 'unfulfilled'"}}
        with db.engine.begin() as connection:
            for table, columns in additions.items():
                existing = {c['name'] for c in inspect(connection).get_columns(table)}
                for column, definition in columns.items():
                    if column not in existing:
                        connection.execute(text(f'ALTER TABLE {table} ADD COLUMN {column} {definition}'))
        from seed import seed_products
        seed_products()
        click.echo('Additive schema upgrade and demo catalog complete; existing orders preserved.')

    @app.cli.command('init-db')
    def init_db():
        db.create_all()
        click.echo('Database initialized. For later schema changes use flask db migrations.')

    @app.cli.command('seed')
    def seed():
        from seed import seed_products
        seed_products()
        click.echo('Demo products ready.')

    @app.cli.command('create-admin')
    @click.option('--username', prompt=True)
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(username, password):
        if not 2 <= len(username) <= 80 or len(password) < 12:
            raise click.ClickException('Username must be 2–80 characters; password at least 12.')
        if db.session.scalar(db.select(AdminUser).where(AdminUser.username == username)):
            raise click.ClickException('Username already exists.')
        db.session.add(AdminUser(username=username, password_hash=generate_password_hash(password)))
        db.session.commit()
        click.echo('Admin created.')
    return app
