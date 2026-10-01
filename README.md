# ShopFlow

<p align="center">
  <strong>Full-Stack Multilingual E-Commerce Platform</strong>
</p>

<p align="center">
  <a href="https://shopflow-q6r6.onrender.com">
    <strong>🌐 Live Demo</strong>
  </a>
  &nbsp;•&nbsp;
  <a href="https://github.com/roman-webdev/ShopFlow">
    <strong>💻 Source Code</strong>
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/PostgreSQL-Neon-336791?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/tests-28%20passed-brightgreen" alt="Tests">
  <img src="https://img.shields.io/badge/i18n-EN%20%7C%20RU%20%7C%20UA-6FA58D" alt="Languages">
  <img src="https://img.shields.io/badge/deploy-Render-46E3B7" alt="Render">
</p>

---

## About ShopFlow

**ShopFlow** is a full-stack e-commerce platform built with Flask, PostgreSQL and vanilla JavaScript.

The project demonstrates a complete online-store workflow:

**product discovery → variants → favorites → cart → checkout → order persistence → admin management**

ShopFlow was created as a portfolio project with a strong focus on:

- polished UI/UX;
- responsive design;
- interactive product experiences;
- multilingual interfaces;
- secure backend architecture;
- production deployment;
- maintainable code;
- realistic e-commerce workflows.

The production version is deployed on **Render** and uses **Neon PostgreSQL**.

---

## 🖼 Preview

### Storefront

<p align="center">
  <img src="docs/qa/screenshots/storefront-v2.png" alt="ShopFlow storefront" width="100%">
</p>

### Product Catalog

<p align="center">
  <img src="docs/qa/screenshots/catalog-v2.png" alt="ShopFlow product catalog" width="100%">
</p>

### Product Experience

<p align="center">
  <img src="docs/qa/screenshots/product-v2.png" alt="ShopFlow product details" width="100%">
</p>

### Checkout

<p align="center">
  <img src="docs/qa/screenshots/checkout-v2.png" alt="ShopFlow checkout" width="100%">
</p>

### Admin Dashboard

<p align="center">
  <img src="docs/qa/screenshots/admin-v2.png" alt="ShopFlow admin dashboard" width="100%">
</p>

---

# ✨ Key Features

## Customer Experience

- 18 demo products
- Responsive storefront
- Product categories
- Search
- Filters
- Sorting
- Product color variants
- Variant-specific images
- Variant-specific pricing
- Product galleries
- Product specifications
- Favorites / wishlist
- Recently viewed products
- Product comparison
- Related products
- Persistent shopping cart
- Quantity controls
- Remove from cart
- Clear cart
- Checkout flow
- Order confirmation
- Multilingual UI
- Responsive desktop / tablet / mobile layouts

---

## 🎨 UI & Motion Design

ShopFlow is designed to feel like a modern e-commerce experience rather than a traditional Flask template application.

The interface includes:

- animated hero content;
- section reveal animations;
- smooth transitions;
- product-card interactions;
- hover effects;
- dynamic product visuals;
- interactive category blocks;
- mood-based product discovery;
- product galleries;
- carousel components;
- animated feedback;
- toast notifications;
- interactive cart behavior;
- responsive navigation;
- motion-aware user interactions;
- `prefers-reduced-motion` support.

The visual system uses a soft **mint / cream / peach** palette with large typography and product-focused layouts.

---

# 🌍 Internationalization

ShopFlow supports three interface languages:

- 🇬🇧 English
- 🇷🇺 Russian
- 🇺🇦 Ukrainian

The selected language is persisted between sessions.

Localization covers:

- navigation;
- homepage content;
- categories;
- catalog;
- filters;
- sorting;
- product cards;
- product details;
- product variants;
- cart;
- checkout;
- validation messages;
- success and error states;
- admin interface;
- order states;
- UI notifications.

Product names and descriptions can also be localized.

---

# 🛍 Product Catalog

The demo catalog currently contains **18 products** across several categories.

Product functionality includes:

