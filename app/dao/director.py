from app.dao.models.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, d_id):
        item = self.session.query(Director).get(d_id)
        return item

    def get_all(self):
        all_items = self.session.query(Director).all()
        return all_items

    def do_post(self, item):
        try:
            self.session.add(item)
            self.session.commit()
            self.session.close()
            return ""
        except:
            return None

    def do_update(self, d_id, data):
        try:
            self.session.query(Director).filter(Director.id == d_id).update(data)
            self.session.commit()
            self.session.close()
            return ""
        except:
            return None

    def do_delete(self, d_id):
        try:
            item = self.get_one(d_id)
            self.session.delete(item)
            self.session.commit()
            self.session.close()
            return ""
        except:
            return None
