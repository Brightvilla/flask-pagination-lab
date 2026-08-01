from flask import Flask, jsonify, request
from models import db, Book


def create_app(config_name="development"):
    app = Flask(__name__)

    # Basic configuration: use in‑memory DB for tests, file DB otherwise
    if config_name == "test":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    @app.route("/books", methods=["GET"])
    def get_books():
        """
        Return paginated list of books.

        Query parameters:
          - page (default 1)
          - per_page (default 5)
        """
        # Get query params with safe fallbacks
        try:
            page = int(request.args.get("page", 1))
        except (TypeError, ValueError):
            page = 1

        try:
            per_page = int(request.args.get("per_page", 5))
        except (TypeError, ValueError):
            per_page = 5

        pagination = Book.query.order_by(Book.id).paginate(
            page=page,
            per_page=per_page,
            error_out=False,  # don't raise 404 if page is out of range
        )

        items = [book.to_dict() for book in pagination.items]

        response = {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": items,
        }

        return jsonify(response), 200

    return app


# Allow running the server directly: `python app.py`
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)