import asyncio
from prisma import Prisma
from prisma.models import Listing


async def main() -> None:

    db = Prisma(auto_register=True)

    await db.connect()
    await Listing.prisma().delete_many({})

if __name__ == '__main__':
    asyncio.run(main())
