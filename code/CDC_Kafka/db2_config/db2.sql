-- Create a table
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    department VARCHAR(50)
);

-- Insert dummy values into the table
INSERT INTO employees (id, name, age, department) VALUES
(1, 'John Doe', 30, 'IT'),
(2, 'Jane Smith', 25, 'HR'),
(3, 'Michael Johnson', 35, 'Finance'),
(4, 'Emily Brown', 28, 'Marketing');