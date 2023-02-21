from flask import Flask , request , render_template,jsonify, session
from flask_mysqldb import MySQL
import _mysql_connector
from datetime import datetime
# import docx2txt
# import pytesseract
# from PIL import Image

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'my_db'

mysql=MySQL(app)

# @app.route('/',methods=['GET'])
# def la():
#     cur=mysql.connection.cursor()
#     query=("select * from index_table where text_key='title_text';")
#     cur.execute(query)
#     data=cur.fetchall()
#     print(data)
#     title_ = data[0][1]
#     cur.close()


#     cur=mysql.connection.cursor()
#     query=("select * from images_table")
#     cur.execute(query)
#     data=cur.fetchall()
#     print(data)


#     #arrange Key value pairs to get identify unique keys....
#     xy_key = 'xy'
#     aaa_key = 'aaaa'


#     xy_value = ''
#     aaa_value = ''

#     for d in data:
#         if (str(d[0]).strip() == str(xy_key).strip()):
#             xy_value = d[1]
#             break
    
#     for d in data:
#         if (d[0] == aaa_key):
#             aaa_value = d[1]
#             break
    

#     image_key = data[0][1] #(('xy','das'),('xy','fas'))
#     cur.close()

#     return render_template('index.html',title=title_,aaa=aaa_value,xy=xy_value)



# #Image upload
# @app.route('/upload_image',methods=['POST'])
# def upload():
#     if (request.method == "POST"):
#         f = request.files['file']
#         image_key = request.form['image_key']

#         file_name = "static/uploads/"+f.filename
#         f.save(file_name)
#         #2nd steps
#         # update to database
#         cursor=mysql.connection.cursor() #replace (xy) to actual keys
#         cursor.execute("insert into images_table (image_key,image_value) values(%s,%s)",(image_key,file_name))
#         mysql.connection.commit()
#         cursor.close()
#     return render_template('admin.html',message_="File uploaded successfully!")

# # Admin page visit...
# @app.route('/admin',methods=['GET'])
# def admin():
#     cur=mysql.connection.cursor()
#     query=("select * from index_table where text_key='title_text';")
#     cur.execute(query)
#     data=cur.fetchall()
#     print(data)
#     title_value = data[0][1]
#     title_key = data[0][0]
#     cur.close()
#     return render_template("admin.html",text_key=title_key,text_value=title_value)


# #Update title_text , title_keys
# @app.route('/update_admin',methods=["POST"])
# def upadte_admin():
#     form_value = request.form
#     text_value = form_value['text_value']
#     text_key = form_value['text_key']
#     messge = ""
#     try:
#         cursor=mysql.connection.cursor()
#         cursor.execute("update index_table set text_value=(%s) where text_key = (%s)",(text_value,text_key))
#         mysql.connection.commit()
#         cursor.close()
#         messge = "Data update successfully!"
#     except Exception as e:
#         messge = e

#     #regetting the values from database to update text fields...
#     cur=mysql.connection.cursor()
#     query=("select * from index_table where text_key='title_text';")
#     cur.execute(query)
#     data=cur.fetchall()
#     print(data)
#     title_value = data[0][1]
#     title_key = data[0][0]
#     cur.close()


#     return render_template('admin.html',messge_= messge,text_key=text_key,text_value=text_value)




#     return render_template('result.html',title=title_,aaa=aaa_value,xy=xy_value)
#-------------------SUPER ADMIN AREA ------------------#


def apply_global_notification_sql(type,txt,file):
    return_val = ''
    try:
        cursor=mysql.connection.cursor()
        viewd = ''
        date_time = str(datetime.now())
        cursor.execute("insert into g_notifications (type,text,file,viewd,date_time) values(%s,%s,%s,%s,%s)"
        ,(type,txt,file,viewd,date_time))
        mysql.connection.commit()
        cursor.close()

    except Exception as e:
        return_val = e
    
    return return_val




def read_notification_sql(n_id,e_id):
    print("read notifiction....................")
    print(n_id,e_id)
    single_notification = get_notification(n_id)

    all_prev_viewd = single_notification[0][4]
    all_prev_viewd = all_prev_viewd  + str(e_id) + ","
    print(all_prev_viewd)
    cursor=mysql.connection.cursor()
    cursor.execute("update g_notifications set viewd='"+str(all_prev_viewd)+"' where id="+n_id+";")
    mysql.connection.commit()
    cursor.close()


    data = check_global_notification_sql_len(e_id)


    return data

    



@app.route('/read_notification',methods=["POST"])
def read_notification():
    data = request.json

    n_id = data['n_id']
    e_id = data['e_id']
    print(n_id,e_id)
    data = read_notification_sql(n_id,e_id)

    return jsonify({"response":"OK","data":data})

def check_id(id,arr):
    print(id,arr)
    found = False
    if (id in arr):
        found = True
    return found

@app.route('/g_file',methods=['POST'])
def upload_file():
    file = request.files['g-notification-file']
    filename = 'static/uploads/'+file.filename #Save this filname to datbase notification as type
    apply_global_notification_sql('file','',filename)
    file.save(filename)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_notification(id):
    cur=mysql.connection.cursor()
    query=("select * from g_notifications where id="+id+";")
    cur.execute(query)
    data=cur.fetchall()

    return data

def check_global_notification_sql_len(id):
    cur=mysql.connection.cursor()
    query=("select * from g_notifications;")
    cur.execute(query)
    data=cur.fetchall()
    viewd_data = []
    for d in data:
        viewd = d[4]
        if (str(viewd).strip() == ''):
            print("viewd 00000000000000")
            viewd_data.append(d)
        else:
            spliter = str(viewd).split(',')
            print(spliter)
            if (not check_id(id,spliter)):
                viewd_data.append(d)

    return viewd_data

