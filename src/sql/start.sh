# Creating database
psql -U postgres -c "CREATE DATABASE twitter;"

psql -U postgres -d twitter -f create_db.sql