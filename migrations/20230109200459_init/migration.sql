-- CreateTable
CREATE TABLE "Listing" (
    "ID" SERIAL NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3),
    "price" DOUBLE PRECISION NOT NULL,
    "price_to_sqm" DOUBLE PRECISION,
    "full_address" TEXT NOT NULL,
    "city" TEXT NOT NULL,
    "neighborhood" TEXT NOT NULL,
    "square_meters" DOUBLE PRECISION,
    "rooms" DOUBLE PRECISION NOT NULL,
    "apartment_type" TEXT NOT NULL,
    "listing_url" TEXT NOT NULL,

    CONSTRAINT "Listing_pkey" PRIMARY KEY ("ID")
);
