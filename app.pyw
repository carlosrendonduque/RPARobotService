import schedule
import time
import requests

import smtplib
import os
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import email.encoders
import email.mime.text

import base64
from envelopes import Envelope
import pyodbc 
from prettytable import PrettyTable

# https://www.devdungeon.com/content/run-python-script-windows-service
def send_report():
    server = '172.17.7.26' 
    database = 'Adv_Condor_soporte' 
    username = 'usuariodms' 
    password = 'Usu2017*dms' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    cursor.execute('select id_con_cco, count(o.id) from cns_liquidacion o join cns_calendario_periodo p on o.fecha = p.fecha where p.año = 2021 and p.mes = 1 group by id_con_cco' )
    for row in cursor:
        # print(row['id_con_cco'])
        id_con_cco = str(row[0])
        send_email('3', '2021', '1', id_con_cco, '60')
        #     tabular_table.add_row(row)
def get_data(emp, ano, mes, id_con_cco, tope):    
    server = '172.17.7.26' 
    database = 'Adv_Condor_soporte' 
    username = 'usuariodms' 
    password = 'Usu2017*dms' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    # id_con_cco2='1010'
    # emp = '3'   
    # ano = '2021'    
    # mes = '1' 
    # id_con_cco  = '994'
    # tope  = '60'

    # sql = 'exec [my_database].[dbo].[my_table](?, ?, ?, ?, ?, ?, ?, ?)'
    # values = (emp, ano, mes, id_con_cco, tope )

    # cursor.execute(sql, (values))

    SQL = "execute GetCnsValidacionJornadasTope " + emp + ", " + ano + ", " + mes + ", " + id_con_cco + ", " + tope + ""

    print(SQL)

    cursor.execute("execute GetCnsValidacionJornadasTope " + emp + ", " + ano + ", " + mes + ", " + id_con_cco + ", " + tope + "")
    cursor.close()
    cursor = cnxn.cursor()
    cursor.execute("select distinct * from RPA_GetCnsValidacionJornadasTope where emp = " + emp + " and ano = " + ano + " and mes = " + mes + " and  id_con_cco = " + id_con_cco + " and accion  = 'Pendiente'")
    # tabular_fields = ["emp", "ano", "mes", "id_con_cco", "tope"]
    # tabular_table = cursor
    # tabular_table.field_names = tabular_fields 
    # for row in cursor:
    #     print(row)
    #     tabular_table.add_row(row)

    result = cursor.fetchall()
    
    p = []

    tbl = "tbl_rpa_cns_liquidacion"
    p.append(tbl)
    tbl = "<tr><td>emp</td><td>ano</td><td>mes</td><td>id_con_cco</td><td>tope</td></tr>"
    p.append(tbl)

    for row in result:
        a = "<tr><td>%s</td>"%row[0]
        p.append(a)
        b = "<td>%s</td>"%row[1]
        p.append(b)
        c = "<td>%s</td>"%row[2]
        p.append(c)
        d = "<td>%s</td><eeeeeeeeeeeee/tr>"%row[3]
        p.append(d)
        e = "<td>%s</td></tr>"%row[4]
        p.append(e)

    contents = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
        <html>
        <head>
        <meta content="text/html; charset=ISO-8859-1"
        http-equiv="content-type">
        <title>Python Webbrowser</title>
        </head>
        <body>
        <table>
        %s
        </table>
        </body>
        </html>
        """%(p)

    htmlFilename = 'report.html'
    htmlFile = open(htmlFilename, 'w')

    htmlFile.write(formatDataAsHtml(contents))

    htmlFile.close()

    cnxn.commit()   

    if not result:
        contents = "No Data"

    # resultado = ' '.join(result)

    # print(tabular_table)
    # print (resultado)
    # print (contents)
    return contents


#cursor.execute('select top 10 * from cns_liquidacion')

# for row in cursor:
#     print(row)

# try:
#     cursor.execute(SQL)
#     #cursor.execute('select top 10 * from cns_liquidacion')
#     for row in cursor:
#         print(row)
#     cursor.close()
#     cnxn.commit()
# finally:
#     cnxn.close()

""" EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS') """


url = "https://api.coindesk.com/v1/bpi/currentprice.json"
page = requests.get(url)
data = page.json()

def fetch_bitcoin():
    print("Getting Bitcoin Price ...")
    result= data['bpi']['USD']
    print(result)

def fetch_bitcoin_by_curreny(x):
    print("Getting Bitcoin Price in ...", x)
    result= data['bpi'][x]
    print(result)

def formatDataAsHtml(data):
    return "<br>".join(data)

