class CRUD:
    

    def insert(con, ticket, name):
        ticket = (ticket, name)
        con.execute("INSERT INTO tickets (name, full_name) VALUES (?,?)", ticket)
        con.commit()
        con.close()

    def select(con):
        lista_nombres = []
        for row in con.execute("SELECT * FROM tickets"):
            lista_nombres.append(row[0])
        
        return lista_nombres
    
    def delete(con, name):
        sql = 'DELETE FROM tickets WHERE name=?'
        cur = con.cursor()
        cur.execute(sql, (name,))
        con.commit()
    
  

