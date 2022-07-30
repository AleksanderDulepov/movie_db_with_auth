from app.dao.models.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, g_id):
        item = self.session.query(Genre).get(g_id)
        return item

    def get_all(self):
        all_items = self.session.query(Genre).all()
        return all_items

    def do_post(self, item):
        try:
            self.session.add(item)
            self.session.commit()
            self.session.close()
            return ""
        except:
            return None

    def do_update(self, g_id, data):
        try:
            self.session.query(Genre).filter(Genre.id == g_id).update(data)
            self.session.commit()
            self.session.close()
            return ""
        except:
            return None

    def do_delete(self, g_id):
        try:
            item = self.get_one(g_id)
            self.session.delete(item)
            self.session.commit()
            self.session.close()
            return ""
        except:
            return None
