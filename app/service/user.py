import base64
import hashlib
import hmac

from app.dao.models.user import User
from app.helper.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService():
    def __init__(self, dao):
        self.dao = dao

    def get_one(self, u_id):
        return self.dao.get_one(u_id)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def do_post(self, data):
        data.pop('id', None)  # удалить id, если он будет передан
        # хеширование пароля перед записью в БД:
        data['password'] = self.make_user_password_hash(data.get('password'))
        new_item = User(**data)
        return self.dao.do_post(new_item)

    def do_put(self, u_id, data):
        item = self.get_one(u_id)

        item.username = data.get('username')
        item.password = data.get('password')
        item.role = data.get('role')

        return self.dao.do_post(item)

    def do_patch(self, u_id, data):
        data.pop('id', None)  # удалить id, если он будет передан
        return self.dao.do_update(u_id, data)

    def delete_one(self, u_id):
        return self.dao.do_delete(u_id)

    def make_user_password_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
        return base64.b64encode(hash_digest)

    def compare_password(self, hash_password_from_db, client_input_password):
        decoded_digest_db = base64.b64decode(hash_password_from_db)  # в байт-код
        hash_digest_client = self.make_user_password_hash(client_input_password)
        decoded_digest_client = base64.b64decode(hash_digest_client)
        return hmac.compare_digest(decoded_digest_db, decoded_digest_client)
