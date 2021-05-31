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



## Selenium

> [Documentação Django com exemplo de teste](https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.LiveServerTestCase)

### Set up para Firefox

1. Fazer download do driver em https://github.com/mozilla/geckodriver/releases/;
2. Extrair driver e colocá-lo em `/opt/WebDriver/bin` (por exemplo);
3. Adicionar localização à variável `$PATH`;

```bash
export PATH=$PATH:/opt/WebDriver/bin >> ~/.profile
```

4. Testar que funciona;

```bash
chromedriver
```

> Output esperado:
>
> ```text
> Starting ChromeDriver 2.25.426935 (820a95b0b81d33e42712f9198c215f703412e1a1) on port 9515
> Only local connections are allowed.
> ```



### Behave

Para facilitar a escrita dos testes podemos utilizar a biblioteca [Behave](https://behave.readthedocs.io/en/stable/index.html), que permite a escrita dos testes em linguagem natural, de forma análoga ao Cucumber para Java.

Para tal basta criar um ficheiro `XXX.feature` na pasta `features` que se encontra na raiz do projeto (na mesma pasta que o ficheiro `manage.py`). A implementação dos testes é feita dentro da pastas `features/steps`, num ficheiro `.py`, de nome livre.

> Não é necessário escrever os testes de raiz. Uma vez escritos em linguagem natural no ficheiro `.feature`, basta correr o comando dos testes que ele vai identificar as linhas que não estão implementadas e fornecer um esqueleto para o método, que pode ser copiado para os ficheiros dos steps.

O tutorial oficial pode ser consultado [aqui](https://behave.readthedocs.io/en/stable/tutorial.html).

Para correr os testes, corre-se o comando abaixo.

```bash
$ python manage.py behave
```

