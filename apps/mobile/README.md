# Nexo - Mobile App

Bem-vindo ao Aplicativo Mobile do Nexo! Esta aplicação foi desenvolvida em **React Native** (geralmente orquestrada pelo **Expo**) para fornecer a melhor experiência mobile para os estudantes.

## Pré-requisitos

Para rodar o aplicativo mobile localmente você precisará de:
- **Node.js** (versão 18+ recomendada)
- **NPM** ou **Yarn**
- Conta e aplicativo do **Expo Go** instalado no seu celular, OU simulador configurado no seu computador (Android Studio / Xcode).
- O [Backend Nexo](../../backend/README.md) rodando na mesma rede (caso necessite de comunicação real com a API).

## Como Baixar e Configurar

1. **Acesse a pasta do app mobile a partir da raiz do monorepo:**
   ```bash
   cd apps/mobile
   ```

2. **Instale as dependências:**
   ```bash
   npm install
   # ou caso ocorram problemas de peer dependency:
   npm install --legacy-peer-deps
   ```

3. **Configuração de Variáveis de Ambiente:**
   - Crie um arquivo `.env` baseado no `.env.example`.
   - Se for usar o aplicativo pelo celular no Expo Go, certifique-se de configurar a `API_URL` apontando para o seu IP local (ex: `EXPO_PUBLIC_API_URL=http://192.168.1.100:8000/api/v1`) ao invés de `localhost`, pois o celular não entenderá o `localhost` do seu computador.

## Como Rodar

Para iniciar o bundler do React Native / Expo:

```bash
npm start
# ou
npx expo start
```

Uma aba do navegador abrirá com o **Metro Bundler** e um **QR Code**. 
- **Se você tiver o app Expo Go:** Abra a câmera do seu celular, escaneie o QR Code e o app abrirá no dispositivo físico.
- **Se quiser usar um simulador virtual:** Aperte `a` para abrir no Android Emulator, ou `i` para abrir no simulador iOS (Mac apenas).

## Estrutura e Testes

- Se adicionou componentes novos, escreva os testes utilizando o `@testing-library/react-native`.
- Execute os testes rodando `npm test`.
