TTPU
======

Tests
=====
python .\manage.py test  whowlong.tests.tests_initproject
python .\manage.py test  whowlong.tests.tests_debug_models2
python .\manage.py test
  

> 


Migration
=========
A chaque change de model faire

python manage.py makemigrations whowlong 

lancer les test :
 python .\manage.py test
 
ou
python manage.py makemigrations

python manage.py makemigrations => generer des fichier de migration mais ne les fait pas
python .\manage.py showmigrations => montre ce qui migre
python .\manage.py sqlmigrate 0012_auto_20180621_1549 => affiche ce qu'il va faire
python .\manage.py sqlmigrate makemigrations => MIGRE REELLEMENT


	
Commands
========
python .\manage.py agspGetTrajetsAround --adress "80 rue injalbert 34130 castelanu le lez" --arroundInMeter 7500


Besoins  :
===========================
conda install -c conda-forge proj4
conda install psycopg2
conda install basemap
pip install geopy
pip install geoindex
    a besoin de Microsoft visual compiler pour python : aka.ms/vcpython27/
     http://aka.ms/vcpython27
