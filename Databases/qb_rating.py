# Simple Python <--> MySQL Examples

import mysql.connector

def qb_rating():
   conn = mysql.connector.connect (user="root", database='Football')
   cursor = conn.cursor ()
   
   l = []
   for x in range(1960, 1978):
      query = "SELECT * FROM Seasons where `year` = "+`x`+" and pass_attempts > 191"
      cursor.execute (query)
      qbs = cursor.fetchall ()
      average = 0
      count = 0
      for row in qbs:
       r = row[0].encode("utf-8")
       query = "select count(*) from Seasons where id = "+`r`+"and `year` = "+ `row[1]`
       cursor.execute (query)
       c = cursor.fetchone ()
       if (c[0] > 1):
          a = 1
       else:
          query = "select qb_rating_season("+`r`+", "+`row[1]`+")"
          cursor.execute(query)
          rating = cursor.fetchone ()
          average += rating[0]
          count += 1
      average = average/count
      l.append(average)

   for x in range(1978, 2009):
      query = "SELECT * FROM Seasons where `year` = "+`x`+" and pass_attempts > 255"
      cursor.execute (query)
      qbs = cursor.fetchall ()
      average = 0
      count = 0
      for row in qbs:
       r = row[0].encode("utf-8")
       query = "select count(*) from Seasons where id = "+`r`+"and `year` = "+ `row[1]`
       cursor.execute (query)
       c = cursor.fetchone ()
       if (c[0] > 1):
          a = 1
       else:
          query = "select qb_rating_season("+`r`+", "+`row[1]`+")"
          cursor.execute(query)
          rating = cursor.fetchone ()
          average += rating[0]
          count += 1
      average = average/count
      l.append(average)

   for i in l:
      print i
      
   cursor.close ()
   conn.close ()