- SKU;
- category;
- price;
- stock;
- availability;
- badges;
- color variants;
- variant-specific images;
- variant-specific pricing;
- product galleries;
- specifications;
- localized descriptions.

Supported product badges include:

- Bestseller
- New
- Sale
- Out of stock

---

# 🎨 Product Variants

ShopFlow supports multiple variants for a product.

Variants can contain:

- color;
- custom display name;
- image;
- price;
- stock-related information.

Different variants of the same product remain separate cart items.

A selected variant is preserved through:

```text
Product → Cart → Checkout → Order
```

---

# ❤️ Favorites

Products can be added to favorites directly from the storefront.

Favorite state is persisted on the client side so products remain saved between page reloads.

---

# 👁 Recently Viewed

ShopFlow remembers recently viewed products and provides a dedicated browsing-history experience.

This allows users to quickly return to products they previously explored.

---

# ⚖ Product Comparison

Customers can add products to comparison and review their characteristics side by side.

Comparison is designed as an additional discovery tool rather than a separate purchasing flow.

---

# 🛒 Shopping Cart

The cart supports:

- add product;
- remove product;
- increase quantity;
- decrease quantity;
- clear cart;
- preserve selected variants;
- realtime subtotal calculation;
- persistent state;
- empty-cart state;
- direct checkout transition.

Cart information survives page reloads.

---

# 💳 Checkout

ShopFlow includes a complete checkout workflow.

Customer information includes:

- full name;
- email;
- phone;
- city;
- delivery address.

The backend validates checkout data before creating an order.

Order data contains:

- customer information;
- products;
- selected variants;
- quantity;
- unit price;
- total;
- payment state;
- fulfillment state;
- creation timestamp.

---

# 💰 Stripe Safety

Stripe support is intentionally restricted to **test / demo usage**.

If Stripe credentials are not configured, ShopFlow automatically uses a clearly labeled demo checkout flow.

No money is charged.

ShopFlow also intentionally rejects live Stripe secret keys in the current demo configuration.

Supported environment variables:

```env
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

The application also includes webhook signature validation support.

---

# 🔐 CSRF Protection

ShopFlow uses CSRF protection for state-changing actions.

The checkout flow refreshes the CSRF token before submitting an order, preventing expired page sessions from silently breaking checkout.

Backend failures are logged safely without exposing:

- SQL parameters;
- secrets;
- customer data;
- credentials.

---

# 🤖 Telegram Notifications

Telegram order notifications are optional.

When configured, ShopFlow can send new-order information to an administrator.

Notifications may include:

- order ID;
- customer;
- products;
- selected variants;
- quantity;
- total.

Environment variables:

```env
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

If Telegram is not configured, checkout continues normally.

---

# 🛠 Admin Dashboard

ShopFlow includes a protected administration interface.

The dashboard provides:

- total products;
- total orders;
- demo revenue;
- fulfillment metrics;
- product search;
- product management;
- order search;
- order filtering;
- payment status;
- fulfillment status;
- status history.

---

## Product Management

Administrators can manage:

- product name;
- SKU;
- category;
- price;
- stock;
- availability;
- descriptions;
- product variants;
- colors;
- variant prices;
- cover image;
- gallery images;
- image order.

Product images can be uploaded and reordered directly from the admin interface.

---

## Automatic Product Translation

ShopFlow includes a translation workflow for product content.

Product names and descriptions can be translated automatically through an external translation service.

Translation errors are handled without silently overwriting valid product data.

---

# 📦 Order Management

Administrators can:

- search orders;
- filter orders;
- open order details;
- inspect customer information;
- view totals;
- view payment state;
- change fulfillment status;
- inspect status history.

Supported fulfillment states include states such as:

```text
New
Processing
Completed
Cancelled
```

Status changes are persisted in the database.

Cancelled orders are excluded from relevant dashboard revenue calculations.

---

# 🧱 Tech Stack

## Backend

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-WTF
- PostgreSQL
- SQLite
- psycopg
- Waitress

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- Responsive Design
- Custom animations
- Client-side state management

## Integrations

- Stripe API
- Telegram Bot API
- MyMemory Translation API

