##########These would be used with migrations###########
# from migrate.versioning import api
# from config import SQLALCHEMY_DATABASE_URI
# from config import SQLAlCHEMY_MIGRATE_REPO
# import os.path
from rdio_collabo import db

db.create_all()
###########This logic is used for migrations############
# if not os.path.exists(SQLAlCHEMY_MIGRATE_REPO):
#     api.create(SQLAlCHEMY_MIGRATE_REPO, 'database repository')
#     api.version_control(SQLALCHEMY_DATABASE_URI, SQLAlCHEMY_MIGRATE_REPO)
# else:
#     api.version_control(SQLALCHEMY_DATABASE_URI, SQLAlCHEMY_MIGRATE_REPO, api.version(SQLAlCHEMY_MIGRATE_REPO))
