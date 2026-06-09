from . import db

class ProductDetail(db.Model):
    __tablename__ = "product_details"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("produk.produk_id"), nullable=False)
    detail = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    how_to_use = db.Column(db.Text)

    def __repr__(self):
        return f"<ProductDetail {self.id}>"