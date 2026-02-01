CREATE DATABASE IF NOT EXISTS social_dashboard;

USE social_dashboard;

CREATE TABLE IF NOT EXISTS tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tweet TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL
);

select count(*) from tweets;

select * from tweets order by created_at desc;


