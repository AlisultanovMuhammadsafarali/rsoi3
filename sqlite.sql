drop table if exists Entries;
create table Entries (
  entry_id integer primary key autoincrement,
  user_fk integer not null,
  title text not null,
  text text not null
);


drop table if exists Session1;
create table Session1 (
    sess_id integer primary key autoincrement,
    user_id integer not null,
    key text not null,
    expire datetime not null
);


