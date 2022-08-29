# Music API With Django Rest Framework

> 

## Table of Contents

- [Music API With Django Rest Framework](#music-api-with-django-rest-framework)
  - [Table of Contents](#table-of-contents)
  - [Objetivo](#objetivo)
  - [Utilizando o projeto](#utilizando-o-projeto)
  - [Funcionamento](#funcionamento)

## Objetivo

O objetivo do projeto consiste em criar uma API REST utilizando o django rest framework na qual irá organizar as músicas, artistas e playlists. Assim, as funcionalidades desenvolvidas são: criar, editar, listar e deletar.



## Utilizando o projeto
Para utilizar o projeto, siga estas etapas:

1. Crie um env com anaconda:
```
conda create --name nomeenv python=3.10
```
2. Execute:
```
pip install -r requirements.txt
```
1. Vá para pasta musicapi:
```
cd musicapi
```
3. Execute a aplicação:
```
python manage.py runserver
```
5. Vá para http://127.0.0.1:8000 para usar e navegar

Para utilizar a aplicação usando o **Docker**, utilize o comando
```
docker-compose build 
```
e o comando 
```
docker-compose up 
```
para executar a aplicação.

Assim, para navegar vá para http://localhost:8000 




## Funcionamento

- Para utilizar ou ver a API vá para: http://127.0.0.1:8000/api
- Para ver o Schema vá para: http://127.0.0.1:8000/schema
- Para ver a documentação vá para: http://127.0.0.1:8000/docs




