-- 1. Create table loyalty_program
CREATE TABLE loyalty_program
    (cust_id INT,
    fname STRING,
    lname STRING,
    email STRING,
    loyalty_level STRING,
    phone_number MAP<STRING, STRING>,
    past_orders ARRAY<INT>,
    orders_summary STRUCT<minimum: INT,
                          maximum: INT,
                          average: FLOAT,
                          TOTAL: INT>        
    )
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':';

-- 2. Load data into Hive
LOAD DATA INPATH '/user/hive/warehouse/dualcore.db/loyalty_program/loyalty_data.txt'
    INTO TABLE loyalty_program;

-- 3. Select home phone number from customer 1200866
SELECT  phone_number["HOME"]
    FROM    loyalty_program
    WHERE   cust_id = 1200866;
-- 408-555-4914

-- 4. Select 3rd element of order IDs from customer 1200866
SELECT  past_orders[2]
    FROM    loyalty_program
    WHERE   cust_id = 1200866;
-- 5278505

-- 5. Number of products bought by customer 1071189
SELECT  count(d.prod_id)
    FROM    customers c
    JOIN    orders o
        ON  (c.cust_id = o.cust_id)
    JOIN    order_details d
        ON  (o.order_id = d.order_id)
    WHERE   c.cust_id = 1071189;
-- 20

-- 6. Number of customers who spent more than 300000 total ????
SELECT  c.cust_id
    FROM    customers c
    JOIN    orders o
        ON  (c.cust_id = o.cust_id)
    JOIN    order_details d
        ON  (o.order_id = d.order_id)
    JOIN    products p
        ON (d.prod_id = p.prod_id)
    GROUP BY c.cust_id
    HAVING   sum(p.price) > 300000;

-- 7. Customers who have not placed an order
SELECT  c.cust_id
    FROM        customers c
    LEFT JOIN   orders o
        ON (c.cust_id = o.cust_id)
    WHERE       o.cust_id IS NULL;

-- 8. Product with lowest average rating from
-- products with at least 50 ratings
SELECT  prod_id
    FROM        ratings
    GROUP BY    prod_id
    HAVING      count(rating) > 50
    ORDER BY    avg(rating) ASC
    LIMIT 1;
-- 1274673

-- 9. Five most common trigrams from rating messages
SELECT  EXPLODE(NGRAMS(SENTENCES(LOWER(message)), 3, 5))
    AS      trigrams
    FROM    ratings
    WHERE   prod_id = 1274673;

-- 10. Messages that contain "ten times more"
SELECT  message
    FROM    ratings
    WHERE   prod_id = 1274673
        AND message LIKE '%ten times more%';