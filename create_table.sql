CREATE TABLE repo_info(
   id SERIAL PRIMARY KEY,
   name VARCHAR (256) NOT NULL,
   username VARCHAR (256) NOT NULL,
   html_url VARCHAR (512),
   description VARCHAR,
   private boolean,
   created_at date,
   watchers INTEGER
)
