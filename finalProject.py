#!/usr/bin/python
#
# "she-bang" line is a directive to the web server: where to find python
#
# filename: finalProject.py
# description: A web application to help peole share their class notes online.
# Uses Python 2.7, Twitter Bootstrap for the front end, and MySQL for storage.
# Final Project for CS108 - Dynamic Web Applications Class

# Author: Sua Morales
# smorales@bu.edu

##import the libs. 
import MySQLdb
import time
import cgi
import cgitb; cgitb.enable()
import os


print "Content-Type: text/html; charset=utf-d\n\n"
print "" # blank line

################################################################################
def getConnectionAndCursor():
    """
    This function will connect to the database and return the
    Connection and Cursor objects.
    """ 
    # connect to the MYSQL database
    conn = MySQLdb.connect(host="localhost",
                      user="root",
                      passwd="",
                      db="collab")

    cursor = conn.cursor()
    return conn, cursor
 
################################################################################
def doHTMLHead(title):
    """
    Write HTML header. Manually includes Twitter bootstrap for front-end design.
    """

    #print heading
    print """
    <html>
    <head>
    
    <title>%s</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Bootstrap core CSS -->
    <link href="http://localhost/collab_css/css/bootstrap.css" rel="stylesheet">

    <!-- Custom CSS for the 'Heroic Features' Template -->
    <link href="http://localhost/collab_css/css/heroic-features.css" rel="stylesheet">
    </head>

    
    <body>
    <h1><a href = "./finalProject.py">%s</a></h1>    
    """ % (title, title)


################################################################################
def doHTMLTail():
    """
    Do html tail
    """
    # always show this link to go back to the main page
    print """
     <footer>
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <ul class="list-inline">
                        <li><a href="./finalProject.py">Home</a>
                        </li>
                        <li class="footer-menu-divider">&sdot;</li>
                        <li><a href="./finalProject.py/about.html">About</a>
                        </li>
                        <li class="footer-menu-divider">&sdot;</li>
                        <li><a href="./finalProject.py/contact.html">Contact</a>
                        </li>
                    </ul>
                    <p class="copyright text-muted small">Copyright &copy; Sua Morales 2015. All Rights Reserved</p>
                    <p class="copyright text-muted small">This page was generated at %s.</p>
                </div>
            </div>
        </div>
    </footer>
    </body>
    </html>

    """ % time.ctime()

################################################################################
def debugFormData(form):
    """
    A helper function which will show us all of the form data that was
    sent to the server in the HTTP form.
    """
    
    
    print """
    <h2>DEBUGGING INFORMATION</h2>
    <p>
    Here are the HTTP form data:
    """
    print """
    <table border=1>
        <tr>
            <th>key name</th>
            <th>value</th>
        </tr>
    """
    
    # form behaves like a python dict
    keyNames = form.keys()
    # note that there is no .values() method -- this is not an actual dict

    ## use a for loop to iterate all keys/values
    for key in keyNames:

        ## discover: do we have a list or a single MiniFieldStorage element?
        if type(form[key]) == list:

            # print out a list of values
            values = form.getlist(key)
            print """
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
            """ % (key, str(values))

        else:
            # print the MiniFieldStorage object's value
            value = form[key].value
            print """
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
            """ % (key, value)
        
    print """
    </table>
    <h3>End of HTTP form data</h3>
    <hr>
    """

## end: def debugFormData(form)
    

################################################################################

def getAllClasses():
    """
    Middleware function to get all classes in "classes" table.
    """

    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT *
    FROM classes
    """

    # execute the query
    cursor.execute(sql)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data

## end: def getAllClasses():

##################################################################################

def showAllClasses(data):
    """
    Presentation layer function to display a table containing all classes.
    """
    #pritn nav bar at top

    printNavBar()

    print """
    <table>
    """

    #cycle through tuple and print classes
    for tup in data:
        (idNum, classNum, className, semester, year) = tup
        print """
        <tr>
            <td><a href="?idNum=%s">%s %s %s %s</a></td>
        </tr>
        """ %(idNum, classNum, className, semester, year)


    print"""
    </table>
    """

  
    #print total classes found

    print "<p> Found %d classes <br>" % len(data)

## end: def showAllClasses():

##################################################################################

def getOneClass(idNum):
    
    """
    Middleware function to retrieve info for one class
    """
    
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT *
    FROM classes
    WHERE id=%s
    """

    # execute the query
    parameters = (int(idNum), )
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data

