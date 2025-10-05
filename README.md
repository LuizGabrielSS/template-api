# Template API Flask

Um template completo e robusto para criação rápida de APIs Flask com as melhores práticas de desenvolvimento.

## 📋 Sobre o Projeto

Este template foi desenvolvido para acelerar a criação de novas APIs Flask, fornecendo uma estrutura base bem organizada e configurada com componentes essenciais para desenvolvimento profissional.

## 🏗️ Estrutura do Projeto

```text
template-api/
├── app.py          # Entrada da aplicação: cria e configura a Flask app e registra blueprints/rotas
├── Dockerfile      # Instruções para build da imagem e execução em container
├── README.md       # Documentação do projeto
├── components/     # Componentes reutilizáveis e auxiliares
│   ├── logger.py   # Sistema de logging configurado (formatos, handlers, níveis)
│   ├── secrets.py  # Gerenciamento/carregamento de variáveis sensíveis (.env, Vault, etc.)
│   └── timer.py    # Utilitários para medir performance e tempos de execução
├── routes/         # Definição das rotas/blueprints da API
│   └── healthy.py  # Endpoint de health check (ex.: /health) e exemplo de rota
└── src/            # Código fonte da aplicação
    └── login.py    # Módulo de autenticação (validações, tokens, helpers)

Notas rápidas:

- Registre novas rotas/blueprints em app.py ao adicionar arquivos em routes/.
- Mantenha secrets fora do repositório (use .env, variáveis de ambiente ou um cofre de segredos).
- Aproveite components para centralizar lógica cross-cutting (logging, monitoramento, etc.).
- Renomeie e adapte a estrutura conforme as necessidades do seu projeto.
```


## 🚀 Características do Template

### ✅ Estrutura Organizada
- **Separação de responsabilidades** com módulos específicos
- **Arquitetura modular** para fácil manutenção e escalabilidade
- **Organização clara** de rotas, componentes e código fonte

### ✅ Componentes Prontos
- **Sistema de Logging** configurado e pronto para uso
- **Gerenciamento de Secrets** para variáveis de ambiente sensíveis
- **Utilitários de Timer** para monitoramento de performance
- **Health Check** endpoint para monitoramento da aplicação

### ✅ Containerização
- **Dockerfile** configurado para deploy em containers
- Pronto para ambientes de produção e desenvolvimento

### ✅ Autenticação
- Módulo de login base para implementação de autenticação

## 🛠️ Como Usar Este Template

### 1. Clone o Template
```bash
git clone <url-do-repositorio>
cd template-api
```

### 2. Configure o Ambiente
```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual (Windows)
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configure as Variáveis de Ambiente
```bash
# Copie o arquivo de exemplo (se existir) ou crie um .env
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 4. Execute a Aplicação
```bash
python app.py
```

### 5. Teste o Health Check
```bash
curl http://localhost:5000/health
```

### 🔧 Personalizando para Seu Projeto

1. Renomeie o Projeto

    - Atualize o nome nos arquivos de configuração
    - Modifique as referências no código conforme necessário

2. Adicione Suas Rotas

    - Crie novos arquivos em routes seguindo o padrão do healthy.py
    - Registre as novas rotas no app.py

3. Implemente Sua Lógica de Negócio

    - Adicione seus módulos em src
    - Utilize os componentes prontos em components

4. Configure Logging

    - Personalize o sistema de logging em logger.py
    - Defina níveis e formatos conforme sua necessidade


### 📦 Deploy
```bash
# Build da imagem
docker build -t minha-api .

# Execute o container
docker run -p 5000:5000 minha-api
```


### Produção

- Configure variáveis de ambiente adequadas
- Utilize um servidor WSGI como Gunicorn
- Configure reverse proxy (Nginx)
- Implemente monitoramento e logs

### 🧪 Testes
```bash
# Execute os testes unitários
python -m pytest tests/

# Execute com coverage
python -m pytest tests/ --cov=src --cov=components --cov=routes
```

