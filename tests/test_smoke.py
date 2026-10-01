import re
import uuid
from unittest.mock import patch
import pytest
from werkzeug.security import generate_password_hash
from app import create_app, db, Order, Product, AdminUser
from seed import seed_products

@pytest.fixture
def app(tmp_path):
    app = create_app({'TESTING': True, 'SECRET_KEY': 'test-only-secret', 'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + str(tmp_path / 'test.db'),
        'STRIPE_SECRET_KEY': '', 'STRIPE_WEBHOOK_SECRET': '', 'TELEGRAM_BOT_TOKEN': '', 'TELEGRAM_CHAT_ID': ''})
    with app.app_context():
        db.create_all()
        seed_products()
        db.session.add(AdminUser(username='roman', password_hash=generate_password_hash('Testing-only-password')))
        db.session.commit()
    yield app

def checkout_data():
    return {'customer': {'name': 'Demo Buyer', 'email': 'demo@example.com', 'phone': '+380501234567', 'city': 'Kyiv', 'address': 'Example Street 10'},
            'items': [{'id': 1, 'quantity': 2, 'variant': 'Graphite'}], 'request_key': str(uuid.uuid4())}

def token(client):
    return client.get('/api/config').json['csrf_token']

def form_token(client, url):
    return re.search(r'name="csrf_token" value="([^"]+)"', client.get(url).text).group(1)

def test_catalog_checkout_persistence_and_retry(app):
    client = app.test_client()
    assert client.get('/').status_code == 200
    assert len(client.get('/api/products').json) == 18
    assert client.get('/api/products/1').json['price_cents'] == 12900
    assert client.get('/api/config').json['payment_mode'] == 'mock'
    data = checkout_data()
    data['total_cents'] = 1  # server must ignore forged prices
    headers = {'X-CSRFToken': token(client)}
    result = client.post('/api/checkout', json=data, headers=headers)
    assert result.status_code == 201
    assert result.json['status'] == 'demo_paid'
    assert client.get(result.json['url']).status_code == 200
    assert client.post('/api/checkout', json=data, headers=headers).status_code == 200
    with app.app_context():
        order = db.session.get(Order, result.json['order_id'])
        assert order.total_cents == 25800
        assert len(order.items) == 1
        assert order.items[0].quantity == 2
        assert db.session.query(Order).count() == 1
    outsider = app.test_client()
    assert outsider.post('/api/checkout', json=data, headers={'X-CSRFToken': token(outsider)}).status_code == 409

def test_validation_and_csrf(app):
    client = app.test_client()
    assert client.post('/api/checkout', json=checkout_data()).status_code == 400
    headers = {'X-CSRFToken': token(client)}
    for changes, expected in [({'items': []},400), ({'items':[{'id':8,'quantity':1}]},409), ({'items':[{'id':1,'quantity':True}]},400), ({'customer':{}},400)]:
        data = checkout_data(); data.update(changes)
        assert client.post('/api/checkout', json=data, headers=headers).status_code == expected
    assert client.post('/api/stripe/webhook').status_code == 503

def test_admin_crud_and_order_details(app):
    client = app.test_client()
    assert client.get('/admin').status_code == 302
    assert client.post('/admin/login', data={'username':'roman','password':'wrong','csrf_token':form_token(client,'/admin/login')}).status_code == 200
    response = client.post('/admin/login', data={'username':'roman','password':'Testing-only-password','csrf_token':form_token(client,'/admin/login')})
    assert response.status_code == 302
    assert client.get('/admin').status_code == 200
    data = {'name':'New demo item','description':'A useful demo product.', 'category':'Home','price':'12.34','image':'/static/favicon.svg','active':'on','available':'on','csrf_token':form_token(client,'/admin/product/new')}
    assert client.post('/admin/product/new', data=data).status_code == 302
    with app.app_context():
        p = db.session.scalar(db.select(Product).where(Product.name == 'New demo item')); product_id = p.id
        assert p.price_cents == 1234
    data.pop('active'); data['csrf_token'] = form_token(client,f'/admin/product/{product_id}')
    assert client.post(f'/admin/product/{product_id}', data=data).status_code == 302
    assert client.get(f'/api/products/{product_id}').status_code == 404
    order = client.post('/api/checkout', json=checkout_data(), headers={'X-CSRFToken':token(client)})
    assert client.get(f"/admin/order/{order.json['order_id']}").status_code == 200
    assert client.post('/admin/logout', data={'csrf_token':form_token(client,'/admin')}).status_code == 302
    assert client.get('/admin').status_code == 302

