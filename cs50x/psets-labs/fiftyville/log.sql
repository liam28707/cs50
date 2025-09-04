-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT
  description
FROM
  crime_scene_reports
WHERE
  street = 'Humphrey Street';

-- Theft took place on 28th July,2021 at
--10:15am at the H street (Emma's)bakery. Three witness's interviews
SELECT
  transcript
FROM
  interviews
WHERE
  MONTH = '7'
  AND DAY = '28'
  AND YEAR = '2021';

--Thief got into car in parking lot
-- and drove away. Witness #2 saw thief withdraw money from atm on legget street. Witness #3 overheard the thief talking
--to someone about taking the earliest flight out of fiftyville and for less than a minute. Reciever's end of the phone was asked to purchase the
--flight ticket.
SELECT
  *
FROM
  atm_transactions
WHERE
  DAY = '28'
  AND MONTH = '7'
  AND YEAR = '2021'
  AND atm_location = 'Leggett Street';

--
--9 transaction on that day of which 8 were withdrawals and ranged from  10 $  - 80 $
SELECT
  *
FROM
  airports;

--FIftyville rgional airport has id = 8
SELECT
  *
FROM
  flights
WHERE
  origin_airport_id = 8
  AND DAY = 28;

--Earliest flight at 8:20 to airport id = 4 and flight id = 36
--which is the airport in New York City (Reran previous command)
SELECT
  *
FROM
  bakery_security_logs
WHERE
  YEAR = 2021
  AND MONTH = 7
  AND DAY = 28
  AND HOUR = 10;

--bankid's 264,266,267,269 withdrew money from leggett street and exited in a car at the 10th hour from the bakery
SELECT
  *
FROM
  bank_accounts
WHERE
  account_number LIKE '282%';

--id 264 has account 28296815 and creation year 2014 and id 395717
--Similarly id 266 has '' 76054385 and '' 2015 and '' 449774
--          id 267 has '' 49610011 and '' 2010 and '' 686048
--          id 269 has '' 16153065 and '' 2012 and '' 458378
SELECT
  *
FROM
  people
WHERE
  id = 395717;

--id 264 is Kenny and passport number 9878712108 and plate 30G67EN;
--Similarly id 266 is Taylore and '' 1988161715 and '' 1106N58;
--          id 267 is Bruce and '' 5773159633 and '' 94KL13X; From Security Logs this car left almost immediately within 10 mins of theft
--          id 269 is Brooke and '' 4408372428 and '' QX4YZN3;
SELECT
  *
FROM
  passengers
WHERE
  flight_id = 36;

-- Bruce's passport number is there in the list of passenegers to the earlist flight out of Fiftyville with seat 4A.
SELECT
  *
FROM
  people
WHERE
  name = 'Bruce';

-- Retrieved Phone Number. (367) 555-5533
SELECT
  *
FROM
  people
WHERE
  phone_number = (375) 555 -8161;

--Its Robin with this number and with a conversation of less than a minute
--Therefore she is the accomplice.