import os
import random
from flask import Flask, redirect, render_template, session,g
ROOT='E:/anjianjipic'
SESSION_TYPE = 'memcached'
UPPER_DIR="上一级"

app = Flask(__name__,static_folder=ROOT)
app.secret_key='12345'

def list_dir():
    curpath=session['curpath']
    dirlist= os.listdir(os.path.join(ROOT,curpath[1:]))
    subdirs=[]
    if len(curpath)>1:
        subdirs.append(UPPER_DIR)
    files=[]
    for file in dirlist :
        file1=os.path.join(ROOT,curpath[1:],file)
        if os.path.isdir(file1):
            subdirs.append(file)
        if os.path.isfile(file1):
            files.append(file)
         
    g.subdirs= subdirs
    g.files  = files

def switch_path(curpath):
    print('switch path curpath=',curpath)
    session['curpath']=curpath
    session['fid'] = 0

def render():
    print('session=',session)
    list_dir()
    print('render curpath=',session['curpath'])
    print('render files=',  g.files)
    print('render  subdirs=',g.subdirs)            
    if len(g.files)==0:
        return render_template('main.html',subdirs=g.subdirs,file='',curpath=session['curpath'])
    
    id=session['fid']
    if id >= len(g.files):
            id=0
    session['fid']=id+1
    #使用随机数            
    id=random.randint(0,len(g.files)-1)      
    if id >= len(g.files):
            id=0
    
    return render_template('main.html',subdirs=g.subdirs,file=session['curpath']+'/'+g.files[id],curpath=session['curpath'])
@app.route('/switch/<dir>')
def switch_handle(dir):
    print('switch_handle dir=',dir,' curpath=',session['curpath'])
    if dir==UPPER_DIR:
        print('switch to upper')
        dir=session['curpath']
        pos=dir.rfind('/')
        if pos!=-1:
            dir=dir[:pos]
        switch_path(dir)    
    else:
        if len(session['curpath'])>1:
            switch_path(session['curpath']+'/'+dir)
        else:
            switch_path(session['curpath']+dir)

    return redirect('/')

@app.route('/')
def main():
    try:
        if 'curpath' in session:
            curpath=session['curpath']
        else:
            curpath='/'   
            switch_path(curpath)
        return render()
    
    except:
        curpath='/'   
        switch_path(curpath)
        return render()

if __name__ == "__main__":
    app.run()