def test_live_stripe_key_rejected():
    with pytest.raises(RuntimeError, match='Only Stripe'):
        create_app({'STRIPE_SECRET_KEY':'sk_live_forbidden'})

def test_telegram_failure_does_not_lose_order(app):
    import requests
    app.config.update(TELEGRAM_BOT_TOKEN='test-placeholder', TELEGRAM_CHAT_ID='test-chat')
    client = app.test_client()
    with patch('app.requests.post', side_effect=requests.ConnectionError):
        assert client.post('/api/checkout', json=checkout_data(), headers={'X-CSRFToken':token(client)}).status_code == 201
    with app.app_context():
        assert db.session.query(Order).count() == 1

def test_stripe_test_checkout_and_signed_webhook(tmp_path):
    import hashlib
    import hmac
    import json
    import time
    from types import SimpleNamespace
    app = create_app({'TESTING':True,'SECRET_KEY':'test-only-secret','SQLALCHEMY_DATABASE_URI':'sqlite:///' + str(tmp_path/'stripe.db'),
        'STRIPE_SECRET_KEY':'sk_test_placeholder','STRIPE_WEBHOOK_SECRET':'whsec_test_placeholder',
        'TELEGRAM_BOT_TOKEN':'','TELEGRAM_CHAT_ID':''})
    with app.app_context():
        db.create_all(); seed_products()
    client = app.test_client()
    with patch('app.stripe.checkout.Session.create',return_value=SimpleNamespace(id='cs_test_demo',url='https://checkout.stripe.com/test')) as mocked:
        result = client.post('/api/checkout',json=checkout_data(),headers={'X-CSRFToken':token(client)})
        assert result.status_code == 201
        assert result.json['status'] == 'pending'
        assert mocked.call_args.kwargs['line_items'][0]['price_data']['unit_amount'] == 12900
    assert client.post('/api/stripe/webhook',data='{}').status_code == 400
    def send_event(live=False, amount=25800):
        payload = json.dumps({'id':'evt_test','type':'checkout.session.completed','livemode':live,
            'data':{'object':{'id':'cs_test_demo','payment_status':'paid','amount_total':amount,'currency':'usd'}}})
        timestamp=str(int(time.time()))
        signature=hmac.new(b'whsec_test_placeholder',f'{timestamp}.{payload}'.encode(),hashlib.sha256).hexdigest()
        return client.post('/api/stripe/webhook',data=payload,headers={'Stripe-Signature':f't={timestamp},v1={signature}','Content-Type':'application/json'})
    assert send_event(live=True).status_code == 400
    assert send_event(amount=1).status_code == 200
    with app.app_context():
        assert db.session.get(Order,result.json['order_id']).status == 'pending'
    assert send_event().status_code == 200
    assert send_event().status_code == 200
    with app.app_context():
        assert db.session.get(Order,result.json['order_id']).status == 'paid_test'


def test_variants_snapshot_and_aggregate_stock(app):
    client = app.test_client()
    headers = {'X-CSRFToken': token(client)}
    data = checkout_data()
    data['items'] = [{'id': 1, 'quantity': 2, 'variant': 'Graphite'}, {'id': 1, 'quantity': 3, 'variant': 'Sand'}]
    result = client.post('/api/checkout', json=data, headers=headers)
    assert result.status_code == 201
    with app.app_context():
        order = db.session.get(Order, result.json['order_id'])
        assert order.total_cents == 64500
        assert {i.variant for i in order.items} == {'Graphite', 'Sand'}
    data['request_key'] = str(uuid.uuid4())
    data['items'][0]['variant'] = 'forged'
    assert client.post('/api/checkout', json=data, headers=headers).status_code == 400
    data['items'] = [{'id': 1, 'quantity': 20, 'variant': 'Graphite'}, {'id': 1, 'quantity': 20, 'variant': 'Sand'}]
    assert client.post('/api/checkout', json=data, headers=headers).status_code == 409
    data['items'] = [{'id': 1, 'quantity': 1, 'variant': 'Sand'}] * 2
    assert client.post('/api/checkout', json=data, headers=headers).status_code == 400

