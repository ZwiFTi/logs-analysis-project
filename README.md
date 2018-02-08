
# **logs-analysis-project**
### **About this project**
In this project, we'll work with data that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths. The web server and the reporting tool both connect to the same database, allowing information to flow from the web server into the report.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, a Python programm has been coded and will deliver answer on the folowing questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### **How to Run?**
#### PreRequisites:
  * [Python3](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)

#### Setup Project:
  1. Install Vagrant and VirtualBox. Check the websites for installation manuals.
  2. Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
  3. Download the database data from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and copy it to your `/vagrant` folder.
  4. Clone [this repository](https://github.com/mvuijk/logs-analysis-project.git) or copy the [python program](newsdata.py) to your `/vagrant` folder.
  
#### Launching the Virtual Machine:
  1. Launch the Vagrant VM inside Vagrant sub-directory in the downloaded fullstack-nanodegree-vm repository using command:
  
  ```
    $ vagrant up
  ```
  2. Then Log into this using command:
  ```
    $ vagrant ssh
  ```

#### Create the database

1. Before we can run the program we need to setup the database. To create and load the data into the tables you first need to download it. Check the **'Setup Project'** paragraph for the required link.

2. After you have downloaded the file you will need to unzip it. The file inside the zip is called `newsdata.sql`. Put this file into the `/vagrant` directory, which is shared with your virtual machine.

3. To load the data, cd into the vagrant directory and use the command `psql -d news -f newsdata.sql`. Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data. Here's what this command does:
```
$ psql -d news -f newsdata.sql
```

  - `psql` — the PostgreSQL command line program
  - `-d news` — connect to the database named news which has been set up for you
  - `-f newsdata.sql` — run the SQL statements in the file newsdata.sql

4. The database includes three tables:

- The **authors** table includes information about the authors of articles.
- The **articles** table includes the articles themselves.
- The **log** table includes one entry for each time a user has accessed the site.

#### Create the Views:

1. Make sure you are still connected to the database. If not run the following command within you Vagrant virtual machine:
```
$ psql -d news
```

2. Create view "view_art_cnt" by copy and paste the following code to the command line:
```
CREATE VIEW view_art_cnt AS
SELECT a.title, 
       COUNT(*) AS c_articles
  FROM articles AS a
  JOIN log      AS l
    ON '/article/'||a.slug = l.path
 WHERE l.status LIKE '%200%'
 GROUP BY a.title
 ORDER BY c_articles DESC;
```
| Column     | Type     |
| :-------   | :------- |
| title      | char     |
| c_articles | integer  |

3. Create view "view_art_auth_cnt" by copy and paste the following code to the command line:
```
CREATE VIEW view_art_auth_cnt AS
SELECT aut.name, 
       COUNT(*) AS c_articles
  FROM authors  AS aut,
       articles AS art
  JOIN log      AS l
    ON '/article/'||art.slug = l.path
 WHERE aut.id = art.author
   AND l.status LIKE '%200%'
 GROUP BY aut.name
 ORDER BY c_articles DESC;
```
| Column     | Type     |
| :--------- | :------- |
| name       | char     |
| c_articles | integer  |

4. Create view "view_date_err_perc" by copy and paste the following code to the command line:
```
CREATE VIEW view_date_err_perc AS 
SELECT date(l.time),
       ROUND(100.0 * COUNT(*) FILTER (WHERE l.status NOT LIKE '%200%') / COUNT(*),2) AS "err_perc"
  FROM log AS l
 GROUP BY date(l.time);
```
| Column   | Type     |
| :------- | :------- |
| date     | date     |
| err_perc | float    |

#### Executing the program and get query results:
1.  Make sure you are in the `/vagrant` working directory of your virtual machine. When you are not sure if you are located in the right folder then type `pwd`. This command will show you your location. The program should be located in this directory. Type the following command to run the program:

`$ python3 newdata.py`

The output of this program is displayed in your terminal window. A textfile with the output is also added to this repository. You can find it [here](output.txt).