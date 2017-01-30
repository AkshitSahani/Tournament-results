-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--Make sure there already isn't a database with the same name--
drop database if exists tournament;

--Create a database called tournament--
create database tournament;

--Connect to the database created--
\c tournament;

--Create a table for players that assigns them a unique id and enters their names--
create table players(
  id serial primary key,
  name text
);

--Create a table called matches that assigns a match id and stores the winner and loser id--
create table matches(
  match_id serial primary key,
  winner_id integer references players(id),
  loser_id integer references players(id)
);
