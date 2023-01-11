/*
  Warnings:

  - A unique constraint covering the columns `[listing_url]` on the table `Listing` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "Listing_listing_url_key" ON "Listing"("listing_url");
