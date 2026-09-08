'''import sqlite3
conn=sqlite3.connect("sqlite.db")

conn.execute('''
'''Create table student1
(
student1_id  int primary key,
student1_name  varchar(50),
student1_class  char(50),
student1_email  varchar(50)
)'''
''')
conn.close()'''



import sqlite3
conn=sqlite3.connect("sqlite.db")

ins=('''insert into student1(student1_id,student1_name,student1_class,student1_email)
values(2,"Himanshu Jaat","Btech","abc@gmail.com")''')
conn.execute("DELETE FROM student1 WHERE student1_id=1")
conn.commit()
conn.close()



'''import sqlite3
conn=sqlite3.connect("sqlite.db")
data=conn.execute("Select * from student1")
print("student1_id","student1_name","student1_class","student1_email")
for n in data:
    print(n)

conn.commit()
conn.close()'''



