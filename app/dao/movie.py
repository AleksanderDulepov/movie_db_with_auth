from app.dao.models.movie import Movie


class MovieDAO:

    def __init__(self, session):
        self.session = session

    def get_one(self, d_id):
        item = self.session.query(Movie).get(d_id)
        return item

    def get_all(self):
        # all_items = self.session.query(Movie).all()#list
        all_items = self.session.query(Movie)  # flask_sqlalchemy
        # all_items = Movie.query# flask_sqlalchemy
        # all_items = Movie.query.all()#list
        return all_items

    def get_with_filter(self, parameters):
        all_items = self.get_all()
        for key, value in parameters.items():
            all_items = all_items.filter(getattr(Movie, key) == value)
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
            self.session.query(Movie).filter(Movie.id == d_id).update(data)
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
