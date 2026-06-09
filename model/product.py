from . import db

class Product(db.Model):
    __tablename__ = "produk"

    produk_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    dataset_id = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float)
    love = db.Column(db.Integer)
    rating = db.Column(db.Float)
    number_of_reviews = db.Column(db.Integer)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"),nullable=False)
    details = db.relationship("ProductDetail", backref="product", uselist=False, cascade="all, delete-orphan")
    nlp_features = db.relationship("ProductNLPFeature", backref="product", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product {self.name}>"