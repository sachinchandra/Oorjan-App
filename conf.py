production = True

if production:
    db_name = 'oorjan'
    db_port = 5432
    db_host = "localhost"
    db_user = 'oorjan'
    db_password = 'oorjan'
    db_url = "postgresql://{user}:{password}@{host}/{dbname}".format(user=db_user, password=db_password,
                                                                     host=db_host, dbname=db_name)
    api_host = "localhost"
    api_port = 80
else:
    db_name = 'example'
    db_port = 5432
    db_host = "localhost"
    db_user = None
    db_password = None
    db_url = "postgresql://{host}/{db}".format(host=db_host, db=db_name)

    api_host = "localhost"
    api_port = 5000
