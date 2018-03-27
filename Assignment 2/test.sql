--CS457 PA2

--Construct the database and table (0 points; expected to work from PA1)
CREATE DATABASE CS457_PA2;
USE CS457_PA2;
CREATE TABLE Product (pid int, name varchar(20), price float);

--Insert new data (20 points)
insert into Product values(1,	'Gizmo',      	19.99);
insert into Product values(2,	'PowerGizmo', 	29.99);
insert into Product values(3,	'SingleTouch', 	149.99);
insert into Product values(4,	'MultiTouch', 	199.99);
insert into Product values(5,	'SuperGizmo', 	49.99);

.EXIT
