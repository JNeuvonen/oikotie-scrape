/*
  Warnings:

  - You are about to drop the column `full_address` on the `Listing` table. All the data in the column will be lost.
  - Added the required column `address` to the `Listing` table without a default value. This is not possible if the table is not empty.
  - Added the required column `year` to the `Listing` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Listing" DROP COLUMN "full_address",
ADD COLUMN     "address" TEXT NOT NULL,
ADD COLUMN     "year" DOUBLE PRECISION NOT NULL;
