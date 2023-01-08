from flask import Flask,redirect,render_template,session,request,url_for,send_file
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "363cd1255b3e41f7ac817215d415f22a"

@app.route('/',methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            return render_template('error.html')
        return render_template('download.html',url = url)
    return render_template('home.html')

@app.route('/download',methods = ['GET','POST'])
def download_video():
    if request.method == 'POST':
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='video.mp4', mimetype='video/mp4')
    return redirect(url_for('home'))    

if __name__=='__main__':
    app.run(debug=False,host='0.0.0.0')

