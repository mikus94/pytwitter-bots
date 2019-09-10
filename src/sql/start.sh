# Creating database
psql -U postgres -c "CREATE DATABASE twitter;"

psql -U postgres -d twitter -f queries/create_db.sql