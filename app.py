from flask import Flask, request, render_template,redirect,session,url_for
from services import qrService
from flask_session import Session


app = Flask(__name__)
qr_service = qrService.QR()
app.config['SECRET_KEY'] = 'appkey' 
app.config['SESSION_TYPE'] = 'filesystem'  
Session(app)




@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == 'POST' :
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        user = qr_service.get_user(user_name)
        user_balance = user.get('user_balance',0)

        status = qr_service.user_sign(user_name=user_name, user_password=user_password, user_balance=user_balance)
        
        if status == 'exists':
            msg = "Zaten Bir Hesabınız Mevcut."
            return render_template("signup.html", msg=msg)
        
        session['user_name'] = user_name
        session['logged_in'] = True
        session['msg'] = "Kayıt İşleminiz Başarılı."
        return redirect(url_for('home'))
    
    return render_template("signup.html")

@app.route("/")
def home():
    if 'logged_in' in session and session['logged_in']:
        user_name = session.get('user_name')
        user = qr_service.get_user(user_name)
        if not user:
            return redirect(url_for('signup'))
        
        user_balance = user.get('user_balance',0)
        msg = session.get('msg', '')
        return f'Merhaba, {user_name}. {msg} Güncel Bakiyeniz: {user_balance}'
    else:
        return redirect(url_for('signup'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('signup'))

@app.route("/add_balance",  methods = ['GET'])
def add_balance():
    user_name = session.get('user_name')
    user = qr_service.get_user(user_name)
    
    if 'logged_in' not in session or not session['logged_in'] or not user:
        msg = 'Giriş Yapmanız Gerekmektedir'
        return render_template('signup.html', msg=msg)
    
    qr_value = request.args.get('qr_value')
    
    if qr_value and qr_value.isdigit():
        status = qr_service.add_balance(user_name=user_name, new_balance=int(qr_value))
        if status == 'used':
            user = qr_service.get_user(user_name)
            return render_template("activated.html", user_balance=user['user_balance'])
        
        user = qr_service.get_user(user_name)
        return render_template("balance_added.html",user_balance=user['user_balance'])
        
    else:
        return render_template("eror.html")
    
@app.route("/activate_qr",methods = ['POST'])
def activate_qr():
    qr_id= request.form.get('qr_id')
    qr_value = request.form.get('qr_value')
    user_name =  session.get('user_name')
    
    new_balance, success = qr_service.activate_qr(qr_id=qr_id, user_name=user_name)
    
    if success:
        return render_template("activated.html", user_balance=new_balance)
    else:
        return "Aktivasyon işlemi Başarısız."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

