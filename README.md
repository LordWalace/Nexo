# Nexo Monorepo

Bem-vindo ao **Nexo**, um aplicativo de gerenciamento completo e moderno.

O projeto está dividido em aplicações (Frontend/Mobile) e serviços (Backend), todos organizados em um único repositório para facilitar o desenvolvimento e a manutenção.

## Estrutura do Projeto

```bash
nexo/
├── apps/
│   ├── frontend/   # Aplicação Web (React / Next.js)
│   └── mobile/     # Aplicação Mobile (React Native / Expo)
├── backend/        # API Restful (FastAPI, Python, PostgreSQL)
├── packages/       # Bibliotecas e componentes compartilhados (se houver)
├── infrastructure/ # Configurações de Deploy e Containers (Docker, etc)
├── tests/          # Testes E2E globais (se aplicável)
└── docs/           # Documentações gerais adicionais
```

---

## Guias Específicos (Documentação por Módulo)

Para saber como baixar as dependências, configurar o ambiente e rodar cada parte do sistema isoladamente, leia os READMEs específicos de cada módulo abaixo:

- **Quer saber mais sobre o Backend?**  
  [Leia o README do Backend](./backend/README.md)

- **Quer saber mais sobre o aplicativo Mobile?**  
  [Leia o README do Mobile](./apps/mobile/README.md)

- **Quer saber mais sobre o Frontend?**  
  [Leia o README do Frontend](./apps/frontend/README.md)

---

## Comandos Padrões Globais

Na raiz do projeto, você poderá rodar comandos úteis, especialmente se utilizar ferramentas como o Docker (via `docker-compose`).

- **Iniciar Serviços Base (Banco de Dados, Redis, etc):**
  ```bash
  docker compose up -d
  ```

- **Parar Serviços Base:**
  ```bash
  docker compose down
  ```

*Aviso: Para rodar comandos específicos de cada projeto (como `npm start` ou `pytest`), você deve navegar até a respectiva pasta (ex: `cd backend`).*

---

## Padrões de Código e Diretrizes

### Convenções Gerais
1. **Idioma**: O código fonte (variáveis, classes, métodos) deve ser escrito em **Inglês**. Comentários e documentações mais robustas podem ser em português (como este README), mas priorize o inglês no código.
2. **Nomenclatura**:
   - `snake_case` para variáveis e funções em Python.
   - `camelCase` para variáveis e funções em TypeScript/JavaScript.
   - `PascalCase` para Classes e Componentes React.
   - `kebab-case` para nomes de arquivos no frontend (ex: `user-profile.tsx`).
3. **Formatação e Linting**: O projeto adota ferramentas de lint automáticas. Certifique-se de executar `ruff check .` no backend e `eslint` no frontend antes de fazer commit.

### Como criar e revisar PRs (Pull Requests)
1. **Branching**:
   - Nunca faça commits direto na `main`.
   - Crie branches com padrões semânticos. Exemplos: `feature/adicionar-login`, `fix/erro-banco`, `chore/atualizar-deps`.
2. **Commits**:
   - Use [Conventional Commits](https://www.conventionalcommits.org/).
   - Exemplos: `feat: add user authentication`, `fix: resolve crash on mobile header`, `docs: update readme`.
3. **Revisão de PR**:
   - Todo PR deve ter um título claro sobre o que foi resolvido.
   - Caso inclua alterações visuais no frontend/mobile, adicione screenshots ou vídeos ao PR.
   - Deve ser aprovado por pelo menos 1 revisor.
   - O CI (Lint e Testes) deve estar com status **verde (passando)**.