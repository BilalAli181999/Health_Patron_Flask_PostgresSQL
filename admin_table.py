import psycopg2


class admin_table:
    conn=''
    cur=''
    def __init__(self):
        self.conn = psycopg2.connect(database="d8p1th5vv9dmeu", user="lumlcggnjdaumc", password="f276602e62d3bea9ed337e0d364be3d052e5649d1efacf7b8cbdbcc468970929", host="ec2-54-221-201-212.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()





    def getUser(self):
        self.cur.execute("select username from admin")
        res=self.cur.fetchall()
        return res[0][0]

    def getPassword(self):
        self.cur.execute("select password from admin")
        res=self.cur.fetchall()
        return res[0][0]


    def setUser(self,username,password):
        query="UPDATE admin set username = '"+username+"' ,"+"password = '" + password + "' where id=1"

        self.cur.execute(query)

        self.conn.commit()




    def closeConnection(self):
        self.conn.close()