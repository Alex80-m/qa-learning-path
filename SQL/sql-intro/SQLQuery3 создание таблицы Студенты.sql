CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    f_name VARCHAR(50),
    l_name VARCHAR(50),
    Vozrast INT,
    facultet VARCHAR(50),
    kurs INT
);

INSERT INTO Students VALUES
(1, 'Иван', 'Иванов', 20, 'Информатика', 2),
(2, 'Петр', 'Петров', 19, 'Математика', 1),
(3, 'Анна', 'Сидорова', 21, 'Физика', 3),
(4, 'Мария', 'Кузнецова', 22, 'Химия', 4),
(5, 'Алексей', 'Смирнов', 20, 'Биология', 2);