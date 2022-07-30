from app.dao.models.user import User

class UserDAO:
    def __init__(self,session):
        self.session=session

    def get_one(self, u_id):
        item = self.session.query(User).get(u_id)
        return item

    def get_all(self):
        all_items = self.session.query(User)
        return all_items

    def get_by_username(self, username):
        item = self.session.query(User).filter(User.username == username).first()
        return item

    def do_post(self, item):
        try:
            self.session.add(item)
            self.session.commit()
            self.session.close()
            return ""
        except:
            return None

    def do_update(self, u_id, data):
        try:
            self.session.query(User).filter(User.id == u_id).update(data)
            self.session.commit()
            self.session.close()
            return ""
        except:
            return None

    def do_delete(self, u_id):
        try:
            item = self.get_one(u_id)
            self.session.delete(item)
            self.session.commit()
            self.session.close()
            return ""
        except:
            return None