## end: def getOneClass(idNum)



###############################################################################

def getAllDocs(idNum):
    
    """
    Middleware function to retrieve info for one class
    """
    
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT *
    FROM documents
    WHERE class_num = %s
    """

    # execute the query
    parameters = (int(idNum), )
    cursor.execute(sql,parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data

## end: def getAllDocs(idNum)



###############################################################################

def showOneClass(data, docData):
    """
    Presentation layer function to display page for one class.
    """

    printNavBar()
    
    ## show profile information
    (idNum, classNum, className, semester, year) = data[0]
    
    #print the headings
    print """
        <h2> %s </h2
        <p>
        <p>
        <h3> User Notes </h3>
    """%className

    #print all docs for class
    
    for tup in docData:
        (docId,date,url,doc_name,rating,class_num) = tup

        print """
        
        <a href = "%s">%s</a> <br>
        Rating: %s
        """%(url,doc_name,rating)

    #print the upvote/downvote buttons (actually forms)

        print"""
        <form>
        <table>
            <tr>
            <input type="submit" name="upvote" value="Good Quality">
             <input type = "hidden" name = "class_num" value = %s>
             <input type = "hidden" name = "up" value = 1>
        </form>
            </tr>
        <tr>
        <form>
            <input type="submit" name="downvote" value="Bad Quality">
            <input type = "hidden" name = "class_num" value = %s>
            <input type = "hidden" name = "down" value = -1>        
        </form>
        </tr>
        </table>
        <p>
        <p>

        """%(class_num, class_num)




## end: def showOneClass(data)


################################################################################

def showUploadPage():
    printNavBar()
    ##print nav bar

    ##print different fields and hidden fields to submit form
    print """
       <form enctype="multipart/form-data" method = "POST" action = "./finalProject.py" >
    Date notes/study guide was created <input type = "text">
    <br>
    class name <input type = "text" name ="class_name">
    <br>
    class number (ex. CS101) <input type = "text" name = "class_num">
    <br>
    Semester
          <select name = "semester">
          <option value="Fall">Fall</option>
          <option value="Spring">Spring</option>
          </select>
    <br>
    year <input type = "text" name = "year">
    <br>
    professor <input type = "text" name = "professor">
    <br>
    File Name <input type = "text" name = "fileName">

   
    <input type = "file" accept = "application/pdf" name = "fileUpload" >
    <input type = "submit" name ="finalUpload" value = "Upload Notes"></input>
    </form>
    """
 
##end showUploadPage()
 
################################################################################
    
def voteUpDown(classNum, upOrDown):
    """
    Middleware to update the rating on the document by 1
    """
    # connect to database
    conn, cursor = getConnectionAndCursor()

    sql1 = """
    SELECT rating
    FROM documents
    WHERE class_num = %s
    """
    parameters = (classNum, )
    cursor.execute(sql1,parameters)

    currentRating = cursor.fetchone()
    
    
    # build SQL
    sql2 = """
    UPDATE documents
    SET rating= %s + %s
    WHERE class_num = %s
    """

    # execute the query
    parameters = (int(currentRating[0]),int(upOrDown),classNum )
    cursor.execute(sql2,parameters)

    rowcount = cursor.rowcount
    # clean up
    conn.commit()
    conn.close()
    cursor.close()

    return rowcount


##end voteUpDown(classNum, upOrDown):

################################################################################
def printNavBar():
    #prints nav bar at top of page. Via twitter Bootstrap
    
    print"""

   <nav class="navbar navbar-fixed-top navbar-inverse" role="navigation">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="./finalProject.py?uploadNotes=Upload+Notes">Upload Notes</a>
            </div>
            
            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse navbar-ex1-collapse">
                <ul class="nav navbar-nav">
                    <li><a href="./finalProject.py/about.html">About</a>
                    </li>
                    <li><a href="./finalProject.py/contact.html">Contact</a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>
        """

    ##end printNavBar()
################################################################################

def showFrontPage():
    """
    Show front page of project.
    """
    printNavBar()
    #print nav bar

    
    #show options to display classes or upload doc
    print"""
    <div class="container">

        <div class="jumbotron hero-spacer">
            <h1>Collab: Use notes from those before you</h1>
            <p>Collab helps you study smarter by sharing notes </p>
            <p><a href = "./finalProject.py?showAllClasses=Show+All+Classes%21" class="btn btn-primary btn-large">Show all classes on Collab now</a>
            </p>
        </div>

        <hr>

        <div class="row">
            <div class="col-lg-12">
                <h3>Latest Features</h3>
            </div>
        </div>
        <!-- /.row -->

        <div class="row text-center">

            <div class="col-lg-3 col-md-6 hero-feature">
                <div class="thumbnail">
                    <img src="http://cs-webapps.bu.edu/cs108/smorales/images/studying.jpg" alt="">
                    <div class="caption">
                        <h3>Find your class</h3>
                        <p>Get notes to help make studying more effective</p>
                        <p>
                        <form>
                        <input type="submit" name = "showAllClasses" class="btn btn-primary" value = "Show All Classes!"> 
                        </form>
                        </p>
                    </div>
                </div>
            </div>


            <div class="col-lg-3 col-md-6 hero-feature">
                <div class="thumbnail">
                    <div class="caption">
                        <h3>Upload Notes</h3>
                        <p>You're a helpful person, upload notes by clicking the button below</p>
                        <p>
                        
                        <form>
                        <input type = "submit" name = "uploadNotes" value = "Upload Notes" class = "btn btn-primary" >
                        </form>
                        
                        </p>
                    </div>
                </div>
            </div>


        </div>
        <!-- /.row -->

        <hr>


    </div>
    <!-- /.container -->

    <!-- JavaScript -->
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.js"></script>

