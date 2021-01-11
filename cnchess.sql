/* Creating database */
CREATE  DATABASE IF NOT EXISTS  cnchess;
/* Selecting database */
USE cnchess;

DROP TABLE IF EXISTS chess_qipu;

/* admin table */
create table chess_qipu
(
    id                  BIGINT              NOT NULL,
    title               VARCHAR(255)        DEFAULT "无",
    binit               VARCHAR(80)         DEFAULT "",
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
