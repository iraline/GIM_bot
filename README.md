
# GIMBot

GIMBot é um bot para o telegram,
onde com ele é possível verificar 
se um perfil do twitter é ou não é um bot. O GIMBot 

# Sobre o projeto

O GIMBot foi desenvolvido utilizando Python. Para verificar se um perfil
do twitter é ou não um bot, uma requisição é enviada para o site 
[Pegabot](https://pegabot.com.br). 
Atualmente o bot não está hospedado em servidores. 

## Configurando o ambiente

Pré-requisitos: Conta no Telegram, Python (>=3.6)

### Instalando Pacotes
 `pip install pytelegrambotapi`

### Criando bot no telegram
No seu telegram:

1. Procure por @BotFather. Este bot é quem cria e gerencia os seus bots.
2. Envie uma mensagem para o @BotFather e aguardar o retorno com as opções.
3. Selecione a opção /newbot.
4. Insira o nome e username do seu bot. O username deve ser único e terminar com bot.
5. Crie o arquivo config.py com o conteúdo do configExample.py
6. Copie a chave API gerada pelo @BotFather e insira como valor na variável TELEGRAM_API_KEY do config.py.

### Rodando o bot
 `python botTelegram.py `

## Como usar o bot
Com o código rodando em sua máquina:

1. Pesquise pelo seu bot no telegram.
2. Mande uma mensagem
3. Caso queira saber se o perfil `fulano` é um bot, basta inserir `/analisar fulano`.
4. Caso queira saber se o perfil `fulano` e `sicrano` são bots, basta inserir `/analisar fulano sicrano`.

