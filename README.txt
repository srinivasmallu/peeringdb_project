How to Execute the file.

Activate the  Python Environment in the directory where the files are:

root@ip-172-31-101-19:/home/ubuntu# . p2/bin/activate
(p2) root@ip-172-31-101-19:/home/ubuntu#

Make sure the user has write access to the following directory:

/var/www/html/

Once the python file is executed , it will generate as_report.txt file, which will be read by a PHP script, and serves the contents:

(p2) root@ip-172-31-101-19:/home/ubuntu# ./asreport.py
(p2) root@ip-172-31-101-19:/home/ubuntu#

(p2) root@ip-172-31-101-19:/home/ubuntu# ls /var/www/html/as_report.txt
/var/www/html/as_report.txt
(p2) root@ip-172-31-101-19:/home/ubuntu#

The content from as_report.txt is served by Apache Webserver :

http://ec2-54-183-197-162.us-west-1.compute.amazonaws.com/

