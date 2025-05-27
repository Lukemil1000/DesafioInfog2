# Desafio Infog2

# Sobre o projeto

DesafioInfog2 é uma API Rest desenvolvida utilizando FastApi, que tem 
como objetivo simular o back-end de uma loja.

Esse projeto foi desenvolvido como parte do processo seletivo para a 
vaga de desenvolvedor back-end júnior da Infog2

# Tecnologias utilizadas

- Python
- FastAPI
- sqlalchemy
- Pytest
- Postgresql
- Docker
- Docker-compose

# Como executar o projeto

Clone o repositório com o comando abaixo:

```
git clone https://github.com/lucaspomar/DesafioInfog2.git
```

Navegue até a pasta do projeto e use o comando:

```
docker-compose up --build
```

Ao finalizar o processo de compose o projeto ficará disponível no localhost
na porta 8000

```
http://localhost:8000
```

# Documentação

A documentação da API está disponível em /docs

```
http://localhost:8000/docs
```

# Testes

Para realizar os testes primeiro é necessário instalar as dependências
do projeto com:

```
# Recomendado criar um ambiente virtual antes da instalação
pip install -r requirements.txt
```

Os testes unitários utilizam um container de testes isolado do resto 
da aplicação e podem ser executados com o comando:

```
task test
```

# Autor

Lucas Detogni Pomar