@app.route("/admin",methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route('/send_g_notification',methods=["POST"])
def send_global_notification():
    data = request.json
    notification_text = data['text']
    print(notification_text)
    retrn_val = apply_global_notification_sql("txt",notification_text,"")
    res = ''
    if (retrn_val != ""):
        res = "Something went wrong! Please try again later."
    else:
        res = "OK"
    return jsonify({"response":res})



@app.route('/check_g_notification',methods=["POST"])
def check_g_notification():
    data = request.json

    id = data['id']

    data  = check_global_notification_sql_len(id)
    len_ = len(data)
    print("LENTH: ")
    print(len_)
    print(data)
    new_data = []
    if (len_ > 1):
        for i in range(len(data)-1,0,-1):
            new_data.append(data[i])
    else:
        new_data = data

    
    return jsonify({"len":len_,"data":new_data})

    #-------------------ADMIN  AREA ------------------#
def apply_department_notification_sql(type,txxt,files):
    return_vale = ''
    try:
        cursor=mysql.connection.cursor()
        viewdee = ''
        date_timee = str(datetime.now())
        cursor.execute("insert into d_notification (typee,texte,filee,viewde,date_timee) values(%s,%s,%s,%s,%s)"
        ,(type,txxt,files,viewdee,date_timee))
        mysql.connection.commit()
        cursor.close()

    except Exception as d:
        return_vale = d
    
    return return_vale




def read_notification_sqll(n_idi,e_idi):
    print("read notifiction....................")
    print(n_idi,e_idi)
    single_notificationn = get_notificationn(n_idi)

    all_prev_viewde = single_notificationn[0][4]
    all_prev_viewde = all_prev_viewde + str(e_idi) + ","
    print(all_prev_viewde)
    cursor=mysql.connection.cursor()
    cursor.execute("update d_notification set viewde='"+str(all_prev_viewde)+"' where ids="+n_idi+";")
    mysql.connection.commit()
    cursor.close()


    dataa = check_department_notification_sql_len(e_idi)


    return dataa

    



@app.route('/read_notificationn',methods=["POST"])
def read_notificationn():
    dataa = request.json

    n_idi = dataa['n_idi']
    e_idi = dataa['e_idi']
    print(n_idi,e_idi)
    dataa = read_notification_sqll(n_idi,e_idi)

    return jsonify({"response":"OK","data":dataa})

def check_idi(idi,arrr):
    print(idi,arrr)
    foundo = False
    if (idi in arrr):
        foundo = True
    return foundo

@app.route('/d_file',methods=['POST'])
def upload_filee():
    filee = request.files['d-notification-file']
    filenamee = 'static/uploads/'+filee.filename #Save this filname to datbase notification as type
    apply_department_notification_sql('file','',filenamee)
    filee.save(filenamee)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_notificationn(idi):
    cur=mysql.connection.cursor()
    query=("select * from d_notification where ids="+idi+";")
    cur.execute(query)
    dataa=cur.fetchall()

    return dataa

def check_department_notification_sql_len(idi):
    cur=mysql.connection.cursor()
    query=("select * from d_notification;")
    cur.execute(query)
    dataa=cur.fetchall()
    viewd_dataa = []
    for d in dataa:
        viewde = d[4]
        if (str(viewde).strip() == ''):
            print("viewd 00000000000000")
            viewd_dataa.append(d)
        else:
            spliter = str(viewde).split(',')
            print(spliter)
            if (not check_id(idi,spliter)):
                viewd_dataa.append(d)

    return viewd_dataa

@app.route("/admin",methods=['GET'])
def adminn():
    return render_template('admin.html')


@app.route('/send_d_notification',methods=["POST"])
def send_department_notification():
    dataa = request.json
    notification_textt = dataa['text']
    print(notification_textt)
    retrn_vale = apply_department_notification_sql("txt",notification_textt,"")
    ress = ''
    if (retrn_vale != ""):
        ress = "Something went wrong! Please try again later."
    else:
        ress = "OK"
    return jsonify({"response":ress})


@app.route('/check_d_notification',methods=["POST"])
def check_d_notification():
    dataa = request.json

    idi = dataa['id']

    dataa  = check_department_notification_sql_len(idi)
    len_ = len(dataa)
    print("LENTH: ")
    print(len_)
    print(dataa)
    new_dataa = []
    if (len_ > 1):
        for j in range(len(dataa)-1,0,-1):
            new_dataa.append(dataa[j])
    else:
        new_dataa = dataa

    
    return jsonify({"len":len_,"data":new_dataa})
    # department admin area



    # ADMIN AND ACCOUNT AREA

def apply_admin_account_notification_sql(typee,txxxt,filees):
    return_valee = ''
    try:
        cursor=mysql.connection.cursor()
        viewdeee = ''
        date_timeee = str(datetime.now())
        cursor.execute("insert into ad_notification (typeee,txtee,fileee,viewdee,date_timeee) values(%s,%s,%s,%s,%s)"
        ,(typee,txxxt,filees,viewdeee,date_timeee))
        mysql.connection.commit()
        cursor.close()

    except Exception as f:
        return_valee = f
    
    return return_valee




def read_notification_sqlll(n_idii,e_idii):
    print("read notifiction....................")
    print(n_idii,e_idii)
    single_notificationnn = get_notificationnn(n_idii)

    all_prev_viewdee = single_notificationnn[0][4]
    all_prev_viewdee = all_prev_viewdee + str(e_idii) + ","
    print(all_prev_viewdee)
    cursor=mysql.connection.cursor()
    cursor.execute("update ad_notification set viewdee='"+str(all_prev_viewdee)+"' where idss="+n_idii+";")
    mysql.connection.commit()
    cursor.close()


    dataaa = check_admin_notification_sql_len(e_idii)


    return dataaa

    



@app.route('/read_notificationnn',methods=["POST"])
def read_notificationnn():
    dataaa = request.json

    n_idii = dataaa['n_idii']
    e_idii = dataaa['e_idii']
    print(n_idii,e_idii)
    dataaa = read_notification_sqlll(n_idii,e_idii)

    return jsonify({"response":"OK","data":dataaa})

def check_idii(idii,arrrr):
    print(idii,arrrr)
    foundu = False
    if (idii in arrrr):
        foundu = True
    return foundu

@app.route('/a_file',methods=['POST'])
def upload_fileeee():
    fileee = request.files['a-notification-file']
    filenameee = 'static/uploads/'+fileee.filename #Save this filname to datbase notification as type
    apply_admin_account_notification_sql('file','',filenameee)
    fileee.save(filenameee)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_notificationnn(idii):
    cur=mysql.connection.cursor()
    query=("select * from ad_notification where idss="+idii+";")
    cur.execute(query)
    dataaa=cur.fetchall()

    return dataaa

def check_admin_notification_sql_len(idii):
    cur=mysql.connection.cursor()
    query=("select * from ad_notification;")
    cur.execute(query)
    dataaa=cur.fetchall()
    viewd_dataaa = []
    for f in dataaa:
        viewde = f[4]
        if (str(viewde).strip() == ''):
            print("viewd 00000000000000")
            viewd_dataaa.append(f)
        else:
            spliter = str(viewde).split(',')
            print(spliter)
            if (not check_id(idii,spliter)):
                viewd_dataaa.append(f)

    return viewd_dataaa

@app.route("/admin",methods=['GET'])
def adminnn():
    return render_template('admin.html')


@app.route('/send_a_notification',methods=["POST"])
def send_admin_notification():
    dataaa = request.json
    notification_texttt = dataaa['text']
    print(notification_texttt)
    retrn_vale = apply_admin_account_notification_sql("txt",notification_texttt,"")
    resss = ''
    if (retrn_vale != ""):
        resss = "Something went wrong! Please try again later."
    else:
        resss = "OK"
    return jsonify({"response":resss})


@app.route('/check_a_notification',methods=["POST"])
def check_a_notification():
    dataaa = request.json

    idii = dataaa['id']

    dataaa  = check_admin_notification_sql_len(idii)
    len_ = len(dataaa)
    print("LENTH: ")
    print(len_)
    print(dataaa)
    new_dataaa = []
    if (len_ > 1):
        for z in range(len(dataaa)-1,0,-1):
            new_dataaa.append(dataaa[z])
    else:
        new_dataaa = dataaa

    
    return jsonify({"len":len_,"data":new_dataaa})

    # end ADMIN AND  ACCOUNT AREA

# sales  and marketing area
def apply_sales_notification_sql(typeee,txxxxt,fileeees):
    return_valeee = ''
    try:
        cursor=mysql.connection.cursor()
        viewdeeee = ''
        date_timeeee= str(datetime.now())
        cursor.execute("insert into s_notification (typeeee,txteee,fileeeee,viewdeee,date_timeeee) values(%s,%s,%s,%s,%s)"
        ,(typeee,txxxxt,fileeees,viewdeeee,date_timeeee))
        mysql.connection.commit()
        cursor.close()

    except Exception as s:
        return_valeee = s
    
    return return_valeee




def res_notification_sqllll(n_idiiii,e_idiiii):
    print("read notifiction....................")
    print(n_idiiii,e_idiiii)
    single_notificationnnn = get_notificationnnn(n_idiiii)

    all_prev_viewdeee = single_notificationnnn[0][4]
    all_prev_viewdeee = all_prev_viewdeee + str(e_idiiii) + ","
    print(all_prev_viewdeee)
    cursor=mysql.connection.cursor()
    cursor.execute("update s_notification set viewdeee='"+str(all_prev_viewdeee)+"' where idsss="+n_idiiii+";")
    mysql.connection.commit()
    cursor.close()


    dataaaa = check_sales_notification_sql_len(e_idiiii)


    return dataaaa

    



@app.route('/res_notificationnnn',methods=["POST"])
def res_notificationnnn():
    dataaaa = request.json

    n_idiiii = dataaaa['n_idiiii']
    e_idiiii = dataaaa['e_idiiii']
    print(n_idiiii,e_idiiii)
    dataaaa = res_notification_sqllll(n_idiiii,e_idiiii)

    return jsonify({"response":"OK","data":dataaaa})

def check_idiiii(idiii,arrrrr):
    print(idiii,arrrrr)
    foundu = False
    if (idiii in arrrrr):
        foundz = True
    return foundz

@app.route('/s_file',methods=['POST'])
def upload_fileeeeee():
    fileeee = request.files['s-notification-file']
    filenameeee = 'static/uploads/'+fileeee.filename #Save this filname to datbase notification as type
    apply_sales_notification_sql('file','',filenameeee)
    fileeee.save(filenameeee)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_notificationnnn(idiii):
    cur=mysql.connection.cursor()
    query=("select * from s_notification where idsss="+idiii+";")
    cur.execute(query)
    dataaaa=cur.fetchall()

    return dataaaa

def check_sales_notification_sql_len(idiii):
    cur=mysql.connection.cursor()
    query=("select * from s_notification;")
    cur.execute(query)
    dataaaa=cur.fetchall()
    viewd_dataaaaa = []
    for t in dataaaa:
        viewde = t[4]
        if (str(viewde).strip() == ''):
            print("viewd 00000000000000")
            viewd_dataaaaa.append(t)
        else:
            spliter = str(viewde).split(',')
            print(spliter)
            if (not check_id(idiii,spliter)):
                viewd_dataaaaa.append(t)

    return viewd_dataaaaa

@app.route("/admin",methods=['GET'])
def adminnnn():
    return render_template('admin.html')


@app.route('/send_s_notification',methods=["POST"])
def send_sales_notification():
    dataaaa = request.json
    notification_textttt = dataaaa['text']
    print(notification_textttt)
    retrn_vale = apply_sales_notification_sql("txt",notification_textttt,"")
    resss = ''
    if (retrn_vale != ""):
        resss = "Something went wrong! Please try again later."
    else:
        resss = "OK"
    return jsonify({"response":resss})


@app.route('/check_s_notification',methods=["POST"])
def check_s_notification():
    dataaaa = request.json

    idiii = dataaaa['id']

    dataaaa  = check_sales_notification_sql_len(idiii)
    len_ = len(dataaaa)
    print("LENTH: ")
    print(len_)
    print(dataaaa)
    new_dataaaa = []
    if (len_ > 1):
        for d in range(len(dataaaa)-1,0,-1):
            new_dataaaa.append(dataaaa[d])
    else:
        new_dataaaa = dataaaa

    
    return jsonify({"len":len_,"data":new_dataaaa})

   
# End sales and marketing area

# deployment Team ISB
def deploy_isb_notification_sql(typeeee,txxxxxt,filees):
    return_valeeee = ''
    try:
        cursor=mysql.connection.cursor()
        viewdesee = ''
        date_times= str(datetime.now())
        cursor.execute("insert into i_notification (typeeeee,txteee,fileeese,viewdes,date_times) values(%s,%s,%s,%s,%s)"
        ,(typeeee,txxxxxt,filees,viewdesee,date_times))
        mysql.connection.commit()
        cursor.close()

    except Exception as i:
        return_valeeee = i
    
    return return_valeeee




def deploy_notification_sql(n_idis,e_idis):
    print("read notifiction....................")
    print(n_idis,e_idis)
    single_notifications = get_notifications(n_idis)

    all_prev_viewds = single_notifications[0][4]
    all_prev_viewds = all_prev_viewds + str(e_idis) + ","
    print(all_prev_viewds)
    cursor=mysql.connection.cursor()
    cursor.execute("update i_notification set viewdes='"+str(all_prev_viewds)+"' where idsss="+n_idis+";")
    mysql.connection.commit()
    cursor.close()


    datas = check_deploy_notification_sql_len(e_idis)


    return datas

    



@app.route('/rei_notifications',methods=["POST"])
def rei_notifications():
    datas = request.json

    n_idis = datas['n_idis']
    e_idis = datas['e_idis']
    print(n_idis,e_idis)
    datas = deploy_notification_sql(n_idis,e_idis)

    return jsonify({"response":"OK","data":datas})

def check_idis(ids,arrs):
    print(ids,arrs)
    founds = False
    if (ids in arrs):
        founds = True
    return founds

@app.route('/i_file',methods=['POST'])
def upload_files():
    fileees = request.files['i-notification-file']
    filenames = 'static/uploads/'+fileees.filename #Save this filname to datbase notification as type
    deploy_isb_notification_sql('file','',filenames)
    fileees.save(filenames)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_notifications(ids):
    cur=mysql.connection.cursor()
    query=("select * from i_notification where idsss="+ids+";")
    cur.execute(query)
    datas=cur.fetchall()

    return datas

def check_deploy_notification_sql_len(ids):
    cur=mysql.connection.cursor()
    query=("select * from i_notification;")
    cur.execute(query)
    datas=cur.fetchall()
    viewd_datasa = []
    for a in datas:
        viewde = a[4]
        if (str(viewde).strip() == ''):
            print("viewd 00000000000000")
            viewd_datasa.append(a)
        else:
            spliter = str(viewde).split(',')
            print(spliter)
            if (not check_id(ids,spliter)):
                viewd_datasa.append(a)

    return viewd_datasa

@app.route("/admin",methods=['GET'])
def admins():
    return render_template('admin.html')


@app.route('/send_i_notification',methods=["POST"])
def send_salei_notification():
    datas = request.json
    notification_texts = datas['text']
    print(notification_texts)
    retrn_vale = deploy_isb_notification_sql("txt",notification_texts,"")
    resss = ''
    if (retrn_vale != ""):
        resss = "Something went wrong! Please try again later."
    else:
        resss = "OK"
    return jsonify({"response":resss})


@app.route('/check_i_notification',methods=["POST"])
def check_i_notification():
    datas = request.json

    ids = datas['id']

    datas  = check_deploy_notification_sql_len(ids)
    len_ = len(datas)
    print("LENTH: ")
    print(len_)
    print(datas)
    new_datas = []
    if (len_ > 1):
        for i in range(len(datas)-1,0,-1):
            new_datas.append(datas[i])
    else:
        new_datas = datas

    
    return jsonify({"len":len_,"data":new_datas})

#  end deployment team isb

# pak navy coxail

def pak_navy_notification_sql(types,txts,files):
    return_vales = ''
    try:
        cursor=mysql.connection.cursor()
        viewdees = ''
        date_timees= str(datetime.now())
        cursor.execute("insert into p_notification (typse,txtes,filese,viewdess,date_timees) values(%s,%s,%s,%s,%s)"
        ,(types,txts,files,viewdees,date_timees))
        mysql.connection.commit()
        cursor.close()

    except Exception as p:
        return_vales = p
    
    return return_vales




def navy_notification_sql(n_idis,e_idis):
    print("read notifiction....................")
    print(n_idis,e_idis)
    single_notificationss = get_notificationss(n_idis)

    all_prev_viewdss = single_notificationss[0][4]
    all_prev_viewdss = all_prev_viewdss + str(e_idis) + ","
    print(all_prev_viewdss)
    cursor=mysql.connection.cursor()
    cursor.execute("update p_notification set viewdess='"+str(all_prev_viewdss)+"' where idisss="+n_idis+";")
    mysql.connection.commit()
    cursor.close()


    datass = check_navy_notification_sql_len(e_idis)


    return datass

    



@app.route('/rep_notifications',methods=["POST"])
def rep_notifications():
    datass = request.json

    n_idis = datass['n_idis']
    e_idis = datass['e_idis']
    print(n_idis,e_idis)
    datass = navy_notification_sql(n_idis,e_idis)

    return jsonify({"response":"OK","data":datass})

def check_idis(idis,arrss):
    print(idis,arrss)
    foundss = False
    if (idis in arrss):
        foundss = True
    return foundss

@app.route('/p_file',methods=['POST'])
def upload_filess():
    fileeess = request.files['p-notification-file']
    filenames = 'static/uploads/'+fileeess.filename #Save this filname to datbase notification as type
    pak_navy_notification_sql('file','',filenames)
    fileeess.save(filenames)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_notificationss(idis):
    cur=mysql.connection.cursor()
    query=("select * from p_notification where idisss="+idis+";")
    cur.execute(query)
    datass=cur.fetchall()

    return datass

def check_navy_notification_sql_len(idis):
    cur=mysql.connection.cursor()
    query=("select * from p_notification;")
    cur.execute(query)
    datass=cur.fetchall()
    viewd_datassa = []
    for a in datass:
        viewde = a[4]
        if (str(viewde).strip() == ''):
            print("viewd 00000000000000")
            viewd_datassa.append(a)
        else:
            spliter = str(viewde).split(',')
            print(spliter)
            if (not check_id(idis,spliter)):
                viewd_datassa.append(a)

    return viewd_datassa

@app.route("/admin",methods=['GET'])
def adminss():
    return render_template('admin.html')


@app.route('/send_p_notification',methods=["POST"])
def send_salep_notification():
    datass = request.json
    notification_texts = datass['text']
    print(notification_texts)
    retrn_vale = pak_navy_notification_sql("txt",notification_texts,"")
    resss = ''
    if (retrn_vale != ""):
        resss = "Something went wrong! Please try again later."
    else:
        resss = "OK"
    return jsonify({"response":resss})


@app.route('/check_p_notification',methods=["POST"])
def check_p_notification():
    datass = request.json

    idis = datass['id']

    datass  = check_navy_notification_sql_len(idis)
    len_ = len(datass)
    print("LENTH: ")
    print(len_)
    print(datass)
    new_datass = []
    if (len_ > 1):
        for i in range(len(datass)-1,0,-1):
            new_datass.append(datass[i])
    else:
        new_datass = datass

    
    return jsonify({"len":len_,"data":new_datass})

# End pak navy coxail

# Customer support 

def Customer_support_notification_sql(tyypee,txtes,filles):
    return_valles = ''
    try:
        cursor=mysql.connection.cursor()
        viewdde = ''
        date_ttime= str(datetime.now())
        cursor.execute("insert into c_notification (typex,txet,fiile,vieewde,date_tiime) values(%s,%s,%s,%s,%s)"
        ,(tyypee,txtes,filles,viewdde,date_ttime))
        mysql.connection.commit()
        cursor.close()

    except Exception as c:
        return_valles = c
    
    return return_valles




def support_notification_sql(n_iid,e_iid):
    print("read notifiction....................")
    print(n_iid,e_iid)
    single_notiffication = get_notiffication(n_iid)

    all_prev_viewwds = single_notiffication[0][4]
    all_prev_viewwds = all_prev_viewwds + str(e_iid) + ","
    print(all_prev_viewwds)
    cursor=mysql.connection.cursor()
    cursor.execute("update c_notification set viewdess='"+str(all_prev_viewwds)+"' where iid="+n_iid+";")
    mysql.connection.commit()
    cursor.close()


    ddata = check_support_notification_sql_len(e_iid)


    return ddata

    



@app.route('/rec_notifications',methods=["POST"])
def rec_notifications():
    ddata = request.json

    n_iid = ddata['n_iid']
    e_iid = ddata['e_iid']
    print(n_iid,e_iid)
    ddata = support_notification_sql(n_iid,e_iid)

    return jsonify({"response":"OK","data":ddata})

def checkk_id(idd,aar):
    print(idd,aar)
    ffound = False
    if (idd in aar):
        ffound = True
    return ffound

@app.route('/c_file',methods=['POST'])
def upload_filex():
    filles = request.files['c-notification-file']
    filenames = 'static/uploads/'+filles.filename #Save this filname to datbase notification as type
    Customer_support_notification_sql('file','',filenames)
    filles.save(filenames)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_notiffication(idd):
    cur=mysql.connection.cursor()
    query=("select * from c_notification where iid="+idd+";")
    cur.execute(query)
    ddata=cur.fetchall()

    return ddata

def check_support_notification_sql_len(idd):
    cur=mysql.connection.cursor()
    query=("select * from c_notification;")
    cur.execute(query)
    ddata=cur.fetchall()
    viewd_ddataa = []
    for c in ddata:
        viewde = c[4]
        if (str(viewde).strip() == ''):
            print("viewd 00000000000000")
            viewd_ddataa.append(c)
        else:
            spliter = str(viewde).split(',')
            print(spliter)
            if (not check_id(idd,spliter)):
                viewd_ddataa.append(c)

    return viewd_ddataa

@app.route("/admin",methods=['GET'])
def admiin():
    return render_template('admin.html')


@app.route('/send_c_notification',methods=["POST"])
def send_salec_notification():
    ddata = request.json
    notification_texttt = ddata['text']
    print(notification_texttt)
    retrnn_vale = support_notification_sql("txt",notification_texttt,"")
    rees = ''
    if (retrnn_vale != ""):
        rees = "Something went wrong! Please try again later."
    else:
        rees = "OK"
    return jsonify({"response":rees})


@app.route('/check_c_notification',methods=["POST"])
def check_c_notification():
    ddata = request.json

    idd = ddata['id']

    ddata  = check_support_notification_sql_len(idd)
    len_ = len(ddata)
    print("LENTH: ")
    print(len_)
    print(ddata)
    new_ddata = []
    if (len_ > 1):
        for o in range(len(ddata)-1,0,-1):
            new_ddata.append(ddata[o])
    else:
        new_ddata = ddata

    
    return jsonify({"len":len_,"data":new_ddata})


# End customer support department


# deployment team lahore

def dept_team_lahore_notification_sql(typpe,ttxt,ffile):
    retturn_vale = ''
    try:
        cursor=mysql.connection.cursor()
        viiiewde = ''
        datee_time= str(datetime.now())
        cursor.execute("insert into L_notification (ttyyp,ttxtt,ffiil,viieewd,daate_time) values(%s,%s,%s,%s,%s)"
        ,(typpe,ttxt,ffile,viiiewde,datee_time))
        mysql.connection.commit()
        cursor.close()

    except Exception as l:
        retturn_vale = l
    
    return retturn_vale




def lahore_notification_sql(n_iidi,e_idii):
    print("read notifiction....................")
    print(n_iidi,e_idii)
    single_notificcation = get_notificcation(n_iidi)

    all_prev_viewwd = single_notificcation[0][4]
    all_prev_viewwd = all_prev_viewwd + str(e_idii) + ","
    print(all_prev_viewwd)
    cursor=mysql.connection.cursor()
    cursor.execute("update L_notification set viieewd='"+str(all_prev_viewwd)+"' where iidi="+n_iidi+";")
    mysql.connection.commit()
    cursor.close()


    ddatta = check_lahore_notification_sql_len(e_idii)


    return ddatta

    



@app.route('/reL_notifications',methods=["POST"])
def reL_notifications():
    ddatta = request.json

    n_iidi = ddatta['n_iidi']
    e_idii = ddatta['e_idii']
    print(n_iidi,e_idii)
    ddatta = lahore_notification_sql(n_iidi,e_idii)

    return jsonify({"response":"OK","data":ddatta})

def chheck_id(iddi,aarr):
    print(iddi,aarr)
    foundl = False
    if (iddi in aarr):
        foundl = True
    return foundl

@app.route('/l_file',methods=['POST'])
def upload_ffil():
    ffille = request.files['l-notification-file']
    filenamesx = 'static/uploads/'+ffille.filename #Save this filname to datbase notification as type
    dept_team_lahore_notification_sql('file','',filenamesx)
    ffille.save(filenamesx)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_notificcation(iddi):
    cur=mysql.connection.cursor()
    query=("select * from L_notification where iidi="+iddi+";")
    cur.execute(query)
    ddatta=cur.fetchall()

    return ddatta

def check_lahore_notification_sql_len(iddi):
    cur=mysql.connection.cursor()
    query=("select * from L_notification;")
    cur.execute(query)
    ddatta=cur.fetchall()
    viewd_ddattaa = []
    for a in ddatta:
        viewde = a[4]
        if (str(viewde).strip() == ''):
            print("viewd 00000000000000")
            viewd_ddattaa.append(a)
        else:
            spliter = str(viewde).split(',')
            print(spliter)
            if (not check_id(iddi,spliter)):
                viewd_ddattaa.append(a)

    return viewd_ddattaa

@app.route("/admin",methods=['GET'])
def adminsxx():
    return render_template('admin.html')


@app.route('/send_L_notification',methods=["POST"])
def send_saleL_notification():
    ddatta = request.json
    notification_teexts = ddatta['text']
    print(notification_teexts)
    retrrn_vale = dept_team_lahore_notification_sql("txt",notification_teexts,"")
    resss = ''
    if (retrrn_vale != ""):
        resss = "Something went wrong! Please try again later."
    else:
        resss = "OK"
    return jsonify({"response":resss})


@app.route('/check_L_notification',methods=["POST"])
def check_L_notification():
    ddatta = request.json

    iddi = ddatta['id']

    ddatta  = check_lahore_notification_sql_len(iddi)
    len_ = len(ddatta)
    print("LENTH: ")
    print(len_)
    print(ddatta)
    new_ddatta = []
    if (len_ > 1):
        for i in range(len(ddatta)-1,0,-1):
            new_ddatta.append(ddatta[i])
    else:
        new_ddatta = ddatta

    
    return jsonify({"len":len_,"data":new_ddatta})



# End deployment team lahore

# Fiber Team islamabad

def fiber_team_isb_notification_sql(typpee,ttxxt,ffilee):
    retturn_valee = ''
    try:
        cursor=mysql.connection.cursor()
        viiewwde = ''
        datee_timee= str(datetime.now())
        cursor.execute("insert into f_notification (ttyype,ttxxtte,ffiile,viieewde,daate_timee) values(%s,%s,%s,%s,%s)"
        ,(typpee,ttxxt,ffilee,viiewwde,datee_timee))
        mysql.connection.commit()
        cursor.close()

    except Exception as f:
        retturn_valee = f
    
    return retturn_valee




def fiber_notification_sql(n_iidiee,e_idiie):
    print("read notifiction....................")
    print(n_iidiee,e_idiie)
    single_notificcationn = get_notificcationn(n_iidiee)

    all_prev_viewwde = single_notificcationn[0][4]
    all_prev_viewwde = all_prev_viewwde + str(e_idiie) + ","
    print(all_prev_viewwde)
    cursor=mysql.connection.cursor()
    cursor.execute("update f_notification set viieewde='"+str(all_prev_viewwde)+"' where iidie="+n_iidiee+";")
    mysql.connection.commit()
    cursor.close()


    ddattax = check_fiber_notification_sql_len(e_idiie)


    return ddattax

    



@app.route('/ref_notifications',methods=["POST"])
def ref_notifications():
    ddattax = request.json

    n_iidiee = ddattax['n_iidiee']
    e_idiie = ddattax['e_idiie']
    print(n_iidiee,e_idiie)
    ddattax = fiber_notification_sql(n_iidiee,e_idiie)

    return jsonify({"response":"OK","data":ddattax})

def chheck_iid(iddixx,aarrx):
    print(iddixx,aarrx)
    foundf = False
    if (iddixx in aarrx):
        foundf = True
    return foundf

@app.route('/f_file',methods=['POST'])
def upload_ffilx():
    ffillex = request.files['f-notification-file']
    filenamesx = 'static/uploads/'+ffillex.filename #Save this filname to datbase notification as type
    fiber_team_isb_notification_sql('file','',filenamesx)
    ffillex.save(filenamesx)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_notificcationn(iddix):
    cur=mysql.connection.cursor()
    query=("select * from f_notification where iidie="+iddix+";")
    cur.execute(query)
    ddattax=cur.fetchall()

    return ddattax

def check_fiber_notification_sql_len(iddix):
    cur=mysql.connection.cursor()
    query=("select * from f_notification;")
    cur.execute(query)
    ddattax=cur.fetchall()
    viewd_ddattaa = []
    for a in ddattax:
        viewde = a[4]
        if (str(viewde).strip() == ''):
            print("viewd 00000000000000")
            viewd_ddattaa.append(a)
        else:
            spliter = str(viewde).split(',')
            print(spliter)
            if (not check_id(iddix,spliter)):
                viewd_ddattaa.append(a)

    return viewd_ddattaa

@app.route("/admin",methods=['GET'])
def adminsxxx():
    return render_template('admin.html')


@app.route('/send_f_notification',methods=["POST"])
def send_salef_notification():
    ddattax = request.json
    notification_texxts = ddattax['text']
    print(notification_texxts)
    retrrn_vale =fiber_team_isb_notification_sql("txt",notification_texxts,"")
    resss = ''
    if (retrrn_vale != ""):
        resss = "Something went wrong! Please try again later."
    else:
        resss = "OK"
    return jsonify({"response":resss})


@app.route('/check_f_notification',methods=["POST"])
def check_f_notification():
    ddattax = request.json

    iddix = ddattax['id']

    ddattax  = check_fiber_notification_sql_len(iddix)
    len_ = len(ddattax)
    print("LENTH: ")
    print(len_)
    print(ddattax)
    new_ddatta = []
    if (len_ > 1):
        for i in range(len(ddattax)-1,0,-1):
            new_ddatta.append(ddattax[i])
    else:
        new_ddatta = ddattax

    
    return jsonify({"len":len_,"data":new_ddatta})



# end fiber team isb
# dha lahore department

def dha_Lahore_notification_sql(ttyppe,txtxte,ffilllee):
    reetturn_valleee = ''
    try:
        cursor=mysql.connection.cursor()
        vviiewdee = ''
        datee_ttimee= str(datetime.now())
        cursor.execute("insert into o_notification (ttyyppee,txtxtette,ffiiille,viiieewdee,daaattte_timee) values(%s,%s,%s,%s,%s)"
        ,(ttyppe,txtxte,ffilllee,vviiewdee,datee_ttimee))
        mysql.connection.commit()
        cursor.close()

    except Exception as o:
        reetturn_valleee = o
    
    return reetturn_valleee




def dha_notification_sql(ni_idii,ei_idii):
    print("read notifiction....................")
    print(ni_idii,ei_idii)
    single_nottifficcationnn =  get_nottifficcnation(ni_idii)

    all_preev_viewdeee = single_nottifficcationnn[0][4]
    all_preev_viewdeee = all_preev_viewdeee + str(ei_idii) + ","
    print(all_preev_viewdeee)
    cursor=mysql.connection.cursor()
    cursor.execute("update o_notification set viiieewdee='"+str(all_preev_viewdeee)+"' where iidixxx="+ni_idii+";")
    mysql.connection.commit()
    cursor.close()


    ddataxxx = check_dha_notification_sql_len(ei_idii)


    return ddataxxx

    



@app.route('/rek_notifications',methods=["POST"])
def rek_notificationss():
    ddataxxx = request.json

    ni_idii = ddataxxx['ni_idii']
    ei_idii = ddataxxx['ei_idii']
    print(ni_idii,ei_idii)
    ddataxxx = dha_notification_sql(ni_idii,ei_idii)

    return jsonify({"response":"OK","data":ddataxxx})

def checck_idii(idxss,arxss):
    print(idxss,arxss)
    foundp = False
    if (idxss in arxss):
        foundp = True
    return foundp

@app.route('/o_file',methods=['POST'])
def uplooad_fiille():
    filexxx = request.files['o-notification-file']
    filenamexxx = 'static/uploads/'+filexxx.filename #Save this filname to datbase notification as type
    dha_Lahore_notification_sql('file','',filenamexxx)
    filexxx.save(filenamexxx)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def  get_nottifficcnation(idixx):
    cur=mysql.connection.cursor()
    query=("select * from o_notification where iidixxx="+idixx+";")
    cur.execute(query)
    ddataxxx=cur.fetchall()

    return ddataxxx

def check_dha_notification_sql_len(idixx):
    cur=mysql.connection.cursor()
    query=("select * from o_notification;")
    cur.execute(query)
    ddataxxx=cur.fetchall()
    viewd_dettaaaa = []
    for a in ddataxxx:
        viewdeee = a[4]
        if (str(viewdeee).strip() == ''):
            print("viewd 00000000000000")
            viewd_dettaaaa.append(a)
        else:
            spliter = str(viewdeee).split(',')
            print(spliter)
            if (not check_id(idixx,spliter)):
                viewd_dettaaaa.append(a)

    return viewd_dettaaaa

@app.route("/admin",methods=['GET'])
def admixxss():
    return render_template('admin.html')


@app.route('/send_o_notification',methods=["POST"])
def send_saleo_notification():
    ddataxxx = request.json
    notification_teexxxxts = ddataxxx['text']
    print(notification_teexxxxts)
    retrrrn_vale =dha_Lahore_notification_sql("txt",notification_teexxxxts,"")
    resss = ''
    if (retrrrn_vale != ""):
        resss = "Something went wrong! Please try again later."
    else:
        resss = "OK"
    return jsonify({"response":resss})


@app.route('/check_o_notification',methods=["POST"])
def check_o_notification():
    ddataxxx = request.json

    idixx = ddataxxx['id']

    ddataxxx  = check_dha_notification_sql_len(idixx)
    len_ = len(ddataxxx)
    print("LENTH: ")
    print(len_)
    print(ddataxxx)
    new_ddatta = []
    if (len_ > 1):
        for i in range(len(ddataxxx)-1,0,-1):
            new_ddatta.append(ddataxxx[i])
    else:
        new_ddatta = ddataxxx

    
    return jsonify({"len":len_,"data":new_ddatta})

# coaxial Department

def coaxial_notification_sql(ttyp,txtt,fiillee):
    reetturn_valee = ''
    try:
        cursor=mysql.connection.cursor()
        vviewde = ''
        date_ttime= str(datetime.now())
        cursor.execute("insert into x_notification (ttyypee,txtttte,ffiiile,viiieewde,daaate_timee) values(%s,%s,%s,%s,%s)"
        ,(ttyp,txtt,fiillee,vviewde,date_ttime))
        mysql.connection.commit()
        cursor.close()

    except Exception as x:
        reetturn_valee = x
    
    return reetturn_valee




def coxal_notification_sql(ni_id,ei_id):
    print("read notifiction....................")
    print(ni_id,ei_id)
    single_nottificcation = get_nottificcation(ni_id)

    all_preev_viewde = single_nottificcation[0][4]
    all_preev_viewde = all_preev_viewde + str(ei_id) + ","
    print(all_preev_viewde)
    cursor=mysql.connection.cursor()
    cursor.execute("update x_notification set viiieewde='"+str(all_preev_viewde)+"' where iidix="+ni_id+";")
    mysql.connection.commit()
    cursor.close()


    ddatax = check_coxal_notification_sql_len(ei_id)


    return ddatax

    



@app.route('/rex_notifications',methods=["POST"])
def rex_notifications():
    ddatax = request.json

    ni_id = ddatax['ni_id']
    ei_id = ddatax['ei_id']
    print(ni_id,ei_id)
    ddatax = coxal_notification_sql(ni_id,ei_id)

    return jsonify({"response":"OK","data":ddatax})

def checck_id(idx,arx):
    print(idx,arx)
    foundx = False
    if (idx in arx):
        foundx = True
    return foundx

@app.route('/x_file',methods=['POST'])
def uplooad_file():
    filex = request.files['x-notification-file']
    filenamex = 'static/uploads/'+filex.filename #Save this filname to datbase notification as type
    coaxial_notification_sql('file','',filenamex)
    filex.save(filenamex)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_nottificcation(idixx):
    cur=mysql.connection.cursor()
    query=("select * from x_notification where iidix="+idixx+";")
    cur.execute(query)
    ddatax=cur.fetchall()

    return ddatax

def check_coxal_notification_sql_len(idixx):
    cur=mysql.connection.cursor()
    query=("select * from x_notification;")
    cur.execute(query)
    ddatax=cur.fetchall()
    viewd_dettaa = []
    for a in ddatax:
        viewde = a[4]
        if (str(viewde).strip() == ''):
            print("viewd 00000000000000")
            viewd_dettaa.append(a)
        else:
            spliter = str(viewde).split(',')
            print(spliter)
            if (not check_id(idixx,spliter)):
                viewd_dettaa.append(a)

    return viewd_dettaa

@app.route("/admin",methods=['GET'])
def admixx():
    return render_template('admin.html')


@app.route('/send_x_notification',methods=["POST"])
def send_salex_notification():
    ddatax = request.json
    notification_texxxts = ddatax['text']
    print(notification_texxxts)
    retrrrn_vale =coaxial_notification_sql("txt",notification_texxxts,"")
    resss = ''
    if (retrrrn_vale != ""):
        resss = "Something went wrong! Please try again later."
    else:
        resss = "OK"
    return jsonify({"response":resss})


@app.route('/check_x_notification',methods=["POST"])
def check_x_notification():
    ddatax = request.json

    idixx = ddatax['id']

    ddatax  = check_coxal_notification_sql_len(idixx)
    len_ = len(ddatax)
    print("LENTH: ")
    print(len_)
    print(ddatax)
    new_ddatta = []
    if (len_ > 1):
        for i in range(len(ddatax)-1,0,-1):
            new_ddatta.append(ddatax[i])
    else:
        new_ddatta = ddatax

    
    return jsonify({"len":len_,"data":new_ddatta})


# end coxial deparTMENT

# Lahore Fiber department

def Lahore_fiber_notification_sql(ttypp,txtxt,ffillee):
    reetturn_vallee = ''
    try:
        cursor=mysql.connection.cursor()
        vviiewde = ''
        datee_ttime= str(datetime.now())
        cursor.execute("insert into y_notification (ttyyppee,txtxttte,ffiiile,viiieewdee,daaatte_timee) values(%s,%s,%s,%s,%s)"
        ,(ttypp,txtxt,ffillee,vviiewde,datee_ttime))
        mysql.connection.commit()
        cursor.close()

    except Exception as m:
        reetturn_vallee = m
    
    return reetturn_vallee




def lahore_f_notification_sql(ni_idi,ei_idi):
    print("read notifiction....................")
    print(ni_idi,ei_idi)
    single_nottifficcation = get_nottifficcation(ni_idi)

    all_preev_viewdee = single_nottifficcation[0][4]
    all_preev_viewdee = all_preev_viewdee + str(ei_idi) + ","
    print(all_preev_viewdee)
    cursor=mysql.connection.cursor()
    cursor.execute("update y_notification set viiieewdee='"+str(all_preev_viewdee)+"' where iidixx="+ni_idi+";")
    mysql.connection.commit()
    cursor.close()


    ddataxx = check_lahore_f_notification_sql_len(ei_idi)


    return ddataxx

    



@app.route('/rey_notifications',methods=["POST"])
def rey_notifications():
    ddataxx = request.json

    ni_idi = ddataxx['ni_idi']
    ei_idi = ddataxx['ei_idi']
    print(ni_idi,ei_idi)
    ddataxx = lahore_f_notification_sql(ni_idi,ei_idi)

    return jsonify({"response":"OK","data":ddataxx})

def checck_idi(idxs,arxs):
    print(idxs,arxs)
    foundi = False
    if (idxs in arxs):
        foundi = True
    return foundi

@app.route('/y_file',methods=['POST'])
def uplooad_fiile():
    filexx = request.files['y-notification-file']
    filenamexx = 'static/uploads/'+filexx.filename #Save this filname to datbase notification as type
    Lahore_fiber_notification_sql('file','',filenamexx)
    filexx.save(filenamexx)

    return render_template("admin.html")
    # return jsonify({"response":"Notification sended successfully."})


def get_nottifficcation(idixx):
    cur=mysql.connection.cursor()
    query=("select * from y_notification where iidixx="+idixx+";")
    cur.execute(query)
    ddataxx=cur.fetchall()

    return ddataxx

def check_lahore_f_notification_sql_len(idixx):
    cur=mysql.connection.cursor()
    query=("select * from y_notification;")
    cur.execute(query)
    ddataxx=cur.fetchall()
    viewd_dettaaa = []
    for a in ddataxx:
        viewdee = a[4]
        if (str(viewdee).strip() == ''):
            print("viewd 00000000000000")
            viewd_dettaaa.append(a)
        else:
            spliter = str(viewdee).split(',')
            print(spliter)
            if (not check_id(idixx,spliter)):
                viewd_dettaaa.append(a)

    return viewd_dettaaa

@app.route("/admin",methods=['GET'])
def admixxs():
    return render_template('admin.html')


@app.route('/send_y_notification',methods=["POST"])
def send_saley_notification():
    ddataxx = request.json
    notification_teexxxts = ddataxx['text']
    print(notification_teexxxts)
    retrrrn_vale =Lahore_fiber_notification_sql("txt",notification_teexxxts,"")
    resss = ''
    if (retrrrn_vale != ""):
        resss = "Something went wrong! Please try again later."
    else:
        resss = "OK"
    return jsonify({"response":resss})


@app.route('/check_y_notification',methods=["POST"])
def check_y_notification():
    ddataxx = request.json

    idixx = ddataxx['id']

    ddataxx  = check_lahore_f_notification_sql_len(idixx)
    len_ = len(ddataxx)
    print("LENTH: ")
    print(len_)
    print(ddataxx)
    new_ddatta = []
    if (len_ > 1):
        for i in range(len(ddataxx)-1,0,-1):
            new_ddatta.append(ddataxx[i])
    else:
        new_ddatta = ddataxx

    
    return jsonify({"len":len_,"data":new_ddatta})

# End lahore fiber department


@app.route('/notification',methods=["GET"])
def notification():
    return render_template('notification.html')

@app.route('/',methods=['GET'])
def hi():
    return render_template('login.html')
@app.route('/sales_marketing')
def sales_marketing():
    return render_template('sales_marketing.html')
@app.route('/login.html')
def login():
    return render_template('login.html')   
@app.route('/deppt')
def adminandaccount():
    return render_template('deppt.html')
@app.route('/admin_account')
def adminaccount():
    return render_template('admin_account.html')    
@app.route('/projects.html')
def project():
    return render_template('projects.html')
@app.route('/register.html')
def register():
    return render_template('register.html')   
@app.route('/sales_market')
def sales_market():
    return render_template('sales_mark.html')      
@app.route('/index.html')
def index():
    return render_template('index.html')  
@app.route('/admin_acount')
def admin_acount():
    return render_template('admin_accunt.html')     
@app.route('/video_department')
def video_department():
    return render_template('video.html') 
@app.route('/deployment_team_isb')
def deployment_team_isb():
    return render_template('deploy_team_isb.html') 
@app.route('/deployment_notifi_isb')
def deployment_notifi_isb():
    return render_template('deploy_isb.html')     
@app.route('/pak_navy_coxal')
def pak_navy_coxal():
    return render_template('pak_navy_coxail.html')
@app.route('/pak_navy_coxail')
def pak_navy_coxail():
    return render_template('pak_navy.html')  
@app.route('/Customer_support')
def Customer_support():
    return render_template('customer_support.html')   
@app.route('/customer_Support_notification')
def customer_Support_notification():
    return render_template('customer_s.html')  
@app.route('/deployment_team_lahore_notification')
def deployment_team_lahore_notification():
    return render_template('deployment_lahore_notifi.html')
@app.route('/deployment_team_lahore')
def deployment_team_lahore():
    return render_template('deployment_team_lahore.html')   
@app.route('/Fiber_team_Islamabad_notification')
def fiber_team_isb_notification():
    return render_template('fiber_team_isb_notify.html') 
@app.route('/Fiber_team_Islamabad')
def fiber_team_isb():
    return render_template('fiber_team_isb.html')   
@app.route('/coaxial_department_notification')
def coaxial_department_notification():
    return render_template('coaxil_department_notifi.html') 
@app.route('/coaxial_department')
def coaxial_department():
    return render_template('coaxial_department.html')     
@app.route('/Lahore_fiber_department_notification')
def lahore_fiber_department_notification():
    return render_template('lahore_fiber_department_notify.html')
@app.route('/lahore_fiber_department')
def lahore_fiber_department():
    return render_template('lahore_fiber_department.html')      
@app.route('/dha_Lahore_department_notification')
def dha_lahore_department_notification():
    return render_template('dha_lahore_dep_notifi.html')  
@app.route('/dha_Lahore_department')
def dha_departmen():
    return render_template('dha_lahore_dep.html')                                      
@app.route('/reg',methods=['GET','POST'])
def za():
    cursor=mysql.connection.cursor()
    e=request.form["email"]
    p=request.form["password"]
    cursor.execute("insert into my_table (email,password) values(%s,%s)",(e,p))
    mysql.connection.commit()
    cursor.close()
    return render_template('login.html',status="Registered Sucessfully!")
    

@app.route('/log',methods=['GET','POST'])
def pa():
    data=request.form
    print(data)
    z=request.form['email']
    q=request.form['password']
    cur=mysql.connection.cursor()
    query=("select * from my_table where email='"+z+"'and password='"+q+"';")
    cur.execute(query)
    data=cur.fetchall()
    print(data)
    cur.close()
    logged=False
    
    if(len(data)>0):
        logged=True
        return render_template("index.html",id=data[0][0])
    







    return render_template('login.html',status="Login Failed! due to Incorrect username or password")



@app.route('/del',methods=['GET','POST'])
def ka():
   cua=mysql.connection.cursor()
   w=request.form['email']
   cua.execute("delete from my_table where email='"+w+"';") 
   mysql.connection.commit()
   cua.close()
   return "success"    

if __name__=="__main__":
        app.run(debug=False, host='0.0.0.0')