-- Вставка данных в таблицу "Рейсы самолетов"
INSERT INTO Flights (flight_id, flight_number, departure_date, arrival_date, origin, destination)
VALUES
    (201, 'XYZ789', '2023-09-04T10:00:00', '2023-09-04T12:00:00', 'Moscow', 'Berlin'),
    (202, 'LMN012', '2023-09-05T14:00:00', '2023-09-05T17:00:00', 'Los Angeles', 'Sydney'),
    (203, 'OPQ345', '2023-09-06T08:00:00', '2023-09-06T10:00:00', 'London', 'Paris');
    -- ... добавьте еще рейсы ...

-- Вставка данных в таблицу "Пассажиры"
INSERT INTO Passengers (passenger_id, first_name, last_name, birthdate, gender)
VALUES
    (301, 'Alexander', 'Miller', '1982-04-10', 'Male'),
    (302, 'Emma', 'Johnson', '1998-08-22', 'Female'),
    (303, 'Noah', 'Williams', '1995-11-30', 'Male');
    -- ... добавьте еще пассажиров ...

-- Вставка данных в таблицу "Билеты на рейсы"
INSERT INTO Tickets (ticket_id, flight_id, passenger_id, class, seat_number, price)
VALUES
    (401, 201, 301, 'Business', 'A1', 300.00),
    (402, 202, 302, 'Economy', 'B2', 180.00),
    (403, 203, 303, 'Economy', 'C3', 200.00);
    -- ... добавьте еще билеты ...

-- Продолжайте добавлять еще значения по аналогии

-- Вставка данных в таблицу "Рейсы самолетов"
INSERT INTO Flights (flight_id, flight_number, departure_date, arrival_date, origin, destination)
VALUES
    (204, 'RST678', '2023-09-07T12:00:00', '2023-09-07T14:00:00', 'Berlin', 'Paris'),
    (205, 'UVW901', '2023-09-08T16:00:00', '2023-09-08T18:00:00', 'New York', 'London');
    -- ... добавьте еще рейсы ...

-- Вставка данных в таблицу "Пассажиры"
INSERT INTO Passengers (passenger_id, first_name, last_name, birthdate, gender)
VALUES
    (304, 'Sophia', 'Brown', '1991-03-25', 'Female'),
    (305, 'Liam', 'Davis', '1988-07-15', 'Male');
    -- ... добавьте еще пассажиров ...

-- Вставка данных в таблицу "Билеты на рейсы"
INSERT INTO Tickets (ticket_id, flight_id, passenger_id, class, seat_number, price)
VALUES
    (404, 204, 304, 'Economy', 'D4', 220.00),
    (405, 205, 305, 'Business', 'E5', 350.00);
    -- ... добавьте еще билеты ...
