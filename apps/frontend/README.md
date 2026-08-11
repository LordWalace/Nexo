# Nexo - Web Frontend

Bem-vindo ao Frontend Web do Nexo! Esta aplicação é responsável pela interface principal acessada via navegador. Foi construída com um framework moderno em JavaScript/TypeScript.

## Pré-requisitos

Para rodar o frontend localmente você precisará ter instalado:
- **Node.js** (versão 18+ recomendada)
- **NPM**, **Yarn** ou **PNPM**
- O [Backend Nexo](../../backend/README.md) rodando localmente (caso necessite de dados reais).

## Como Baixar e Configurar

1. **Acesse a pasta do frontend a partir da raiz do monorepo:**
   ```bash
   cd apps/frontend
   ```

2. **Instale as dependências:**
   ```bash
   npm install
   # ou
   yarn install
   ```

3. **Configuração de Variáveis de Ambiente:**
   - Crie um arquivo `.env.local` ou `.env` dentro da pasta `apps/frontend`.
   - Configure a URL base da API (ex: `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`). 
   *(Verifique o arquivo `.env.example` caso exista na pasta para as chaves exatas)*

## Como Rodar

Para iniciar o servidor de desenvolvimento:

```bash
npm run dev
# ou
yarn dev
```

Acesse a aplicação no seu navegador: [http://localhost:3000](http://localhost:3000) (ou a porta que for informada no terminal).

## Testes e Qualidade de Código

- Para checar e corrigir o Lint: `npm run lint` ou `npm run lint --fix`
- Para rodar os testes unitários (ex: Jest/Vitest): `npm test`
- Certifique-se que todo código submetido em PRs não introduza novos _warnings_ de Lint.
