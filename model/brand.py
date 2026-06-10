from extensions import db

class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    products = db.relationship("Product", backref="brand", lazy=True)

    def __repr__(self):
        return f"<Brand {self.name}>"