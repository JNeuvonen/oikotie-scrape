/*
  Warnings:

  - You are about to drop the column `listing_url` on the `Listing` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[url]` on the table `Listing` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `url` to the `Listing` table without a default value. This is not possible if the table is not empty.

*/
-- DropIndex
DROP INDEX "Listing_listing_url_key";

-- AlterTable
ALTER TABLE "Listing" DROP COLUMN "listing_url",
ADD COLUMN     "url" TEXT NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "Listing_url_key" ON "Listing"("url");
