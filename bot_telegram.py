from pyrogram import Client


def cria_session_bot():
    """
    Cria o session do bot, evitando autenticação posterior
    retorna arquivo.session, após criado, não há necessidade e chamar essa função novamente
    """
    # https: // docs.pyrogram.org / start / setup
    api_id = "x"
    api_hash = "x"

    bot_token = "x"

    app = Client(
        "my_bot",
        api_id=api_id, api_hash=api_hash,
        bot_token=bot_token
    )

    app.run()


def enviar_msg_telegram(usuario, msg):
  """Utiliza o arquivo. session"""
    app = Client("my_bot")
    if usuario is not None:
        async def envio():
            async with app:
                await app.send_message(usuario, msg)

        app.run(envio())
    else:
        pass


def enviar_msg_telegram_my_account(usuario, msg):
    app = Client("my_account")

    if usuario is not None:
        async def envio():
            async with app:
                await app.send_message(usuario, msg)

        app.run(envio())
    else:
        pass


def enviar_arquivo_channel(usuario, documento):
    app = Client("my_bot")
    if usuario is not None:
        async def envio():
            async with app:
                await app.send_document(chat_id=usuario, document=documento)

        app.run(envio())
    else:
        pass


def main():
    
    #enviar_arquivo_channel('Mariano', 'BCG_TESTE.pdf')


if __name__ == '__main__':
    main()
