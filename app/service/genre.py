from app.dao.models.genre import Genre


class GenreService():
    def __init__(self,dao):
        self.dao=dao

    def get_one(self, g_id):
        return self.dao.get_one(g_id)

    def get_all(self):
        return self.dao.get_all()

    def do_post(self, data):
        data.pop('id', None)  # удалить id, если он будет передан
        new_item = Genre(**data)
        return self.dao.do_post(new_item)

    def do_put(self, g_id, data):
        item = self.get_one(g_id)

        item.name = data.get('name')

        return self.dao.do_post(item)

    def do_patch(self, g_id, data):
        data.pop('id', None)  # удалить id, если он будет передан
        return self.dao.do_update(g_id, data)

    def delete_one(self, g_id):
        return self.dao.do_delete(g_id)

