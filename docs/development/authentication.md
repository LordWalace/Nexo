# Autenticação e Modo "Sem Conta"

O Nexo possui uma arquitetura híbrida de autenticação, permitindo que o usuário utilize o aplicativo imediatamente de forma anônima e, posteriormente, sincronize seus dados logando com uma conta Google.

## 1. O Modo Sem Conta (Local First)
Ao abrir o app pela primeira vez, o aplicativo gera um identificador local (`localUserId` gerado por UUID) salvo de forma segura no dispositivo. 
Todas as funcionalidades básicas do aplicativo operam salvando dados localmente usando esse ID, de forma que a experiência do usuário não é bloqueada por um login.

## 2. Autenticação via Google OAuth
Quando o usuário opta por sincronizar os dados, usamos o Google Sign-In para gerar um `id_token` no frontend. Esse token é enviado ao backend na rota `POST /api/v1/auth/google`.

### No Backend:
- O backend recebe o `id_token`.
- O token é validado pela biblioteca `google-auth` para verificar assinatura, data de expiração e emissor.
- É extraído o `email` e o `sub` (Google Subject ID).
- Se já existe um usuário com esse email, o `sub` é atualizado (se necessário) e o login ocorre.
- Se o usuário for novo, um novo registro na tabela `users` é criado sem `password_hash` (campo agora `nullable`) e preenchido com os dados extraídos do Google.
- O backend finaliza gerando um JWT padrão de acesso à API e devolvendo ao cliente.

## 3. Sincronização de Dados (Merge Local -> Remoto)
Assim que o login for efetivado pela primeira vez em um celular:
- O mobile itera por todos os registros criados em modo offline.
- Submete-os via os endpoints originais do backend para criar a cópia de segurança remota usando o novo token JWT do usuário.
- O aplicativo passa a operar no modo "online", e o banco de dados remoto atua como a fonte da verdade daquele momento em diante. Em outros dispositivos com a mesma conta, os dados serão diretamente baixados.
