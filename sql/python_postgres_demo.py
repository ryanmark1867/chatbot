# Install psycopg2 using pip.

#  pip install psycopg2

# postgres
# id: postgres
# pw: Anglos2u!

import psycopg2

try:
   connection = psycopg2.connect(user="postgres",
                                  password="<>",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
   cursor = connection.cursor()
   postgreSQL_select_Query = "select * from streetcarjan2014 limit 20"

   cursor.execute(postgreSQL_select_Query)
   print("Selecting rows from streetcarfeb2014 table using cursor.fetchall")
   mobile_records = cursor.fetchall() 
   
   print("Print each row and it's columns values")
   for row in mobile_records:
       print("Route = ", row[0], )
       print("Day = ", row[3])
       print("Incident  = ", row[5], "\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()