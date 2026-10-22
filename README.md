# Algoritmo-de-Recomendaçao-de-Musicas-com-Base-em-Grafos

Este repositório é a base para o desafio de Criação de Algoritmo de Recomendação de Músicas com Base em Grafos da DIO baseado em `neo4J`.

Para este projeto, foi planejado utilizar a seguinte modelagem do banco de dados baseados em grafos:

<img width="1000" height="927" alt="Untitled graph" src="https://github.com/user-attachments/assets/0822f79f-99cb-4a4c-9185-8c5e1ce723a0" />

Link da imagem pode ser acessado [aqui](https://arrows.app/#/import/json=eyJncmFwaCI6eyJzdHlsZSI6eyJmb250LWZhbWlseSI6InNhbnMtc2VyaWYiLCJiYWNrZ3JvdW5kLWNvbG9yIjoiI0ZBRkNGRiIsImJhY2tncm91bmQtaW1hZ2UiOiIiLCJiYWNrZ3JvdW5kLXNpemUiOiIxMDAlIiwibm9kZS1jb2xvciI6IiM0QzhFREEiLCJib3JkZXItd2lkdGgiOjIsImJvcmRlci1jb2xvciI6IiMyODcwYzIiLCJyYWRpdXMiOjI1LCJub2RlLXBhZGRpbmciOjUsIm5vZGUtbWFyZ2luIjoyLCJvdXRzaWRlLXBvc2l0aW9uIjoiYXV0byIsIm5vZGUtaWNvbi1pbWFnZSI6IiIsIm5vZGUtYmFja2dyb3VuZC1pbWFnZSI6IiIsImljb24tcG9zaXRpb24iOiJpbnNpZGUiLCJpY29uLXNpemUiOjY0LCJjYXB0aW9uLXBvc2l0aW9uIjoiaW5zaWRlIiwiY2FwdGlvbi1tYXgtd2lkdGgiOjIwMCwiY2FwdGlvbi1jb2xvciI6IiNmZmZmZmYiLCJjYXB0aW9uLWZvbnQtc2l6ZSI6MTAsImNhcHRpb24tZm9udC13ZWlnaHQiOiJub3JtYWwiLCJsYWJlbC1wb3NpdGlvbiI6Im91dHNpZGUiLCJsYWJlbC1kaXNwbGF5IjoiYmFyZSIsImxhYmVsLWNvbG9yIjoiI2ZmZmZmZiIsImxhYmVsLWJhY2tncm91bmQtY29sb3IiOiIjNEM4RURBIiwibGFiZWwtYm9yZGVyLWNvbG9yIjoiIzRDOEVEQSIsImxhYmVsLWJvcmRlci13aWR0aCI6MCwibGFiZWwtZm9udC1zaXplIjoxMCwibGFiZWwtcGFkZGluZyI6MiwibGFiZWwtbWFyZ2luIjoyLCJkaXJlY3Rpb25hbGl0eSI6ImRpcmVjdGVkIiwiZGV0YWlsLXBvc2l0aW9uIjoiaW5saW5lIiwiZGV0YWlsLW9yaWVudGF0aW9uIjoicGFyYWxsZWwiLCJhcnJvdy13aWR0aCI6MSwiYXJyb3ctY29sb3IiOiIjQTVBQkI2IiwibWFyZ2luLXN0YXJ0IjowLCJtYXJnaW4tZW5kIjowLCJtYXJnaW4tcGVlciI6MjAsImF0dGFjaG1lbnQtc3RhcnQiOiJub3JtYWwiLCJhdHRhY2htZW50LWVuZCI6Im5vcm1hbCIsInJlbGF0aW9uc2hpcC1pY29uLWltYWdlIjoiIiwidHlwZS1jb2xvciI6IiMwMDAwMDAiLCJ0eXBlLWJhY2tncm91bmQtY29sb3IiOiIjZmZmZmZmIiwidHlwZS1ib3JkZXItY29sb3IiOiIjMDAwMDAwIiwidHlwZS1ib3JkZXItd2lkdGgiOjAsInR5cGUtZm9udC1zaXplIjoxMCwidHlwZS1wYWRkaW5nIjoyLCJwcm9wZXJ0eS1wb3NpdGlvbiI6Im91dHNpZGUiLCJwcm9wZXJ0eS1hbGlnbm1lbnQiOiJjb2xvbiIsInByb3BlcnR5LWNvbG9yIjoiIzAwMDAwMCIsInByb3BlcnR5LWZvbnQtc2l6ZSI6MTAsInByb3BlcnR5LWZvbnQtd2VpZ2h0Ijoibm9ybWFsIn0sIm5vZGVzIjpbeyJpZCI6Im4wIiwicG9zaXRpb24iOnsieCI6LTUxOC4zNDU3MTUyMzYzMDY4LCJ5Ijo0Nzg2LjI4NTM3OTIzNDM2OH0sImNhcHRpb24iOiJQZXNzb2EiLCJzdHlsZSI6eyJub2RlLWNvbG9yIjoiI2E0ZGQwMCJ9LCJsYWJlbHMiOlsiUGVyc29uIiwiVXNlciJdLCJwcm9wZXJ0aWVzIjp7IkFnZSI6IiIsIklkIjoiIiwiU2V4IjoiIn19LHsiaWQiOiJuMSIsInBvc2l0aW9uIjp7IngiOi0zMTYuNDYxOTQ2NDAxNzI5MDUsInkiOjQ3ODYuMjg1Mzc5MjM0MzY4fSwiY2FwdGlvbiI6Ik11c2ljYSIsInN0eWxlIjp7Im5vZGUtY29sb3IiOiIjNjUzMjk0In0sImxhYmVscyI6WyJNdXNpYyJdLCJwcm9wZXJ0aWVzIjp7Ikxlbmd0aCI6IiIsIlVwbG9hZGVkX2F0IjoiIiwiSWQiOiIiLCJOYW1lIjoiIn19LHsiaWQiOiJuMiIsInBvc2l0aW9uIjp7IngiOi0xODIuNTQwMzUxNTY5Nzc3NDQsInkiOjQ5NTguNjc2NDE1MzkwNDkyfSwiY2FwdGlvbiI6IkfDqm5lcm8iLCJzdHlsZSI6eyJub2RlLWNvbG9yIjoiIzMzMzMzMyJ9LCJsYWJlbHMiOlsiR2VucmUiXSwicHJvcGVydGllcyI6eyJJZCI6IiIsIk5hbWUiOiIifX0seyJpZCI6Im4zIiwicG9zaXRpb24iOnsieCI6LTIwOC4zNTQ1NDM1MTI4MDgxLCJ5Ijo0NjQ0LjU4NDkxMjEzOTMyMX0sImNhcHRpb24iOiJBcnRpc3RhIiwic3R5bGUiOnsibm9kZS1jb2xvciI6IiNmNDRlM2IifSwibGFiZWxzIjpbIlBlcnNvbiIsIkFydGlzdCJdLCJwcm9wZXJ0aWVzIjp7Ik5hbWUiOiIiLCJJZCI6IiIsIkFnZSI6IiJ9fV0sInJlbGF0aW9uc2hpcHMiOlt7ImlkIjoibjAiLCJ0eXBlIjoiTElTVEVOIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7IlF1YW50aXR5IjoiIiwiTGlrZWQiOiIifSwiZnJvbUlkIjoibjAiLCJ0b0lkIjoibjEifSx7ImlkIjoibjEiLCJ0eXBlIjoiSEFTIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjIiLCJ0b0lkIjoibjEifSx7ImlkIjoibjIiLCJ0eXBlIjoiQ09NUE9TRSIsInN0eWxlIjp7fSwicHJvcGVydGllcyI6eyJBdCI6IiJ9LCJmcm9tSWQiOiJuMyIsInRvSWQiOiJuMSJ9LHsiaWQiOiJuMyIsInR5cGUiOiJCRUxPTkciLCJzdHlsZSI6e30sInByb3BlcnRpZXMiOnt9LCJmcm9tSWQiOiJuMyIsInRvSWQiOiJuMiJ9LHsiaWQiOiJuNCIsInR5cGUiOiJGT0xMT1ciLCJzdHlsZSI6e30sInByb3BlcnRpZXMiOnt9LCJmcm9tSWQiOiJuMCIsInRvSWQiOiJuMyJ9LHsiaWQiOiJuNSIsInR5cGUiOiJMSUtFIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjAiLCJ0b0lkIjoibjIifSx7ImlkIjoibjYiLCJ0eXBlIjoiQ09OTkVDVCIsInN0eWxlIjp7ImRpcmVjdGlvbmFsaXR5IjoidW5kaXJlY3RlZCJ9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjAiLCJ0b0lkIjoibjAifV19LCJkaWFncmFtTmFtZSI6IlVudGl0bGVkIGdyYXBoIn0=)

---

## Modelagem

### Nós

-> Pessoa: possuem 2 Labels: `Person` e `User`, sendo as pessoas usuárias do sistema de recomendação de músicas. Possuem as propriedades:
 - Age: Idade em integer
 - Id: identificador único
 - Sex: sexo informado pelo usuário

-> Música possuem 1 Label: `Music`, podendo ser classificadas facilmente quando procuramos por músicas de forma unitária. Possuem as propriedades:
 - Length: Tamanho da música em segundos, integer
 - Uploaded_at: Data do upload da música na plataforma
 - Id: identificador único
 - Name: nome da música
   
-> Artista: possuem 2 Labels: `Person` e `Artist`, sendo então classificados como pessoas artistas (criadoras de música). Possuem as propriedades:
 - Name: Nome do artista/banda
 - Id: Identificador único
 - Age: Idade da banda (desde sua criação) ou do artista solo

-> Gênero: possuem 1 Label: `Genre`, sendo a unificação dos gêneros de música. Possuem as propriedades:
 - Id: identificador único
 - Name: Nome do gênero

### Relacionamentos

-> Follow: Uma Pessoa pode seguir um ou mais Artistas

-> Like: Uma Pessoa pode gostar de um ou mais Gêneros

-> Belong: Um Artista pertence a um ou mais Gêneros de músicas

-> Listen: Uma Pessoa pode ouvir uma ou mais Músicas (Propriedades: `Quantity`: número de vezes ouvida, `Liked`: Booleano se gostou da música ou não)

-> Has: Uma Música possui um ou mais Gêneros

-> Compose: Um Artista pode compor uma ou mais Músicas (Propriedade: `At`: data de composição)

-> Connect: Uma Pessoa pode se conectar a uma ou mais Pessoas

---

## Origem do banco de dados

Para alimentação do Banco de dados foi utilizado o banco originário do kaggle do [last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm) trabalhado para que as músicas pudessem ser adaptadas aos dados planejados na modelagem.

---

## Troubleshooting

- Parte das músicas não apresentava gênero dentro do banco de dados, foi utilizada então o campo de tag para selecionar como gênero (dando mais de 1 gênero para as músicas). Tags que não são consideradas gênero foram apagadas utilizando o DETACH DELETE para remoção de seus nós e relacionamentos.
