# Creating database
psql -U postgres -c "CREATE DATABASE tttest;"

psql -U postgres -d tttest -f create_db.sql
