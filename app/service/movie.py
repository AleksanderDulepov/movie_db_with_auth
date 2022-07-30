from app.dao.models.movie import Movie


class MovieService:
    def __init__(self, dao):
        self.dao = dao

    def get_one(self, d_id):
        return self.dao.get_one(d_id)

    def get_with_filter(self, data):
        # parameters удалить пустые позиции
        for key, value in data.items():
            if not value:
                del data[key]
        return self.dao.get_with_filter(data)

    def do_post(self, data):
        data.pop('id',None) #удалить id, если он будет передан
        new_item = Movie(**data)
        return self.dao.do_post(new_item)

    def do_put(self, d_id, data):
        item = self.get_one(d_id)

        item.title = data.get('title')
        item.description = data.get('description')
        item.trailer = data.get('trailer')
        item.year = data.get('year')
        item.rating = data.get('rating')
        item.genre_id = data.get('genre_id')
        item.director_id = data.get('director_id')
        return self.dao.do_post(item)

    def do_patch(self, d_id, data):
        data.pop('id',None) #удалить id, если он будет передан
        return self.dao.do_update(d_id, data)

    def delete_one(self, d_id):
        return self.dao.do_delete(d_id)

