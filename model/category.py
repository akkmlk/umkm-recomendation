from . import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    main_category_id = db.Column(db.Integer, db.ForeignKey("main_categories.id"), nullable=False)
    products = db.relationship("Product", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"