def send_email(emp, ano, mes, id_con_cco, tope):

    EMAIL_ADDRESS = 'notificaciones_rpa@elcondor.com'
    EMAIL_PASSWORD = 'NotRpa2021*'

    # EMAIL_ADDRESS = 'condorrpa@gmail.com'
    # EMAIL_PASSWORD = 'NorRpa2021*'

    # smtp.office365.com
    # smtp.gmail.com
    with smtplib.SMTP('smtp.office365.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # result= data['bpi']['USD']

        # subject = 'Testing RPA ' + str(id_con_cco)
        #body = 'Report of validations RPA'
       

        # htmlFilename = 'test.html'
        # htmlFile = open(htmlFilename, 'w')
        
        # htmlFile.write(formatDataAsHtml(get_data()))

        # htmlFile.close()

        # print ('testing' + htmlFile)
        # body =  htmlFile
    
        sender_email = EMAIL_ADDRESS
        receiver_email = 'leorendon@gmail.com, carlos.rendon.duque@gmail.com, carlos@zen-it.solutions, stevenvallejo780@gmail.com, zenit.solutions.cloud@gmail.com'
       # receiver_email = 'carlos.rendon.duque@gmail.com, stevenvallejo780@gmail.com'
        password = EMAIL_PASSWORD

        message = MIMEMultipart("alternative")
        message["Subject"] = "RPA - test cco " + str(id_con_cco)
        message["From"] = EMAIL_ADDRESS
        message["To"] = receiver_email
        message["Cc"] = 'leo.rendon@dms.ms'

        # Create the plain-text and HTML version of your message
        text = """\
        Hola,
        Como vas?
        Este es el reporte"""
        html1 = """\
        <html>
        <body>
            <p>Hi,<br>
            How are you?<br>
            <a href="http://www.realpython.com">Real Python</a> 
            has many great tutorials.
            </p>
        </body>
        </html>
        """
        html = get_data(emp, ano, mes, id_con_cco, tope)
       
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        

        # filename = "report.html"
        # body = "Cualquier cosa"
        # msg = f'Subject: {subject}\n\n{body}'
        
        # smtp.sendmail(EMAIL_ADDRESS, receiver_email, message.as_string())
        if str(html[0]) != "N" :
            smtp.sendmail(EMAIL_ADDRESS, 'carlos.rendon.duque@gmail.com', message.as_string())
            smtp.sendmail(EMAIL_ADDRESS, 'leorendon@gmail.com', message.as_string())
            smtp.sendmail(EMAIL_ADDRESS, 'stevenvallejo780@gmail.com', message.as_string())
            smtp.sendmail(EMAIL_ADDRESS, 'carlos@zen-it.solutions', message.as_string())
            # smtp.sendmail(EMAIL_ADDRESS, 'zenit.solutions.cloud@gmail.com', message.as_string())
            # smtp.sendmail(EMAIL_ADDRESS, 'julian.bello@elcondor.com', message.as_string())
            # smtp.sendmail(EMAIL_ADDRESS, 'julian.montoya@elcondor.com', message.as_string())
            smtp.sendmail(EMAIL_ADDRESS, 'rumen.yepes@elcondor.com', message.as_string())

            print("Emails sent")
        # smtp.sendmail(EMAIL_ADDRESS, 'leorendon@gmail.com', message.as_string())
        # smtp.sendmail(EMAIL_ADDRESS, 'stevenvallejo780@gmail.com', message.as_string())
        # smtp.sendmail(EMAIL_ADDRESS, 'carlos@zen-it.solutions', message.as_string())

        # smtp.sendmail(EMAIL_ADDRESS, 'zenit.solutions.cloud@gmail.com', message.as_string())
        # smtp.sendmail(EMAIL_ADDRESS, 'julian.bello@elcondor.com', message.as_string())
        # smtp.sendmail(EMAIL_ADDRESS, 'julian.montoya@elcondor.com', message.as_string())
        # smtp.sendmail(EMAIL_ADDRESS, 'rumen.yepes@elcondor.com', message.as_string())
        # smtp.sendmail(EMAIL_ADDRESS, 'julianbellop@gmail.com', message.as_string())
        # smtp.sendmail(EMAIL_ADDRESS, 'julianbellop@outlook.com', message.as_string())

        envelope = Envelope(
            from_addr=(sender_email),
            to_addr=(receiver_email),
            subject=u'RPA Test',
            text_body=u'Hola este es el reporteeee',
            html_body=html
        )
        #envelope.add_attachment(filename)

        # envelope.send('smtp.gmail.com', login=EMAIL_ADDRESS, password=EMAIL_PASSWORD, tls=True)

        
def job():
    print("Reading time ...")

def coding():
    print("Coding time ...")

def playing():
    print("Playing time ...")

#Schedule
""" schedule.every(4).seconds.do(job)
schedule.every(10).seconds.do(coding)
schedule.every().day.at("22:00").do(playing)
 """
# schedule.every(5).seconds.do(fetch_bitcoin)
# schedule.every(6).seconds.do(fetch_bitcoin_by_curreny,'GBP')
# schedule.every(7).seconds.do(fetch_bitcoin_by_curreny,'EUR')
# schedule.every(15).seconds.do(send_report)
schedule.every().day.at("22:00").do(send_report)

while True:
    schedule.run_pending()
    time.sleep(1)
