# Sistema de Controle de Estoque

A aplicação Web foi construída usando **Python**, com o framework micro-web **Flask**, motor de templates **Jinja2** e banco de dados **SQLite**.

### Funcionalidades Implementadas
1. **Modelagem e BD Automático**: O SQLite foi modelado para evitar setup complexo na máquina em que rodar. O arquivo `database.py` se encarrega de criar `estoque.db` na primeira execução, preenchendo o sistema inicialmente com o usuário mestre (`admin`).
2. **Criptografia de Senhas**: Senhas não transitam limpas no banco; usamos `werkzeug.security` para gerar hashes salgados irreversíveis.
3. **Autenticação e Sessão de Usuário**: Acesso seguro com páginas bloqueadas, mantendo a variável na sessão baseada no browser. Nenhuma funcionalidade chave roda sem usuário ativo.
4. **Perfis (Admin vs Comum)**: 
   - Usuário *Comum*: Só visualiza, cadastra e edita produtos.
   - *Administrador*: Controla o módulo de "Novo Usuário", podendo criar mais cadastros para a loja.
5. **Validação Rigorosa (*Anti-GIGO*)**: Entradas e edições com "Letras no lugar de Números" na quantidade/preço abortam o cadastro de modo seguro retornando avisos explícitos ("flash messages"), existindo tanto como `<input type="number">` (validação de Frontend / Browser) bem como validação em `int()` / `float()` e captura de exceção no Backend (Server).
6. **Usabilidade, Design Dinâmico e Alertas**: O frontend (CSS) não usou frameworks engessados, construindo em CSS puro uma interface com tipografia legível estilo *Glass* + Material, botões responsivos, mensagens de feedback fluídas e **destaque vermelho** na tabela quando um dado de produto está preenchido como "Estoque Abaixo do Mínimo".

### Como testar na sua máquina:

#### Linux / macOS

1. Certifique-se de estar com o terminal na pasta raiz do projeto.
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask werkzeug
```
2. Ative o ambiente virtual e garanta que o Flask está ativo (o `venv` já deve estar com o Flask instalado).
```bash
source venv/bin/activate
```
3. Inicie o app com o código abaixo:

```bash
python3 app.py
```

#### Windows

1. Certifique-se de estar com o terminal (CMD ou PowerShell) na pasta raiz do projeto.
```bat
python -m venv venv
venv\Scripts\activate
pip install flask werkzeug
```
2. Para ativar o ambiente virtual nas próximas vezes:
```bat
venv\Scripts\activate
```
3. Inicie o app:
```bat
python app.py
```

4. A aplicação inicializará o banco de dados nativamente e subirá um servidor. Abra a URL apresentada no terminal (normalmente `http://127.0.0.1:5000`) em qualquer navegador.
5. Realize seu primeiro login com as credenciais padrão:
   - **Usuário:** `admin`
   - **Senha:** `admin123`
6. Agora é só navegar e aproveitar o sistema!
