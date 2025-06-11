def register(add_command):
    async def echo(event, arg, config):
        await event.reply(arg or "Echo!")
    add_command('echo', echo)
