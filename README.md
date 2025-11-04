# ache-facil
Sistema de Achados e Perdidos Digital para a disciplina de Projeto Integrador II da UNIVESP

#### Comandos para lidar com o ambiente virtual: 
```bash
#criar um 
python3 -m venv env
#rodar um ambiente
source env/bin/activate
#congelar pacotes
pip freeze > requirements.txt
#aplicar pacotes de um txt
pio install -r requirements.txt
```


#### Comandos para rodar a aplicação: 
```bash
#criar um app
python3 manage.py startapp <nome>
#migrations
python manage.py makemigrations ache_facil
python manage.py migrate
#rodar o servidor
python3 manage.py runserver
```