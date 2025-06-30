# cidadao-ai
Projeto de GenAI para a Pós-Graduação da XPE.
# Cidadão AI - Um Facilitador de Acesso a Serviços Públicos

## O Problema
No Brasil, o acesso a informações sobre serviços públicos e direitos básicos ainda é um desafio significativo para parte da população. Muitos cidadãos, especialmente aqueles em situação de vulnerabilidade socioeconômica ou com menor letramento digital, enfrentam dificuldades para:

* Compreender a linguagem técnica e burocrática utilizada em portais governamentais e documentos oficiais.
* Identificar quais serviços são adequados às suas necessidades e se são elegíveis para eles.
* Navegar em múltiplos sites e plataformas para encontrar informações consolidadas.
* Saber quais documentos são necessários e quais os passos para solicitar um serviço ou benefício.
* Localizar os pontos de atendimento físico quando necessário.

As causas desse problema são multifatoriais, incluindo a complexidade do sistema público, a fragmentação da informação, a falta de padronização e as barreiras digitais.

## A Proposta: Cidadão AI
Com base nesse cenário, o **Cidadão AI** é um projeto que propõe facilitar e centralizar o acesso a essas informações. Utilizando IA generativa, o objetivo é "traduzir" a complexidade burocrática para uma linguagem simples e acessível através de uma interface de chat intuitiva.

## Objetivo Acadêmico
Este é um Projeto Aplicado de Pós-Graduação onde se pretende aplicar conhecimentos adquiridos ao longo do curso em áreas como: métodos ágeis, desenho de arquitetura de solução, desenho de arquitetura de software e tipos de arquiteturas de software. A tecnologia principal é o Python, com o framework Flask, e o modelo Gemini Pro do Google, tudo containerizado com Docker para garantir a portabilidade.

---

## Pré-requisitos
Para executar este projeto, você precisará ter o **Docker** e o **Docker Compose** instalados em sua máquina.

-   **Windows/macOS:** A forma mais fácil é instalar o [Docker Desktop](https://www.docker.com/products/docker-desktop/).
-   **Linux:** Instale o Docker Engine e o Docker Compose seguindo as [instruções oficiais](https://docs.docker.com/engine/install/).

## Como Rodar o Projeto
Siga os passos abaixo em um terminal no seu sistema (Linux, macOS ou Windows com PowerShell/CMD).

### 1. Clonar o Repositório
```bash
git clone https://github.com/lima-renan/cidadao-ai
cd cidadao-ai
```

### 2. Configurar a Chave da API do Gemini
Você precisa de uma chave de API do Gemini, que pode ser obtida gratuitamente no [Google AI Studio](https://aistudio.google.com/app/apikey).

a. Crie uma cópia do arquivo de exemplo `.env.example` com o nome `.env`. Você pode fazer isso manualmente ou com o seguinte comando:

   _No Linux ou macOS:_
   ```bash
   cp .env.example .env
   ```
   _No Windows (CMD):_
   ```powershell
   copy .env.example .env
   ```

b. Abra o arquivo `.env` com um editor de texto (como VS Code, Bloco de Notas, etc.) e substitua `SUA_CHAVE_DE_API_GEMINI_AQUI` pela sua chave real.
```
# Exemplo de conteúdo do arquivo .env
GEMINI_API_KEY="AIzaSy...sua_chave_completa"
```

### 3. Subir o Contêiner com Docker Compose
Este comando irá construir a imagem Docker (se ainda não existir) e iniciar o contêiner da aplicação em segundo plano (`-d`).
```bash
docker compose up --build -d
```
O `--build` força a reconstrução da imagem, útil caso você faça alterações no `Dockerfile` ou `requirements.txt`.

### 4. Acessar o Chatbot
Após o comando `docker compose up` finalizar, abra seu navegador e acesse:
[http://localhost:5000](http://localhost:5000)

Você deverá ver a interface do chatbot pronta para uso.

## Desenvolvimento
O volume `./app` é mapeado para dentro do contêiner. Isso significa que qualquer alteração que você fizer nos arquivos dentro da pasta `/app` será refletida automaticamente na aplicação, sem a necessidade de reconstruir a imagem.

## Para Parar a Aplicação
Para parar e remover o contêiner, execute:
```bash
docker-compose down