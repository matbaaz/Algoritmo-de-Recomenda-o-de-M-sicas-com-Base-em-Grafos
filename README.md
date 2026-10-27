# Algoritmo-de-Recomendação-de-Músicas-com-Base-em-Grafos

Este repositório é a base para o desafio de Criação de Algoritmo de Recomendação de Músicas com Base em Grafos da DIO baseado em `Neo4J`.

## Por que utilizar um banco de dados baseado em grafos para a modelagem de um sistema de recomendação de músicas?

Os bancos de dados baseados em grafos possuem uma característica que os BDs relacionais (SQL) não possuem: podem realizar relacionamentos entre nós (entidades) de forma mais simples. Os relacionamentos são guardados diretamente entre os nós, sem precisar comparar chaves.

Isso significa que podemos realizar queries de pesquisa com linguagem mais simples e com maior eficiência, desde que essa query de pesquisa requeira diversos pulos entre várias "tabelas".
A quantidade de joins necessários para percorrer um banco SQL inteiro depende das restrições e relacionamento entre as tabelas, já no Neo4J precisamos somente mostrar o caminho de nós e relacionamentos para podermos percorrer grandes caminhos. Com essa facilidade podemos calcular mais intuitivamente:
 - Vizinhança: nós perto e parecidos
 - Recomendação: usuário -> item -> outro usuário -> item recomendado
 - Menor caminho: como no linkedin que mostra as conexões - 1, 2, 3 ou mais de distância
   
Para este projeto, foi planejado utilizar a seguinte modelagem do banco de dados baseados em grafos:

<img width="1000" height="927" alt="Untitled graph" src="https://github.com/user-attachments/assets/0822f79f-99cb-4a4c-9185-8c5e1ce723a0" />


CALL db.schema.visualization()

<img width="824" height="586" alt="image" src="https://github.com/user-attachments/assets/c78392b2-a561-4341-9eac-0fb6092c3485" />