def test_product_metadata_and_fulfillment(app):
    client = app.test_client()
    result = client.post('/api/checkout', json=checkout_data(), headers={'X-CSRFToken':token(client)})
    order_id = result.json['order_id']
    assert client.post(f'/admin/order/{order_id}/status', data={'status':'shipped', 'csrf_token':token(client)}).status_code == 302
    client.post('/admin/login',data={'username':'roman','password':'Testing-only-password','csrf_token':form_token(client,'/admin/login')})
    url = f'/admin/order/{order_id}/status'
    csrf_value = form_token(client,f'/admin/order/{order_id}')
    assert client.post(url,data={'status':'paid_test','csrf_token':csrf_value}).status_code == 400
    assert client.post(url,data={'status':'processing','csrf_token':csrf_value}).status_code == 302
    with app.app_context():
        order = db.session.get(Order,order_id)
        assert order.status == 'demo_paid'
        assert order.fulfillment_status == 'processing'
    product = client.get('/api/products/1').json
    assert set(product['translations']) == {'en','ru','uk'}
    assert product['image'].startswith('/static/')
    data = {'name':'Localized product', 'description':'Editable product description','category':'Home','price':'20.00','stock':'4','variants':'Small, Large','sku':'QA-01','badge':'Sale','image':'/static/products/4.svg','translations':'{"ru":{"name":"Товар"},"uk":{"name":"Товар"}}','active':'on','available':'on','csrf_token':form_token(client,'/admin/product/new')}
    assert client.post('/admin/product/new',data=data).status_code == 302
    products = client.get('/api/products').json
    product = next(p for p in products if p['sku']=='QA-01')
    assert product['stock']==4 and product['variants']==['Small','Large']
    data['stock']='-1';data['csrf_token']=form_token(client,f"/admin/product/{product['id']}")
    assert client.post(f"/admin/product/{product['id']}",data=data).status_code == 200
    assert client.get(f"/api/products/{product['id']}").json['stock']==4

def test_telegram_payload_and_demo_upgrade(app):
    from types import SimpleNamespace
    app.config.update(TELEGRAM_BOT_TOKEN='test-placeholder',TELEGRAM_CHAT_ID='test-placeholder')
    client=app.test_client()
    with patch('app.requests.post',return_value=SimpleNamespace(raise_for_status=lambda:None)) as mocked:
        assert client.post('/api/checkout',json=checkout_data(),headers={'X-CSRFToken':token(client)}).status_code==201
        text=mocked.call_args.kwargs['json']['text']
        for value in ['Demo Buyer','demo@example.com','Kyiv','Graphite','× 2','$258.00']:
            assert value in text
    runner=app.test_cli_runner()
    assert runner.invoke(args=['upgrade-demo']).exit_code==0
    assert runner.invoke(args=['upgrade-demo']).exit_code==0
    with app.app_context():
        assert db.session.query(Order).count()==1
        assert db.session.query(Product).count()==18


def test_partial_stripe_configuration_falls_back_to_demo():
    app = create_app({'TESTING':True,'STRIPE_SECRET_KEY':'sk_test_placeholder','STRIPE_WEBHOOK_SECRET':''})
    assert app.test_client().get('/api/config').json['payment_mode']=='mock'

def test_order_localized_snapshot_is_preserved(app):
    client=app.test_client()
    result=client.post('/api/checkout',json=checkout_data(),headers={'X-CSRFToken':token(client)})
    with app.app_context():
        product=db.session.get(Product,1)
        product.translations={'ru':{'name':'Updated name'}}
        db.session.commit()
        order=db.session.get(Order,result.json['order_id'])
        assert order.items[0].translations['ru']['name']=='Студийные наушники'


def test_sneaker_color_and_size_checkout_snapshot(app):
    client = app.test_client()
    data = checkout_data()
    data['items'] = [{'id': 7, 'quantity': 1, 'variant': 'Black / EU 40'},
                     {'id': 7, 'quantity': 1, 'variant': 'Blue / EU 42'}]
    headers = {'X-CSRFToken': token(client)}
    result = client.post('/api/checkout', json=data, headers=headers)
    assert result.status_code == 201
    with app.app_context():
        order = db.session.get(Order, result.json['order_id'])
        assert {i.variant for i in order.items} == {'Black / EU 40', 'Blue / EU 42'}
        assert order.total_cents == 19000
    data['request_key'] = str(uuid.uuid4())
    data['items'][0]['variant'] = 'Black / EU 99'
    assert client.post('/api/checkout', json=data, headers=headers).status_code == 400


