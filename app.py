import os, csv, click
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_migrate import Migrate
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from extensions import db
from routes.pages import pages
load_dotenv()

app = Flask(os.environ.get("APP_NAME"))
app.secret_key = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://"
    f"{os.environ.get('MYSQL_USER')}:"
    f"{os.environ.get('MYSQL_PASSWORD')}@"
    f"{os.environ.get('MYSQL_HOST')}:"
    f"{os.environ.get('MYSQL_PORT')}/"
    f"{os.environ.get('MYSQL_DB')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

from model import *

@app.route("/")
def home():
    return render_template("index.html")

def get_main_category(category_name):
    category_name = category_name.lower()
    
    skincare_keywords = ['serum', 'moisturizer', 'cream', 'face', 'mask', 'cleanser', 'peel', 'exfoliator', 'toner', 'skincare', 'anti-aging', 'acne', 'sunscreen', 'blemish', 'lip balm', 'lip treatment']
    makeup_keywords = ['palette', 'highlighter', 'lipstick', 'primer', 'concealer', 'mascara', 'foundation', 'spray & powder', 'contour', 'eyeshadow', 'lip gloss', 'bronzer', 'eyeliner', 'blush', 'makeup', 'lip liner', 'lip stain', 'bb & cc', 'color correct', 'tinted']
    haircare_keywords = ['hair', 'shampoo', 'conditioner', 'scalp', 'color care', 'curls']
    fragrance_keywords = ['fragrance', 'cologne', 'perfume', 'rollerball', 'candle', 'diffuser', 'scent']
    bodycare_keywords = ['body', 'lotion', 'deodorant', 'bath', 'shower', 'shaving', 'hand', 'foot', 'scrub', 'cellulite', 'tanner', 'aftershave', 'soap']
    
    # Cek berdasarkan keyword
    if any(word in category_name for word in skincare_keywords):
        return "Skincare"
    elif any(word in category_name for word in makeup_keywords):
        return "Makeup"
    elif any(word in category_name for word in haircare_keywords):
        return "Haircare"
    elif any(word in category_name for word in fragrance_keywords):
        return "Fragrance"
    elif any(word in category_name for word in bodycare_keywords):
        return "Body Care"
    else:
        return "Tools & Accessories"

@app.cli.command("seed-db")
@with_appcontext
def seed_db():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'dataset', 'sephora_cleaned_dataset.csv')
    
    if not os.path.exists(csv_file_path):
        print(f"File tidak ditemukan: {csv_file_path}")
        return

    try:
        with open(csv_file_path, mode='r', encoding='utf-8', errors='replace') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            
            print("Memulai proses import data dari CSV..")
            
            count = 0
            for row in csv_reader:
                # Brand
                brand_name = row['brand'].strip()
                brand = Brand.query.filter_by(name=brand_name).first()
                if not brand:
                    brand = Brand(name=brand_name)
                    db.session.add(brand)
                    db.session.flush()

                # Main Category
                cat_name = row['category'].strip()
                main_cat_name = get_main_category(cat_name)
                
                main_category = MainCategory.query.filter_by(name=main_cat_name).first()
                if not main_category:
                    main_category = MainCategory(name=main_cat_name)
                    db.session.add(main_category)
                    db.session.flush()

                # Category
                category = Category.query.filter_by(name=cat_name, main_category_id=main_category.id).first()
                if not category:
                    category = Category(name=cat_name, main_category_id=main_category.id)
                    db.session.add(category)
                    db.session.flush()

                # Insert Product
                dataset_id = int(row['id'])
                product = Product.query.filter_by(dataset_id=dataset_id).first()
                
                if not product:
                    product = Product(
                        dataset_id=dataset_id,
                        name=row['name'].strip(),
                        price=float(row['price'].replace(',', '.')) if row['price'] else 0.0,
                        love=int(row['love']) if row['love'] else 0,
                        rating=float(row['rating'].replace(',', '.')) if row['rating'] else 0.0,
                        number_of_reviews=int(row['number_of_reviews']) if row['number_of_reviews'] else 0,
                        brand_id=brand.id,
                        category_id=category.id
                    )
                    db.session.add(product)
                    db.session.flush()

                    # Product Detail
                    product_detail = ProductDetail(
                        product_id=product.produk_id,
                        detail=row['details'].strip() if row['details'] else "",
                        ingredients=row['ingredients'].strip() if row['ingredients'] else "",
                        how_to_use=row['how_to_use'].strip() if row['how_to_use'] else ""
                    )
                    db.session.add(product_detail)

                    # Product NLP Feature
                    product_nlp = ProductNLPFeature(
                        product_id=product.produk_id,
                        combined_features=row['combined_features'].strip() if row['combined_features'] else "",
                        clean_text=row['clean_text'].strip() if row['clean_text'] else ""
                    )
                    db.session.add(product_nlp)
                    
                count += 1
                if count % 500 == 0:
                    db.session.commit()
                    print(f"Berhasil memproses {count} baris...")
            
            db.session.commit()
            print(f"Selesai! {count} produk berhasil diimport ke database!")
            
    except Exception as e:
        db.session.rollback()
        print(f"Terjadi kesalahan saat seeding: {e}")
app.register_blueprint(pages)

if __name__ == "__main__":
    app.run(debug=True)