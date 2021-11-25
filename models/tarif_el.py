from db import db


class TarifPiceModel(db.Model):
    """
    Model save price for stay in park

    """

    __tablename__ = "tarif_el"

    id = db.Column(db.Integer, primary_key=True)
    tarif_id = db.Column(db.ForeignKey("tariftype.id"), nullable=False)
    stay = db.Column(db.String(5), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
