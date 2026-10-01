import json
from pathlib import Path
from app import db, Product

def seed_products():
    catalog = json.loads((Path(__file__).parent / 'demo_catalog.json').read_text(encoding='utf-8'))
    for data in catalog:
        product = db.session.scalar(db.select(Product).where(Product.name == data['name']))
        if product is None:
            db.session.add(Product(**data))
        elif not product.sku:
            # Upgrade known original demo records once; preserve later admin edits.
            for key, value in data.items():
                setattr(product, key, value)
    db.session.commit()
