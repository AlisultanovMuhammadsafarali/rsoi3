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


{
    user1: {entry {
            title: first commit
            text: hello
        },
        {
            title: second commit
            text: good bye
        }
    }
    user2: {entry {
    
    }}
}

{
    "access_token": "795156847770844656013266777576721532",
    "expire_in": 1800,
    "refresh_token": "824852751320777686770634749190463825",
    "token_type": "bearer"
}