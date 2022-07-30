from app.dao.models.director import Director


class DirectorService():
    def __init__(self,dao):
        self.dao=dao

    def get_one(self, d_id):
        return self.dao.get_one(d_id)

    def get_all(self):
        return self.dao.get_all()

    def do_post(self, data):
        data.pop('id', None)  # удалить id, если он будет передан
        new_item = Director(**data)
        return self.dao.do_post(new_item)

    def do_put(self, d_id, data):
        item = self.get_one(d_id)

        item.name = data.get('name')

        return self.dao.do_post(item)

    def do_patch(self, d_id, data):
        data.pop('id', None)  # удалить id, если он будет передан
        return self.dao.do_update(d_id, data)

    def delete_one(self, d_id):
        return self.dao.do_delete(d_id)

