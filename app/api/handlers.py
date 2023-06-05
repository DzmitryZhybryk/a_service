from app.api.services import AuthenticationStorage


class AuthenticationHandlers:

    def __init__(self, storage: AuthenticationStorage):
        self.__services = storage

    async def test(self):
        await self.__services.test1()
