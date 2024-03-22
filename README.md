# Projeto Lista Jogos ![Status](https://img.shields.io/badge/STATUS-Concluido-y) ![Python](https://img.shields.io/badge/Python-3776AB?style=()&logo=python&logoColor=ffffff) ![Flask](https://img.shields.io/badge/Flask-000000?style=()&logo=flask&logoColor=ffffff) ![SQLServer](https://img.shields.io/badge/SQL_Server-CC2927?style==()&logo=microsoftsqlserver&logoColor=ffffff) ![HTML](https://img.shields.io/badge/HTML-E34F26?style=()&logo=html5&logoColor=ffffff) ![CSS](https://img.shields.io/badge/CSS-1572B6?style=()&logo=css3&logoColor=ffffff) ![GIT](https://img.shields.io/badge/GIT-F05032?style=()&logo=git&logoColor=ffffff) ![VSCode](https://img.shields.io/badge/VS_Code-007ACC?style=()&logo=visualstudiocode&logoColor=ffffff)

Projeto com ênfase no Back-End para testar minhas habilidades.
Conceitos aprendidos na plataforma [Alura](https://www.alura.com.br/).

### Características do Projeto:
* Persistencia de Dados com SQl Server
* Criação e Autenticação de Usuários
* Validação de Formularios
* Criptografia de senhas
* Proteção contra Cross-site request forgery
* Armazenamento das Imagens por dados binarios
* Manipulação de Informações Orientada a Objetos
* CRUD Completo dos Jogos
* Backup do Banco de Dados

# Diagrama das tabelas
![Diagrama-Tabelas](https://github.com/JoaoSouzaXMP/Projeto-Lista-Jogos/blob/main/uploads/imgs/diagrama_tabelas.png)

# Visualização
<video controls src="https://github.com/JoaoSouzaXMP/Projeto-Lista-Jogos/blob/main/uploads/imgs/visualiza%C3%A7%C3%A3o.mp4" title="visualização.mp4"></video>
# Instalando e Executando

> [!IMPORTANT]
> Certifique-se de ter o [Git 2.44.0](https://git-scm.com/download/win), [Python 3.12.2](https://www.python.org/downloads/release/python-3122/) e o [SQL Server Express 2022 ](https://www.microsoft.com/pt-br/sql-server/sql-server-2022) instalados.
> Utilize o Editor de códigos de sua preferência.

Com os pré-requisitos satisfeitos pode seguir com as instruções abaixo.
1. Clone o código fonte:
```git
git clone https://github.com/JoaoSouzaXMP/Projeto-Lista-Jogos.git
```

2. Crie um ambiente virtual para o projeto :
```
python -m venv venv
```

3. Ative o ambiente virtual:
```
.\venv\Scripts\Activate.ps1
```

4. Instale todos os Frameworks:
```
python -m pip install flask
```
```
python -m pip install -U Flask-WTF
```
```
python -m pip install flask-bcrypt
```
```
python -m pip install pyodbc
```
```
python -m pip install werkzeug
```

## Iniciando o Programa
### Ajustes no codigo
Se instalou a mesma versão do SQL Server e não alterou os parâmetros padrão da instalação, então não vai precisar ajustar os arquivos, mas se alterou, insira nos arquivos create_database.py e config.py as duas variáveis da ConnectionString, o DRIVER e o SERVER:
![ConnectionString](https://github.com/JoaoSouzaXMP/Projeto-Lista-Jogos/blob/main/uploads/imgs/ConnectionStringg.jpg)

#### Com todos os ajustes feitos utilize o comando para rodar a aplicação.
```
python main.py
```
> [!IMPORTANT]
> O Projeto agora está em execução e pode ser acessado apontando um navegador da web para [http://localhost:25565/](http://localhost:25565/)

> [!NOTE]
> Para acessar o Projeto de fora da sua rede utilize seu [IP Externo](https://www.invertexto.com/teste-de-portas), ou utilize um [DNS Dinamico](https://www.noip.com/pt-BR) para não ter o trabalho de trocar o IP caso mude.
> 
> Usuário e Senha Padrão: admin 1234

<br>

# Backup 
Para configurarmos o backup do banco de dados, precismos executar este comando no Management Studio (SSMS), altere o caminho forme a sua escolha.
```
CREATE procedure BACKUP_dbListaJogos
AS
DECLARE @Caminho varchar(MAX)
DECLARE @Descricao varchar(MAX)
set @Caminho = 'D:\Backups\' + 'dbListaJogos' + replace(replace(replace(convert(varchar(20), getdate(), 120), '-',''),':',''),' ','_') + '.bak'
set @Descricao = 'Backup do dia ' + convert(varchar(20), getdate(),120)
backup database dbListaJogos to disk = @caminho with checksum, description = @Descricao
```
Realizar Backup pelo CMD.
```
sqlcmd -S .\SQLEXPRESS -ddbListaJogos -Q "exec BACKUP_dbListaJogos"
```
Realizar Backup pelo Management Studio.
```
exec BACKUP_dbListaJogos
```
Opcionalmente se desejar automatizar o backup, utilize o Agendador de tarefas do próprio Windows junto a um arquivo .bat conforme os parâmetros abaixo. Edite os caminhos das pastas conforme a sua escolha. Necessário ter instalado [7-Zip](https://www.7-zip.org/download.html) para compactação.
```cmd
@echo Iniciando Processo de Backup do Banco de Dados, aguarde...
@echo Transferindo Backup, aguarde...
@d:
@cd\Backups
@move *.7Z "D:\Backups\Backup_Anterior"

@echo Iniciando Backup, aguarde...
@sqlcmd -S .\SQLEXPRESS -ddbListaJogos -Q "exec BACKUP_dbListaJogos"

@echo Compactando Backup, aguarde...
For %%f in (*.bak) do ("C:\Program Files\7-Zip\7z.exe" a "%%~nf.7Z" "%%f" -sdel)

@echo Backup Efetuado com Sucesso!

@echo Apagando Backup antigo com mais de 30 dias, aguarde...
forfiles -p "D:\Backups\Backup_Anterior" -s -d -30 -m *.7Z -c "cmd /c del /f /q @path"

@exit
```
