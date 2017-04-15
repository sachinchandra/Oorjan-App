set -e
python create_tables.py
python app.py &
python db_populate.py referencedata True
python data_generate.py referencedata False
kill $!