Link da imagem de modelagem no arrows.app pode ser acessado [aqui](https://arrows.app/#/import/json=eyJncmFwaCI6eyJzdHlsZSI6eyJmb250LWZhbWlseSI6InNhbnMtc2VyaWYiLCJiYWNrZ3JvdW5kLWNvbG9yIjoiI0ZBRkNGRiIsImJhY2tncm91bmQtaW1hZ2UiOiIiLCJiYWNrZ3JvdW5kLXNpemUiOiIxMDAlIiwibm9kZS1jb2xvciI6IiM0QzhFREEiLCJib3JkZXItd2lkdGgiOjIsImJvcmRlci1jb2xvciI6IiMyODcwYzIiLCJyYWRpdXMiOjI1LCJub2RlLXBhZGRpbmciOjUsIm5vZGUtbWFyZ2luIjoyLCJvdXRzaWRlLXBvc2l0aW9uIjoiYXV0byIsIm5vZGUtaWNvbi1pbWFnZSI6IiIsIm5vZGUtYmFja2dyb3VuZC1pbWFnZSI6IiIsImljb24tcG9zaXRpb24iOiJpbnNpZGUiLCJpY29uLXNpemUiOjY0LCJjYXB0aW9uLXBvc2l0aW9uIjoiaW5zaWRlIiwiY2FwdGlvbi1tYXgtd2lkdGgiOjIwMCwiY2FwdGlvbi1jb2xvciI6IiNmZmZmZmYiLCJjYXB0aW9uLWZvbnQtc2l6ZSI6MTAsImNhcHRpb24tZm9udC13ZWlnaHQiOiJub3JtYWwiLCJsYWJlbC1wb3NpdGlvbiI6Im91dHNpZGUiLCJsYWJlbC1kaXNwbGF5IjoiYmFyZSIsImxhYmVsLWNvbG9yIjoiI2ZmZmZmZiIsImxhYmVsLWJhY2tncm91bmQtY29sb3IiOiIjNEM4RURBIiwibGFiZWwtYm9yZGVyLWNvbG9yIjoiIzRDOEVEQSIsImxhYmVsLWJvcmRlci13aWR0aCI6MCwibGFiZWwtZm9udC1zaXplIjoxMCwibGFiZWwtcGFkZGluZyI6MiwibGFiZWwtbWFyZ2luIjoyLCJkaXJlY3Rpb25hbGl0eSI6ImRpcmVjdGVkIiwiZGV0YWlsLXBvc2l0aW9uIjoiaW5saW5lIiwiZGV0YWlsLW9yaWVudGF0aW9uIjoicGFyYWxsZWwiLCJhcnJvdy13aWR0aCI6MSwiYXJyb3ctY29sb3IiOiIjQTVBQkI2IiwibWFyZ2luLXN0YXJ0IjowLCJtYXJnaW4tZW5kIjowLCJtYXJnaW4tcGVlciI6MjAsImF0dGFjaG1lbnQtc3RhcnQiOiJub3JtYWwiLCJhdHRhY2htZW50LWVuZCI6Im5vcm1hbCIsInJlbGF0aW9uc2hpcC1pY29uLWltYWdlIjoiIiwidHlwZS1jb2xvciI6IiMwMDAwMDAiLCJ0eXBlLWJhY2tncm91bmQtY29sb3IiOiIjZmZmZmZmIiwidHlwZS1ib3JkZXItY29sb3IiOiIjMDAwMDAwIiwidHlwZS1ib3JkZXItd2lkdGgiOjAsInR5cGUtZm9udC1zaXplIjoxMCwidHlwZS1wYWRkaW5nIjoyLCJwcm9wZXJ0eS1wb3NpdGlvbiI6Im91dHNpZGUiLCJwcm9wZXJ0eS1hbGlnbm1lbnQiOiJjb2xvbiIsInByb3BlcnR5LWNvbG9yIjoiIzAwMDAwMCIsInByb3BlcnR5LWZvbnQtc2l6ZSI6MTAsInByb3BlcnR5LWZvbnQtd2VpZ2h0Ijoibm9ybWFsIn0sIm5vZGVzIjpbeyJpZCI6Im4wIiwicG9zaXRpb24iOnsieCI6LTUxOC4zNDU3MTUyMzYzMDY4LCJ5Ijo0Nzg2LjI4NTM3OTIzNDM2OH0sImNhcHRpb24iOiJQZXNzb2EiLCJzdHlsZSI6eyJub2RlLWNvbG9yIjoiI2E0ZGQwMCJ9LCJsYWJlbHMiOlsiUGVyc29uIiwiVXNlciJdLCJwcm9wZXJ0aWVzIjp7IkFnZSI6IiIsIklkIjoiIiwiU2V4IjoiIn19LHsiaWQiOiJuMSIsInBvc2l0aW9uIjp7IngiOi0zMTYuNDYxOTQ2NDAxNzI5MDUsInkiOjQ3ODYuMjg1Mzc5MjM0MzY4fSwiY2FwdGlvbiI6Ik11c2ljYSIsInN0eWxlIjp7Im5vZGUtY29sb3IiOiIjNjUzMjk0In0sImxhYmVscyI6WyJNdXNpYyJdLCJwcm9wZXJ0aWVzIjp7Ikxlbmd0aCI6IiIsIlVwbG9hZGVkX2F0IjoiIiwiSWQiOiIiLCJOYW1lIjoiIn19LHsiaWQiOiJuMiIsInBvc2l0aW9uIjp7IngiOi0xODIuNTQwMzUxNTY5Nzc3NDQsInkiOjQ5NTguNjc2NDE1MzkwNDkyfSwiY2FwdGlvbiI6IkfDqm5lcm8iLCJzdHlsZSI6eyJub2RlLWNvbG9yIjoiIzMzMzMzMyJ9LCJsYWJlbHMiOlsiR2VucmUiXSwicHJvcGVydGllcyI6eyJJZCI6IiIsIk5hbWUiOiIifX0seyJpZCI6Im4zIiwicG9zaXRpb24iOnsieCI6LTIwOC4zNTQ1NDM1MTI4MDgxLCJ5Ijo0NjQ0LjU4NDkxMjEzOTMyMX0sImNhcHRpb24iOiJBcnRpc3RhIiwic3R5bGUiOnsibm9kZS1jb2xvciI6IiNmNDRlM2IifSwibGFiZWxzIjpbIlBlcnNvbiIsIkFydGlzdCJdLCJwcm9wZXJ0aWVzIjp7Ik5hbWUiOiIiLCJJZCI6IiIsIkFnZSI6IiJ9fV0sInJlbGF0aW9uc2hpcHMiOlt7ImlkIjoibjAiLCJ0eXBlIjoiTElTVEVOIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7IlF1YW50aXR5IjoiIiwiTGlrZWQiOiIifSwiZnJvbUlkIjoibjAiLCJ0b0lkIjoibjEifSx7ImlkIjoibjEiLCJ0eXBlIjoiSEFTIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjIiLCJ0b0lkIjoibjEifSx7ImlkIjoibjIiLCJ0eXBlIjoiQ09NUE9TRSIsInN0eWxlIjp7fSwicHJvcGVydGllcyI6eyJBdCI6IiJ9LCJmcm9tSWQiOiJuMyIsInRvSWQiOiJuMSJ9LHsiaWQiOiJuMyIsInR5cGUiOiJCRUxPTkciLCJzdHlsZSI6e30sInByb3BlcnRpZXMiOnt9LCJmcm9tSWQiOiJuMyIsInRvSWQiOiJuMiJ9LHsiaWQiOiJuNCIsInR5cGUiOiJGT0xMT1ciLCJzdHlsZSI6e30sInByb3BlcnRpZXMiOnt9LCJmcm9tSWQiOiJuMCIsInRvSWQiOiJuMyJ9LHsiaWQiOiJuNSIsInR5cGUiOiJMSUtFIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjAiLCJ0b0lkIjoibjIifSx7ImlkIjoibjYiLCJ0eXBlIjoiQ09OTkVDVCIsInN0eWxlIjp7ImRpcmVjdGlvbmFsaXR5IjoidW5kaXJlY3RlZCJ9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjAiLCJ0b0lkIjoibjAifV19LCJkaWFncmFtTmFtZSI6IlVudGl0bGVkIGdyYXBoIn0=)

---

## Modelagem

### Nós

|Nome|Labels|Propriedades|
|---|---|---|
|Usuário|Person, User|Age, Id, Sex|
|Música|Musica|Length, Uploaded_at, Id, Name|
|Artista|Person, Artist|Name, Id, Age|
|Gênero|Gênero|Id, Name|

!! Note - Os labels de Person foram removidos por tornar os relacionamentos desnecessariamente complexos, pensei em herança (como em orientado a objeto) mas não achei que fez sentido no banco, então removi como dito abaixo.

### Relacionamentos

|Relacionamento|Propriedades|
|---|---|
|Follows||
|Likes_genre||
|Belongs||
|Listen|Quantity, Liked|
|Has||
|Composed|At|
|Connected||

---

## Origem do banco de dados

Para alimentação do Banco de dados foi utilizado o banco originário do kaggle do [last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm) trabalhado para que as músicas pudessem ser adaptadas aos dados planejados na modelagem.

---

## Forma de utilização do Banco

Os arquivos originais baixados do link acima do kaggle devem ser extraídos do .zip em que são fornecidos e tratados pelos scripts python dentro de `scripts/`. A ordem de execução deve ser:
1. `prepare_data.py`
2. `shrink_listening.py`
3. `prepare_users.py`

Dessa forma, temos a partir do prepare os valores de `músicas`, `artistas`, `gêneros` e seus relacionamentos `composed` e `has`. O script de `shrink` é necessário pois os dados de usuários e músicas ouvidas é grande demais para ser incluído dentro do Aura Free tier. E após o `prepare` temos os `usuários` junto dos relacionamentos de `likes_genre`, `follows`, `connected` e `listen`. Notem que em nenhum momento os artistas estão conectados aos seus gêneros, isso acontece pois na base de dados os artistas não tinham ligação explicita com os gêneros musicais.

Os arquivos .csv gerados dos scripts foram carregados no Neo4j Aura todos ao mesmo tempo e a ferramenta de IA para inferir os nós e relacionamentos foi utilizada, gerando um bom resultado para as relações esperadas.

A query de geração do relacionamento de `belong` deve ser rodada para gerar esse relacionamento e então termos o design da nossa modelagem completo. Foi utilizado uma forma de que o gênero mais tocado pelo artista é incluído em seus gêneros, juntamente com o parâmetro de mais de 20% das músicas.

Os scripts de limpeza tiveram que ser criados e rodados, como podemos ver abaixo em toubleshooting.

---

## Respostas adquiridas deste desafio

Para mostrar todo o poder do Neo4J algumas queries foram criadas (scripts/desafio.txt) e seus resultados apresentados das queries nas imagens (imagens/desafio.md). As análises das respostas encontradas se darão aqui abaixo:

### Query 1: Quem ouviu o mesmo que você curtiu?
 A ideia aqui é encontrar primeiramente pessoas com os mesmos gostos musicais e tenham ouvido as mesmas músicas que o usuário. A partir daí são encontradas músicas que este outro usuário tenha ouvido mas o primeiro não e essas músicas então são recomendadas.

### Query 2: Gêneros que o usuário curte.
A ideia é recomendar a partir dos gêneros que o usuário já curte. Se não ouviu alguma música desse gênero, ela então é recomendada.

### Query 3: Quais artistas as pessoas que eu me conectei seguem?
A ideia é mostrar quais são os artistas que as pessoas que o usuário se conectou segue, que o próprio usuário não segue.

### Query 4: Quem segue este artista seguem quem também?
Desejamos mostrar os outros artistas seguidos por pessoas que seguem um artista, dessa forma é uma pesquisa não direcionada no usuário e sim no artista.

### Query 5: Quem é o usuário?
Mostra de forma visual conexões, likes, músicas ouvidas e tudo mais sobre um usuário. Limitei em 40 para visualização. Conseguimos traçar perfil e ecossistema utilizando essa query.

### Query 6: Gêneros mais curtidos por faixa etária.
A sexta query idealizada mostra uma separação por faixa etária. Poderemos entender melhor o problema encontrado em troubleshooting.

---

## Troubleshooting

- Person dentro da estrutura gerou uma maior complexidade de relacionamentos na visualização no CALL db.schema.visualization(). Dessa forma deletei o nó de Person dos relacionamentos com MATCH (a:Artista) REMOVE a:Person. Removido também de usuário.
<img width="589" height="378" alt="image" src="https://github.com/user-attachments/assets/f83e72f1-18ca-43c1-84b6-6d95d1dfe424" />


- Houveram 3 artistas com idades não esperadas (1 com null e 2 com acima de 80 anos). Fiz o set manual deles com a idade em seu momento de falecimento (Betty Wright, Billie Holiday e Lucille Bogan).

- Parte das músicas não apresentava gênero dentro do banco de dados, foi utilizada então o campo de tag para selecionar como gênero (dando mais de 1 gênero para as músicas). Tags que não são consideradas gênero foram apagadas utilizando o DETACH DELETE para remoção de seus nós e relacionamentos.

- Para mais ouvidos por faixa etária (Recomendação 6) pela forma que o banco foi gerado, houve diferença no 6º para frente dos gêneros. Dessa forma mantive em 3 somente para visualização simplificada. Como as idades foram geradas de forma aleatória no script python, esse dado ficou desconexo da realidade dentro desta base. Lembrando que o banco original não possuia idades dos usuários, por isso foram criados de forma aleatória em script.
