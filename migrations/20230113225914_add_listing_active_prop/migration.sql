/*
  Warnings:

  - Added the required column `sale_active` to the `Listing` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Listing" ADD COLUMN     "sale_active" BOOLEAN NOT NULL;