## Tooling

- Pytest
- python-dotenv
- Pillow
- Requests
- Git
- GitHub

## Production

- Render
- Neon PostgreSQL

---

# 🗄 Database

## Local Development

If `DATABASE_URL` is empty, ShopFlow uses SQLite:

```text
instance/shopflow.db
```

## Production

Production uses PostgreSQL through:

```env
DATABASE_URL=
```

Example SQLAlchemy connection format:

```text
postgresql+psycopg://user:password@host/database?sslmode=require
```

The production ShopFlow deployment currently uses **Neon PostgreSQL**.

---

# 🚀 Live Deployment

ShopFlow is deployed publicly using:

- **Render** — Python / Flask web service
- **Neon** — PostgreSQL database
- **Waitress** — production WSGI server

### Live Demo

https://shopflow-q6r6.onrender.com

> Render's free tier may spin the service down after inactivity.  
> The first request after a period of inactivity may take approximately 50 seconds or more while the service wakes up.

---

# ⚙ Production Configuration

Render build command:

```bash
pip install -r requirements.txt
```

Render start command:

```bash
waitress-serve --host=0.0.0.0 --port=$PORT --call app:create_app
```

Recommended environment variables:

```env
APP_ENV=production

SECRET_KEY=<strong random secret>

DATABASE_URL=<PostgreSQL connection string>

BASE_URL=https://shopflow-q6r6.onrender.com

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Production requires:

- strong `SECRET_KEY`;
- PostgreSQL `DATABASE_URL`.

---

# 🔐 Security

ShopFlow follows several important security practices.

### Environment secrets

Secrets are loaded from environment variables.

The repository does not include:

- `.env`;
- database credentials;
- Stripe credentials;
- Telegram bot tokens;
- production secret keys.

### Password security

Administrator passwords are stored as password hashes.

Plain-text administrator passwords are not stored in the repository.

### CSRF

State-changing requests use CSRF protection.

### Database errors

Database integrity failures are safely handled and logged without exposing SQL parameters or customer information.

### Stripe

Live Stripe secret keys are rejected in the current demo configuration.

### Git

The following are excluded through `.gitignore`:

```text
.env
.env.*
.venv/
instance/
*.db
*.sqlite
*.sqlite3
__pycache__/
.pytest_cache/
.pytest-tmp/
static/products/uploads/
*.log
```

`.env.example` remains available as a safe configuration template.

---

# ⚙ Environment Variables

Create your local `.env`:

```powershell
Copy-Item .env.example .env
```

Example:

```env
APP_ENV=development

SECRET_KEY=

DATABASE_URL=

BASE_URL=http://127.0.0.1:5000

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

---

# 💻 Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/roman-webdev/ShopFlow.git
cd ShopFlow
```

---

## 2. Create virtual environment

### Windows

```powershell
python -m venv .venv
```

---

## 3. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 4. Create environment file

```powershell
Copy-Item .env.example .env
```

Configure values if required.

---

## 5. Initialize / upgrade demo database

```powershell
.\.venv\Scripts\python.exe -m flask --app app:create_app upgrade-demo
```

This command updates the schema and loads the demo catalog while preserving existing orders.

---

## 6. Create administrator

```powershell
.\.venv\Scripts\python.exe -m flask --app app:create_app create-admin
```

Username requirements:

```text
2–80 characters
```

Password requirements:

```text
minimum 12 characters
```

---

## 7. Start ShopFlow

```powershell
.\start.ps1 -Port 5001
```

Store:

```text
http://127.0.0.1:5001
```

Admin:

```text
http://127.0.0.1:5001/admin
```

---

# 🧪 Testing

Install development dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Run the test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Current test status:

```text
28 passed
```

Tests cover:

- app configuration;
- database isolation;
- product data;
- translations;
- checkout;
- order persistence;
- CSRF refresh behavior;
- Stripe demo handling;
- live Stripe rejection;
- webhook signature handling;
- Telegram failure handling;
- PostgreSQL-compatible checkout behavior;
- database error handling.

Test databases are isolated from the real ShopFlow database.

---

# 📁 Project Structure

```text
ShopFlow/
│
├── app.py
├── seed.py
├── product_translation.py
├── demo_catalog.json
│
├── templates/
│   ├── base.html
│   ├── store.html
│   ├── order.html
│   ├── login.html
│   ├── admin.html
│   └── edit.html
│
├── static/
│   ├── products/
│   │   ├── photos/
│   │   └── colorways/
│   │
│   ├── style.css
│   ├── premium.css
│   ├── interaction.css
│   ├── design.css
│   │
│   ├── store.js
│   ├── motion.js
│   ├── admin-ui.js
│   ├── translations.js
│   ├── i18n.js
│   └── colorways.js
│
├── tests/
│   ├── conftest.py
│   ├── test_smoke.py
│   └── test_translation.py
│
├── docs/
│   ├── PROJECT_STRUCTURE.md
│   └── qa/
│       └── screenshots/
│
├── .env.example
├── .gitignore
│
├── requirements.txt
├── requirements-dev.txt
├── requirements.lock.txt
│
├── pytest.ini
├── start.ps1
└── README.md
```

---

# ✅ Production Verification

The deployed version has been verified with the following flow:

```text
Render
  ↓
