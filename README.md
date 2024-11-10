create a database in mysql called "pongscores"
create a table in the database:
CREATE TABLE scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player1 INT NOT NULL,
    player2 INT NOT NULL,
    winner VARCHAR(10)
);
