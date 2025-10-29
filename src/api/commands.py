import click

from api.models import User, db

"""Small helpers to register Flask CLI commands.

Use @app.cli.command to add commands that run with the Flask CLI. Examples:
- flask insert-test-users 5  # create 5 test users
"""


def setup_commands(app):
    """Register example CLI commands used for local development.

    The example below shows how to register `insert-test-users` which accepts a
    numeric count and creates that many test users in the database.
    """

    @app.cli.command("insert-test-users")  # name of our command
    @click.argument("count")  # argument of out command
    def insert_test_users(count):
        print("Creating test users")
        for x in range(1, int(count) + 1):
            user = User()
            user.email = "test_user" + str(x) + "@test.com"
            user.password = "123456"
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print("User: ", user.email, " created.")

        print("All test users created")

    @app.cli.command("insert-test-data")
    def insert_test_data():
        users = [
            ("cli_user1@test.com", "pw1"),
            ("cli_user2@test.com", "pw2"),
            ("cli_user3@test.com", "pw3"),
        ]
        for email, pw in users:
            if not User.query.filter_by(email=email).first():
                u = User()
                u.email = email
                u.password = pw
                u.is_active = True
                db.session.add(u)
                db.session.commit()
                print("Created:", email)
        print("insert_test_data complete")
