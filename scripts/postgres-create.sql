-- Databricks notebook source
CREATE TABLE store (
     "Id" integer not null PRIMARY KEY, 
     "Name" varchar(40) NOT NULL, 
     "City" varchar(40), 
     "State" varchar(40), 
     "Country" varchar(40), 
     "Active" varchar(40)
);
INSERT INTO store VALUES (1, 'Store-A', 'New York', 'New York', 'USA', 1);
INSERT INTO store VALUES (2, 'Store-B', 'Washington', 'Seattle', 'USA', 1);
INSERT INTO store VALUES (3, 'Store-C', 'Dallas', 'Texas', 'USA', 1);

CREATE TABLE item (
     "Id" integer not null PRIMARY KEY, 
     "Name" varchar(40) NOT NULL, 
     "Desc" varchar(40), 
     "Active" varchar(40)
);
INSERT INTO item VALUES (1, 'Bananas', 'Bananas', '1');
INSERT INTO item VALUES (2,'Apples','Gala Apples','1');
INSERT INTO item VALUES (3, 'Organes', 'Naval Oranges', '1');

CREATE TABLE transaction (
     "TId" integer not null PRIMARY KEY, 
     "StoreId" integer NOT NULL, 
     "ItemId" integer not null, 
     "TDesc" varchar(40),
     "TDate" date not null DEFAULT CURRENT_DATE
);
INSERT INTO transaction VALUES (1, 1, 2, 'Apples for StoreB@WAS', '2021-04-19');
INSERT INTO transaction VALUES (2, 3, 3, 'Oranges for StoreC@DAL', '2021-04-18');
INSERT INTO transaction VALUES (3, 2, 1, 'Bananas for StoreA@NYC', '2021-04-17');
