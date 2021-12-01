from db import db


def data_preparate_for_commit(args):
    db.session.add(args)
    db.session.flush()
