import psycopg2


class app_table:
    conn=''
    cur=''
    def __init__(self):
        self.conn = psycopg2.connect(database="d8p1th5vv9dmeu", user="lumlcggnjdaumc", password="f276602e62d3bea9ed337e0d364be3d052e5649d1efacf7b8cbdbcc468970929", host="ec2-54-221-201-212.compute-1.amazonaws.com", port="5432")
        self.cur = self.conn.cursor()




    def getAll(self):
        self.cur.execute("select * from appointments")
        res=self.cur.fetchall()
        return res

    def getSpecific(self, id):
        self.cur.execute("select * from appointments where aid= '"+id+"'")
        res=self.cur.fetchall()
        return res[0]


    def addAppointment(self,username,phone,gender,age,address,email,type):
        query="INSERT INTO appointments (fullName,phoneNo,gender,age,address,email,appType) VALUES ( '"+username+"','"+phone+"','"+gender+"','"+age+"','"+address+"','"+email+"','"+type+"')";
        self.cur.execute(query);
        self.conn.commit()


    def deleteAppointment(self,id):
        query = "delete from appointments where aid="+id
        self.cur.execute(query);
        self.conn.commit()







    def closeConnection(self):
        self.conn.close()