Flask / Waitress
  ↓
Neon PostgreSQL
  ↓
Product Catalog
  ↓
Shopping Cart
  ↓
Checkout
  ↓
Order Creation
  ↓
Admin Dashboard
```

Production checkout successfully creates orders in PostgreSQL.

Created orders are immediately visible in the admin dashboard.

Order fulfillment status changes persist after page reload.

---

# 📊 Current Project Status

| Feature | Status |
|---|---|
| Storefront | ✅ |
| Responsive Design | ✅ |
| EN / RU / UA | ✅ |
| 18 Product Catalog | ✅ |
| Product Variants | ✅ |
| Variant Images | ✅ |
| Variant Pricing | ✅ |
| Product Gallery | ✅ |
| Search | ✅ |
| Filters | ✅ |
| Sorting | ✅ |
| Wishlist | ✅ |
| Recently Viewed | ✅ |
| Product Comparison | ✅ |
| Persistent Cart | ✅ |
| Checkout | ✅ |
| PostgreSQL | ✅ |
| Neon Database | ✅ |
| Admin Dashboard | ✅ |
| Product Management | ✅ |
| Image Management | ✅ |
| Order Management | ✅ |
| Order Status History | ✅ |
| Stripe Demo Flow | ✅ |
| Telegram Integration | ✅ Optional |
| Automated Tests | ✅ 28 passed |
| Render Deployment | ✅ |
| Public Live Demo | ✅ |

---

# ⚠ Demo Limitations

ShopFlow is a portfolio and demonstration project.

The current scope intentionally does not include:

- real payment processing;
- production shipping provider integration;
- customer accounts;
- password recovery for customers;
- refunds;
- real email delivery;
- automatic inventory deduction after checkout;
- production CDN/object-storage infrastructure;
- enterprise monitoring;
- automated backups managed by the application.

Product-image uploads require persistent/object storage for a fully production-grade deployment.

---

# 🔮 Possible Future Improvements

Potential production extensions:

- Stripe live payments;
- Nova Poshta / shipping integration;
- customer accounts;
- order history for customers;
- email confirmations;
- discount codes;
- promotions engine;
- inventory reservations;
- Cloudinary / S3 image storage;
- analytics dashboard;
- product reviews from real customers;
- recommendations;
- background jobs;
- production monitoring;
- automated database backups.

---

# 👨‍💻 Author

**Roman Shalashov**

Full-Stack Developer focused on:

- Python
- Flask
- JavaScript
- PostgreSQL
- REST APIs
- Telegram Bots
- API Integrations
- Full-Stack Web Applications

GitHub:

https://github.com/roman-webdev

---

# ShopFlow

**Thoughtful products. Better everyday experiences.**

🌐 **Live:** https://shopflow-q6r6.onrender.com  
💻 **GitHub:** https://github.com/roman-webdev/ShopFlow