def test_specifications_editor_roundtrip_and_length_limit(app):
    client = app.test_client()
    client.post('/admin/login', data={'username':'roman','password':'Testing-only-password','csrf_token':form_token(client,'/admin/login')})
    with app.app_context():
        product = db.session.get(Product,1)
        payload = {'simple_editor':'1','name':product.name,'description':product.description,'category':product.category,'image':product.image,'price':'129.00','stock':'30','sku':product.sku,'badge':product.badge,'active':'on','available':'on','variant_choices':product.variants,'spec_material':'Fabric','spec_dimensions':'20 cm','spec_features':'30 hours','gallery':'/static/products/photos/1.webp\n/static/products/photos/colorways/1-sand.webp'}
    payload['csrf_token'] = form_token(client,'/admin/product/1')
    with patch('product_translation.translate_product', return_value={}):
        assert client.post('/admin/product/1',data=payload).status_code == 302
    assert client.get('/api/products/1').json['specifications'] == {'material':'Fabric','dimensions':'20 cm','features':'30 hours'}
    assert client.get('/api/products/1').json['gallery'] == ['/static/products/photos/1.webp','/static/products/photos/colorways/1-sand.webp']
    payload['spec_material'] = 'x'*501
    payload['csrf_token'] = form_token(client,'/admin/product/1')
    assert client.post('/admin/product/1',data=payload).status_code == 200
    assert client.get('/api/products/1').json['specifications']['material'] == 'Fabric'


def test_gallery_rejects_external_urls(app):
    client = app.test_client()
    client.post('/admin/login', data={'username':'roman','password':'Testing-only-password','csrf_token':form_token(client,'/admin/login')})
    with app.app_context():
        p = db.session.get(Product,1)
        payload = {'simple_editor':'1','name':p.name,'description':p.description,'category':p.category,'image':p.image,'price':'129.00','stock':'30','sku':p.sku,'badge':p.badge,'active':'on','available':'on','variant_choices':p.variants,'gallery':'https://example.com/photo.jpg'}
    payload['csrf_token'] = form_token(client,'/admin/product/1')
    assert client.post('/admin/product/1',data=payload).status_code == 200
    assert client.get('/api/products/1').json['gallery'] == []


def test_photo_upload_requires_login_and_csrf(app, tmp_path):
    from io import BytesIO
    app.config['PRODUCT_UPLOAD_FOLDER'] = str(tmp_path / 'uploads')
    client = app.test_client()
    assert client.post('/admin/photos', data={'photo': (BytesIO(b'bad'), 'photo.png')}).status_code == 400
    assert client.post('/admin/photos', data={'photo': (BytesIO(b'bad'), 'photo.png')}, headers={'X-CSRFToken':token(client)}).status_code == 302
    assert not (tmp_path / 'uploads').exists()


def test_photo_upload_decodes_reencodes_and_ignores_filename(app, tmp_path):
    from io import BytesIO
    from PIL import Image, PngImagePlugin
    app.config['PRODUCT_UPLOAD_FOLDER'] = str(tmp_path / 'uploads')
    client = app.test_client()
    client.post('/admin/login', data={'username':'roman','password':'Testing-only-password','csrf_token':form_token(client,'/admin/login')})
    data = BytesIO()
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text('Private note', 'remove this')
    Image.new('RGBA', (3200,1600), (120,180,150,128)).save(data, 'PNG', pnginfo=metadata)
    data.seek(0)
    response = client.post('/admin/photos', data={'photo':(data,'../../payload.html')},headers={'X-CSRFToken':token(client)})
    assert response.status_code == 201
    assert re.fullmatch(r'/static/products/uploads/[a-f0-9]{32}\.webp', response.json['url'])
    with Image.open(tmp_path / 'uploads' / response.json['url'].rsplit('/',1)[1]) as image:
        assert image.format == 'WEBP'
        assert image.size == (2400,1200)
        assert 'Private note' not in image.info
        assert 'A' in image.getbands()


@pytest.mark.parametrize('data,name,status', [(b'<svg></svg>','photo.svg',400), (b'not a photo','photo.jpg',400), (b'x'*(8*1024*1024+1),'photo.png',413)], ids=['svg','corrupt','too-large'])
def test_photo_upload_rejects_invalid_or_large_files(app, tmp_path, data, name, status):
    from io import BytesIO
    app.config['PRODUCT_UPLOAD_FOLDER'] = str(tmp_path / 'uploads')
    client = app.test_client()
    client.post('/admin/login', data={'username':'roman','password':'Testing-only-password','csrf_token':form_token(client,'/admin/login')})
    response=client.post('/admin/photos',data={'photo':(BytesIO(data),name)},headers={'X-CSRFToken':token(client)})
    assert response.status_code == status
    assert response.json['error']
    assert not (tmp_path / 'uploads').exists()


def test_dashboard_excludes_cancelled_revenue_and_counts_processing(app):
    with app.app_context():
        for payment, progress, cents in [('demo_paid', 'cancelled', 18800), ('demo_paid', 'shipped', 12900), ('paid_test', 'processing', 5000), ('pending', 'unfulfilled', 3000)]:
            db.session.add(Order(request_key=str(uuid.uuid4()), name='Test', email='test@example.com', phone='123', city='Test', address='Test', total_cents=cents, status=payment, fulfillment_status=progress))
        db.session.commit()
    client = app.test_client()
    with client.session_transaction() as session:
        session['admin_id'] = 1
    response = client.get('/admin')
    assert response.status_code == 200
    stats = re.search(r'<div class="stats">(.*?)</div>', response.text).group(1)
    assert '<strong>$179.00</strong>' in stats
    assert '<small>To fulfill</small><strong>2</strong>' in stats


