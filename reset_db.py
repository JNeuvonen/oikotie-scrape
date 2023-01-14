import asyncio
from prisma import Prisma
from prisma.models import Listing
from prisma.models import PriceChange


async def main() -> None:

    db = Prisma(auto_register=True)

    await db.connect()
    await Listing.prisma().delete_many({})
    await PriceChange.prisma().delete_many({})
    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
