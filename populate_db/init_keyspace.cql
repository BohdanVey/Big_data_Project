// docker run -it --network cassandra-network1 --rm cassandra cqlsh node1


CREATE KEYSPACE wiki_keyspace WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
USE wiki_keyspace;


// task 1:

CREATE TABLE unique_domains (
   page_domain text,
   PRIMARY KEY (page_domain)
);


// task 2:

CREATE TABLE pages_by_user (
   user_id int,
   page_id int,
   page text,

   PRIMARY KEY (user_id, page_id)
);


// task 3: COUNTER TABLE
CREATE TABLE articles_by_domain (
   domain text,
   articles_num counter,
   PRIMARY KEY (domain)
);


// task 4:

CREATE TABLE page_by_id (
   page_id int,
   page text,
   PRIMARY KEY (page_id)
);

// task 5:

CREATE TABLE created_pages_time (
   user_id int,
   page_id int,
   user_text text,
   time_created timestamp,
   PRIMARY KEY (user_id, time_created, page_id)
)
WITH CLUSTERING ORDER BY (time_created ASC);
