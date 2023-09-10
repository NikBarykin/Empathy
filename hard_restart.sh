redis-cli flushall && dropdb database.db && createdb --template=template0 --locale=en_US.UTF-8 --encoding=UTF8 database.db && python3.10 generate/__main__.py && python3.10 bot/__main__.py