"""

##end of showFrontPage():
################################################################################

def addDoc():
    """
    writes doc to directory, to be accessed by user

    """

    ##opens doc
    ##writes binary
    ##closes doc
    fileUpload = form["fileUpload"]
    fileData = fileUpload.value

    file1 = open("/home/course/cs108/smorales/webapps/notes/"+fileUpload.filename, "wb")
    file1.write(fileData)      

        

    file1.close()


##end: addDoc()

################################################################################

def insertDoc(doc_url, doc_name, rating, classID):
    """
    Middleware function to create SQL to insert a doc into the documents table
    """
    
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    INSERT INTO documents (date, doc_url, doc_name, rating, class_num)
    VALUES (%s,%s,%s,%s,%s)
    """

    tm = time.localtime() 
    timestamp = "%04d-%02d-%02d %02d:%02d:%02d" % tm[0:6]


    parameters = (timestamp,doc_url, doc_name, int(rating), int(classID))
    cursor.execute(sql, parameters)


    rowcount = cursor.rowcount

    # clean up
    conn.commit()
    conn.close()
    cursor.close()
    
    return rowcount




## end: insertDoc(doc_url, doc_name, rating, classID)


################################################################################

def insertNewDoc(doc_url, doc_name, rating):
    """
    Middleware function to create SQL to insert a doc into the documents table
    """
    
    # connect to database
    conn, cursor = getConnectionAndCursor()

    firstsql = """
    SELECT MAX(id)
    FROM classes
    """

    cursor.execute(firstsql, )
    newClassID = cursor.fetchone()
    newClassID = int(newClassID[0])+1
    
    
    # build SQL
    sql = """
    INSERT INTO documents (date, doc_url, doc_name, rating, class_num)
    VALUES (%s,%s,%s,%s,%s)
    """

    tm = time.localtime() 
    timestamp = "%04d-%02d-%02d %02d:%02d:%02d" % tm[0:6]


    parameters = (timestamp,doc_url, doc_name, int(rating), int(newClassID))
    cursor.execute(sql, parameters)


    rowcount = cursor.rowcount

    # clean up
    conn.commit()
    conn.close()
    cursor.close()
    
    return rowcount



