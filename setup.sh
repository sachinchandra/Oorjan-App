set -e
python create_tables.py
sudo apachectl restart
python db_populate.py referencedata True
python data_generate.py referencedata False
