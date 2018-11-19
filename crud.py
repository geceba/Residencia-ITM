class CRUD:
    

    def insert(con, ticket, name):
        ticket = (ticket, name)
        con.execute("INSERT INTO tickets (name, full_name) VALUES (?,?)", ticket)
        con.commit()
        con.close()

    def select(con):
        for row in con.execute("SELECT name FROM tickets"):
            print(row)
    
    def delete(con, name):
        con.execute("DELETE FROM tickets WHERE name=?", name)
        con.commit()
        con.close()
    
  

