from . import db


class MainCategory(db.Model):
    __tablename__ = "main_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    categories = db.relationship("Category", backref="main_category", lazy=True)

    def __repr__(self):
        return f"<MainCategory {self.name}>"