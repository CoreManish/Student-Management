from flask import Flask, render_template,request,redirect,url_for
import sqlite3

app=Flask(__name__)

@app.route('/')
def index():
  conn=sqlite3.connect("college.db")
  cur=conn.cursor()

  #select data from table
  cur.execute("SELECT * FROM student")

  #fetch rows
  rows=cur.fetchall()

  cur.close()
  conn.close()
  return render_template('index.html',rows=rows)

@app.route('/add',methods=['GET','POST'])
def add():
  if request.form:
    roll=request.form['roll']
    fname=request.form['fname']
    lname=request.form['lname']
    email=request.form['email']
    
    conn=sqlite3.connect("college.db")
    cur=conn.cursor()

    #insert
    cur.execute("INSERT INTO student(roll,fname,lname,email) VALUES(?,?,?,?)",(roll,fname,lname,email))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index'))
  return render_template('add.html')

@app.route('/delete/<int:roll>')
def delete(roll):
  roll=str(roll)
  conn=sqlite3.connect("college.db")
  cur=conn.cursor()

  cur.execute("DELETE FROM student WHERE roll=?",(roll))
  conn.commit()
  cur.close()
  conn.close()
  return redirect(url_for('index'))

@app.route('/update/<int:roll>',methods=['GET','POST'])
def update(roll):
  roll=str(roll)
  if request.form:
    fname=request.form['fname']
    lname=request.form['lname']
    email=request.form['email']

    con=sqlite3.connect("college.db")
    cur=con.cursor()

    cur.execute("UPDATE student SET fname=?,lname=?,email=? WHERE roll=?",(fname,lname,email,roll))
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for('index'))

  conn=sqlite3.connect("college.db")
  cur=conn.cursor()
  
  #select data from table
  cur.execute("SELECT * FROM student WHERE roll=?",(roll,))
  
  #fetch rows
  rows=cur.fetchmany(size=1)
  
  return render_template('update.html',roll=roll,rows=rows)

if __name__=="__main__":
  app.run(host='0.0.0.0',port=8080,debug=True) # configured for repit.com
