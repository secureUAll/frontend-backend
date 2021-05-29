# Django testing

> Based on https://developer.mozilla.org/pt-BR/docs/Learn/Server-side/Django/Testing



## Classes de testes

https://docs.djangoproject.com/en/2.1/topics/testing/tools/#provided-test-case-classes



## Assertions

https://docs.djangoproject.com/en/2.1/topics/testing/tools/#assertions



## Tipos de testes



### Modelo de dados

- Testar que <u>labels dos campos são válidos</u>;
- Restrições definidas por nós são respeitadas (por exemplo `max_length`);
- Testar ainda os métodos escritos por nós!



### Formulários

- Campos têm <u>labels corretos e textos de ajuda</u>;
- Validações definidas por nós (métodos `clean()` e `clean_attr()`) e mensagens de erro retornadas.



### Views

- Verificar se view é acessível no link correto (por link e por nome com `reverse()`) e retorna status esperado;
- Contexto da resposta (`self.context` como `response.context`);
- Validar restrições de acesso por autores;
- Template utilizado;
- Formulários utilizados (submissões válidas e não, com validação do feedback);



### Testes adicionais 

- Selenium
- unittest.mock
- Coverage.py





## Coverage reports

Através da biblioteca [coverage](https://coverage.readthedocs.io/en/latest/) pode ser analisada a cobertura dos testes.

Para fazer a análise, basta correr o comando abaixo, na raiz do projeto (mesma pasta que o ficheiro `manage.py`).

```bash
# Fazer análise ao projeto
$ coverage run --omit=venv/*,*/migrations/*,*/tests/*,*/__init__.py manage.py test --verbosity 2
```

O resultado da análise pode ser visto na bash.

```bash
# Ver relatório na bash
$ coverage report [-m] # -m para ver linhas não abrangidas pelos testes
```

Ou em alternativa, ser gerado um microsite HTML com a informação, o que facilita a sua análise. O site será disponibilizado na pasta `htmlcov/index.html`, a partir do qual pode ser analisado cada ficheiro individualmente.

```bash
$ coverage html
```

