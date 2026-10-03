INSERT INTO users (name, email)
VALUES
    ('John Smith', 'john@example.com'),
    ('Anna Johnson', 'anna@example.com'),
    ('David Brown', 'david@example.com'),
    ('Emily Wilson', 'emily@example.com');

INSERT INTO accounts (user_id, account_number, balance)
VALUES
    (1, '100001', 1500.00),
    (1, '100002', 500.00),
    (2, '100003', 2500.00),
    (3, '100004', 750.00),
    (4, '100005', 3200.00);

INSERT INTO transactions (account_id, transaction_type, amount)
VALUES
    (1, 'DEPOSIT', 1000.00),
    (1, 'WITHDRAWAL', 100.00),
    (2, 'DEPOSIT', 500.00),
    (3, 'DEPOSIT', 2000.00),
    (3, 'TRANSFER_IN', 200.00),
    (4, 'TRANSFER_OUT', 200.00),
    (5, 'DEPOSIT', 750.00);