#insertNewDoc(doc_url, doc_name, rating, classID)

################################################################################

def insertNewClass(classNum, className, semester, year):
    """
    Middleware function to create SQL to insert a doc into the documents table
    """
    
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    INSERT INTO classes (class_num, class_name, semester,year)
    VALUES (%s,%s,%s,%s)
    """

    tm = time.localtime() 
    timestamp = "%04d-%02d-%02d %02d:%02d:%02d" % tm[0:6]


    parameters = (classNum, className, semester, int(year))
    cursor.execute(sql, parameters)


    rowcount = cursor.rowcount

    # clean up
    conn.commit()
    conn.close()
    cursor.close()
    
    return rowcount

##end insertNewClass(classNum, className, semester, year):


################################################################################

## end: def getOneProfile(idNum):
if __name__ == "__main__":

    # get form field data
    form = cgi.FieldStorage()
    doHTMLHead("Collab")

    if "idNum" in form:                 #initial page
        classId = form["idNum"].value
        data = getOneClass(classId)
        docData = getAllDocs(classId)
        showOneClass(data, docData)

    elif "showAllClasses" in form:          #lists all classes in db
        data = getAllClasses()
        showAllClasses(data)

    elif "uploadNotes" in form:         #shows upload page if user submits form
        showUploadPage()

    elif "upvote" in form:              #determies whther a note was upvoted
        class_num = form["class_num"].value
        plusOne = form["up"].value
        rating = voteUpDown(class_num, plusOne)

        #display info
        data = getOneClass(class_num)
        docData = getAllDocs(class_num)
        showOneClass(data, docData)
        print str(rating) + "rows updated"

        
    elif "downvote" in form:            #determies wheter a note was downvoted
        class_num = form["class_num"].value
        minusOne = form["down"].value
        rating = voteUpDown(class_num, minusOne)

        #display info
        data = getOneClass(class_num)
        docData = getAllDocs(class_num)
        showOneClass(data, docData)
        print str(rating) + "rows updated"


    elif "finalUpload" in form:         #after user uploads page, validate the form via client-side validations
        if len(form["fileUpload"].value)==0:
            showUploadPage()
            print"""
            <script = "javascript">
            alert("You did not attach a document. Please try again")
            </script>
            """
            quit()
        elif len(form["class_num"].value)==0:
            showUploadPage()
            print"""
            <script = "javascript">
            alert("You did not attach a document. Please try again")
            </script>
            """
            quit()
        elif len(form["class_name"].value)==0:
            showUploadPage()
            print"""
            <script = "javascript">
            alert("Please fill in class name. Try again")
            </script>
            """
            quit()

        elif len(form["year"].value)==0:
            showUploadPage()
            print"""
            <script = "javascript">
            alert("Please fill in year of class. Try again"")
            </script>
            """
            quit()

        elif len(form["professor"].value)==0:
            showUploadPage()
            print"""
            <script = "javascript">
            alert("Please fill in professor's name. Try again")
            </script>
            """
            quit()

        #add doc
        addDoc()
        fileUpload = form["fileUpload"]
        fileName = fileUpload.filename
        doc_url = "http://cs-webapps.bu.edu/cs108/smorales/notes/"+fileName
        doc_name = form["fileName"].value
        rating = 0
        #set form fields
        class_num = form["class_num"].value
        class_name = form["class_name"].value
        semester = form["semester"].value
        year = form["year"].value

        data = getAllClasses()

    
        for tup in data: 
            if class_num in tup:
                classID = tup[0]
                insertDoc(doc_url, doc_name, int(rating),classID)
                print"""
                    <script = "javascript">
                    alert("Upload Successful! Your country thanks you.")
                    </script>
                    """
                showFrontPage()
                quit()
                
        ##Javascript to alert user
        insertNewDoc(doc_url, doc_name, int(rating))
        insertNewClass(class_num,class_name,semester, year)

        print"""
            <script = "javascript">
            alert("Upload Successful! Your class thanks you.")
            </script>
            """
        showFrontPage()
        
        #show front page
    else: 
        showFrontPage()
 


    doHTMLTail()    

