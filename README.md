# WebRace
sql komennot:

CREATE DATABASE projektipeli;
USE projektipeli;
source path/to/lp.sql
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE game;
DROP TABLE goal;
DROP TABLE goal_reached;
SET FOREIGN_KEY_CHECKS = 1;
  create table game
  (
      id           int auto_increment
          primary key,
      location     varchar(10) null,
      screen_name  varchar(40) null,
      player_range int         null
  )
   charset = latin1;
grant select, insert, update, delete on projektipeli.* to projekti@localhost;