from . import db


class ProductNLPFeature(db.Model):
    __tablename__ = "product_nlp_features"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("produk.produk_id"),nullable=False)
    combined_features = db.Column(db.Text)
    clean_text = db.Column(db.Text)

    def __repr__(self):
        return f"<ProductNLPFeature {self.id}>"