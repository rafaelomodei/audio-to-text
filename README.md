# Converter áudio em texto

<img alt="audio to text" src="./img/img-readme.png" width="200" />

## Descrição

Este projeto é uma aplicação que tem como objetivo transformar áudio em texto de maneira automática e precisa. Utilizando técnicas avançadas de processamento de sinais de áudio e inteligência artificial, a aplicação é capaz de transcrever áudios MP3 em textos claros e concisos.


### Features

- [x] Importar arquivos de mídias
- [x] Ler grandes arquivos de mídias
- [ ] Suportar arquivos de mídias MP4, WAV, OGG e outros
- [X] Salvar texto em arquivo
- [X] Tratativa para não substituir arquivos já gerados


### Executando o script


**Baixando o repositório**

```bash
# Clone o repositório
$ git clone git@github.com:rafaelomodei/audio-to-text.git

# Acesse a pasta do projeto no terminal/cmd
$ cd media-to-text
```

O ideal é ter um ambiente virtual para executar o script
Neste caso vamos estar usando virtualenv
[DOC para instalar virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

**Configurando o ambiente**

```bash
# Criando ambiente virtual
$ virtualenv audio-to-text

# Ativando o ambiente
$ source audio-to-text/bin/activate

# Instalando as dependências
$ pip install -r requirements.txt
```
**Adicionando a env no projeto**

Temos um arquivo .env.example na raiz do projeto, basca copiar ou renomear para .env.example

Após esse processo, pode acessar o site da openai e obter a sua key. [Click aqui para acessar a pagina da openia](https://platform.openai.com/account/api-keys)

depois é só abrir o arquivo .env e adicionar a sua key, exemplo:

```bash
    OPENAI_API_KEY = "SUA KEY AQUI"
```

**Entendendo os comandos**

Diretório e o nome do arquivo a ser carregado, exemplo:
```--file audio-test.mp3```

Label é um identificador da resposta a ser gerada:
```--label teste```

Diretório de saída, onde deve ser salvo o texto de saída, por padrão o diretório é output:
```--out-dir output```

**Executando o script**

```bash
# Para visualizar os comandos
$ python3 main.py -h

# Por fim é hora de executar o script
$  python3 main.py --file audio-test.mp3 --label audio-test

# O script deve apresentar os passos que estão sendo realizado no momento
# Ao finalizar deve existir um novo diretório sem local
# E dentro contendo os arquivos relacionados a transcrição do da mídia
```