from flask_app import db
from flask_app.models import    User,                           \
                                Post

print(" [!!!] WARNING!!! THIS WILL DROP ALL TABLES AND START OVER [!!!] ")
print("Are you sure you want to continue? [Y/N]")
answer = input()
if answer.lower() == "y":

    print("ABSOLUTELY sure??????? [Y/N]")
    answer = input()
    if answer.lower() == "y":

        print(" ... it's your funeral.")

        db.drop_all()
        db.create_all()

        add_user = User(username="dj.isla", email="dj@email.com", image_file="default.jpg",
                        password="$2b$12$FsSkNop.yhMQD98klCqaqe/DOOvPaA4CtY4Ykd5SmChuG4O3u0X/O")
        db.session.add(add_user)

        add_user = User(username="anonymous", email="anonymous@email.com", image_file="default.jpg",
                        password="$2b$12$RWhMwlA0WA4.EqnVh/VGCufC859rHMJnVmp5DjMnyPVA/3OujT9bS")
        db.session.add(add_user)

        db.session.commit()

    else:
        print("Aborting operation")
        pass


else:
    print("Aborting operation")
    pass

