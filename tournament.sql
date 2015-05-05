-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- Author: Chad Hickenbottom
-- Nano Degree: Full Stack Web Developer
-- Tournament.sql: Version 1.0
-- About: Tournament sql provides the comands to create the tables needed for a SwissStyle Tournament

--TABLES:
-- 	player: only holds the name and unique id of the player. No other information is needed from players
-- 	record: Record is the win, lose, draw record of each play. 
--			NOTE: A player is not referenced in record that will be done later in player_record
-- 	tournament: holds the name of the tournament, the location the tournament is held as a test and also the end and beginning date the tournament is held
-- 	player_record: references the player that players record and the a reference to the tournament. This allows for players to compete in multiple tournaments.
-- 	game: a game holds a reference to two players who played against each other during a tournament.

create table player (player_id serial unique primary key, player_name text);

create table tournament (tournament_id serial unique primary key not null, name text, location text, tournament_begin_date date, tournament_end_date date);

create table record (player_id serial references player, tournament_id serial references tournament, wins integer DEFAULT 0, loses integer DEFAULT 0, draws integer DEFAULT 0);

create table game (player_1 serial references player(player_id), player_2 serial references player(player_id), tournament_id serial references tournament, winner text, loser text);