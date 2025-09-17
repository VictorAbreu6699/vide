# 🚀 VIDE

Este é um projeto web construído com [FastAPI](https://fastapi.tiangolo.com/), utilizando templates HTML integrados (Jinja2) e jQuery no front-end.
Este projeto foi desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) pelos desenvolvedores [Gabriel](https://github.com/gabrielgbr1) e [Victor](https://github.com/VictorAbreu6699).

O artigo com a descrição do projeto pode ser acessado em: [vide.pdf](vide.pdf)

## 🧰 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) como servidor ASGI
- [Jinja2](https://jinja.palletsprojects.com/) para renderização de templates
- [jQuery](https://jquery.com/) no front-end
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)

## ✅ Requisitos

Antes de começar, você precisa ter instalado:

- Python 3.11
- PyCharm
- Git
- Mysql 8

## ⚙️ Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/VictorAbreu6699/vide.git
cd vide
```

### 2. Iniciar virtualenv
Criar local interpreter no pycharm usando o python 3.11 ou criar um virtualenv via terminal

### 3. Instalar dependencias
No terminal do virtualenv, instalar as dependencias:
```bash
pip install -r requirements.txt
```

### 4. Iniciar banco de dados
Instalar o MySql, criar um banco de dados com nome "vide".
No terminal do virtualenv, rodar comando para criar estrutura do banco de dados:
```
alembic upgrade head
```

### 5. Executar projeto:
Rodar comando abaixo para iniciar servidor
```bash
uvicorn main:app --host 0.0.0.0 --port 7878 --reload
```
Acessar: http://127.0.0.1:7878
