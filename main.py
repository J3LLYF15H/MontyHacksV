from flask import Flask, render_template, request, url_for, flash, redirect, session

#for website
app = Flask(__name__)
app.config['SECRET_KEY'] = 'not_secret_key'

@app.before_request
def before_request():
    if (not session.get('score')):
        session['files'] = ['tutorial.txt']
        session['sites'] = ['tutorial']
        session['score'] = 0
        session['passed'] = {
            "job" : [],
            "bluebird" : []
        }        
    return None

#home
@app.route('/')
def index():
    if (session['score']==16):
        return render_template('youwin.html')
    return render_template('index.html')

##########FILES##########
@app.route('/files/tutorial.txt')
def tutorial_file():
    return render_template('files/tutorial.html')

@app.route('/files/password_leaks_job.txt')
def jobleaks():
    return render_template('files/passwordleakjob.html')

@app.route('/files/email_leaks_bluebird.txt')
def birdleaks():
    return render_template('files/emailleakbird.html')

##########SITES##########
@app.route('/sites/tutorial', methods=('GET', 'POST'))
def tutorial_site():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if (username=='admin' and password=='password'):
            flash('Success!')
            flash('Now, try some of the other files and sites! You can use both files and sites to gather information, and try to hack as many people as you can!')
            flash('As you progress, you might unlock new files and websites, so be sure to check.')
            flash('Earn points by hacking into as many different accounts as you can!')
            flash('Have fun!')
            session['files'].pop(0)
            session['sites'].pop(0)
            session['sites'].append('bluebird')
            session['sites'].append('getajobtoday')
            session['files'].append('password_leaks_job.txt')
            session['score'] += 1
            return redirect(url_for('index'))
        else:
            flash('Username or password is incorrect.')
    return render_template('sites/tutorial.html')

@app.route('/sites/bluebird')
def bluebird():
    return render_template('sites/bluebird.html')

@app.route('/sites/getajobtoday', methods=('GET', 'POST'))
def job():
    if request.method == 'POST':
        if ('back' in request.form):
            return redirect(url_for('index'))
        email = request.form['email']
        password = request.form['password']
        correct = {
            'gdunkeld@eps.com':'Dunkeld0520',
            'banderson@eps.com':'kingplatypus1207',
            'mark@eps.com':'bestgolfer',
            'york@eps.com':'orkorkork',
            'brobinson@eps.com':'icequeen0617'
        }
        if (email in correct):
            if (password == correct[email]):
                if (not 'bluebird/login' in session['sites']):
                    session['sites'].append('bluebird/login')
                if (not email in session['passed']['job']):
                    session['passed']['job'].append(email)
                    session['score']+=1
                return render_template('success.html')
            else:
                flash('Password is incorrect.')
        else:
            flash('Username is incorrect.')
    return render_template('sites/emaillogin.html')

@app.route('/sites/bluebird/login', methods=('GET', 'POST'))
def bluelogin():
    if request.method == 'POST':
        if ('back' in request.form):
            return redirect(url_for('index'))
        email = request.form['email']
        password = request.form['password']
        correct = {
            'gdunkeld@eps.com':'Dunkeld0520',
            'banderson@eps.com':'Anderson1207',
            'mark@eps.com':'BestGolfer',
            'york@eps.com':'orkorkork',
            'brobinson@eps.com':'IceQueen0617',
            'JoeJefferJinion@eps.com':'qwertyui',
            'Gank@eps.com':'12345678',
            'klobinstove@eps.com':'password',
            'jnoverdive@eps.com':'00000000',
            'alexinol@eps.com':'abcdefgh'   
        }
        if (email in correct):
            if (password == correct[email]):
                if (not email in session['passed']['bluebird']):
                    session['passed']['bluebird'].append(email)
                    session['score']+=1
                if (session['score'] > 6 and not 'email_leaks_bluebird.txt' in session['files']):
                    session['files'].append('email_leaks_bluebird.txt')
                return render_template('success.html')
            else:
                flash('Password is incorrect.')
        else:
            flash('Username is incorrect.')
    if('email_leaks_bluebird.txt' in session['files']):
        flash('Some people use really common passwords, which are usually very easy to guess. (Note: Bluebird requires at least 8 characters for a password!)')
    else:
        flash('Some people use the same password for everything! Others use a slight variation (such as capitalizing certain letters), and many people use their own names in their passwords.')
    return render_template('sites/emaillogin.html')
    
#runs the website- all website things must be above
if __name__ == "__main__": 
	app.run(host='0.0.0.0', port=5000)