def test_camera_variant_prices_are_authoritative_and_snapshotted(app):
    client = app.test_client()
    camera = next(p for p in client.get('/api/products').json if p['sku'] == 'SF-008')
    assert camera['variant_details']['Body']['price_cents'] == 19900
    assert camera['variant_details']['Kit']['price_cents'] == 24900
    with app.app_context():
        product = db.session.get(Product,camera['id'])
        product.available = True
        product.stock = 10
        db.session.commit()
    payload = checkout_data()
    payload['items'] = [{'id':camera['id'],'variant':'Body','quantity':1,'price_cents':1}, {'id':camera['id'],'variant':'Kit','quantity':1,'price_cents':1}]
    result = client.post('/api/checkout',json=payload,headers={'X-CSRFToken':token(client)})
    assert result.status_code == 201
    with app.app_context():
        order = db.session.get(Order,result.json['order_id'])
        assert order.total_cents == 44800
        assert {i.variant:i.price_cents for i in order.items} == {'Body':19900,'Kit':24900}
        product = db.session.get(Product,camera['id'])
        product.variant_details = {'Body':{'price_cents':21000}}
        db.session.commit()
        assert order.total_cents == 44800
    client.post('/admin/login',data={'username':'roman','password':'Testing-only-password','csrf_token':form_token(client,'/admin/login')})
    assert client.get('/admin/product/'+str(camera['id'])).status_code == 200


def test_order_history_tracks_changes_without_duplicates(app):
    client = app.test_client()
    result = client.post('/api/checkout',json=checkout_data(),headers={'X-CSRFToken':token(client)})
    order_id = result.json['order_id']
    client.post('/admin/login',data={'username':'roman','password':'Testing-only-password','csrf_token':form_token(client,'/admin/login')})
    csrf_value = form_token(client,f'/admin/order/{order_id}')
    for status in ['processing','processing','shipped']:
        assert client.post(f'/admin/order/{order_id}/status',data={'status':status,'csrf_token':csrf_value}).status_code == 302
    with app.app_context():
        order = db.session.get(Order,order_id)
        assert [(c.previous_status,c.new_status) for c in order.status_changes] == [('processing','shipped'),('unfulfilled','processing')]
        assert all(c.changed_at for c in order.status_changes)
    assert 'Status history' in client.get(f'/admin/order/{order_id}').text

def test_checkout_expired_csrf_refresh(app):
    import time
    client = app.test_client()
    with patch('itsdangerous.timed.time.time', return_value=time.time() - 7200):
        expired = token(client)
    with patch.object(app.logger, 'warning') as logged:
        result = client.post('/api/checkout', json=checkout_data(), headers={'X-CSRFToken': expired})
    assert result.status_code == 400
    assert result.json['error'] == 'Checkout session expired. Please try again.'
    assert logged.called
    assert client.post('/api/checkout', json=checkout_data(), headers={'X-CSRFToken': token(client)}).status_code == 201


def test_checkout_constraint_failure_is_not_retry_conflict(app, caplog):
    from sqlalchemy.exc import IntegrityError
    client = app.test_client()
    headers = {'X-CSRFToken': token(client)}
    sensitive = 'buyer@example.invalid SECRET_DATABASE_PASSWORD'
    with patch.object(db.session, 'commit', side_effect=IntegrityError('INSERT', {'email': sensitive}, Exception(sensitive))):
        result = client.post('/api/checkout', json=checkout_data(), headers=headers)
    assert result.status_code == 500
    assert 'Checkout database failure' in caplog.text
    assert sensitive not in caplog.text
    assert 'demo@example.com' not in caplog.text
    with app.app_context():
        assert db.session.query(Order).count() == 0


def test_checkout_database_read_failure_is_logged_safely(app, caplog):
    from sqlalchemy.exc import OperationalError
    client = app.test_client()
    headers = {'X-CSRFToken': token(client)}
    with patch.object(db.session, 'scalar', side_effect=OperationalError('SELECT', {}, Exception('secret'))):
        result = client.post('/api/checkout', json=checkout_data(), headers=headers)
    assert result.status_code == 500
    assert 'OperationalError' in caplog.text
    assert 'secret' not in caplog.text
