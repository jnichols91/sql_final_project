/*
 *  Copy the data from the .csv files into the database. This will create the tables and
 *  then imoprt the data for level one eco regions and fire data
 *
 *  author: Justin Nichols
 *
 */

 DROP TABLE IF EXISTS fires, regions;

 CREATE TABLE regions(
   fpa_id text PRIMARY KEY,
   state char(2),
   eco_id integer,
   eco_region text
 );

 CREATE TABLE fires(
   fpa_id text PRIMARY KEY,
   fire_name text,
   discovery_time integer,
   stat_cause_code integer,
   stat_cause_descr text,
   cont_time integer,
   fire_size decimal,
   fire_size_class char(1),
   latitude decimal,
   longitude decimal,
   state char(2),
   county text,
   disc_date date,
   cont_date date,
   season text,
   human integer
 );

 \COPY regions FROM '../data/eco_regions.csv' DELIMITER ',' CSV HEADER
 \COPY fires FROM '../data/fires.csv' DELIMITER ',' CSV QUOTE '"' HEADER NULL 'NA'
