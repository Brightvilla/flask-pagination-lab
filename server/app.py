#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        pagination = Book.query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
            'items': [BookSchema().dump(b) for b in pagination.items]
        }, 200


api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)