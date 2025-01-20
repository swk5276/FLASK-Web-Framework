from flask import Flask,request,redirect
import random

#Flask app 생성성
app = Flask(__name__)

#새로운 항목 ID 관리 (초기값 : 4)
nextId=4

#topic 데이터 저장 리스트(기본값으로 3개의 항목 포함)
topics = [
    {'id' : 1, 'title': 'html','body': 'html is ...'},
    {'id' : 2, 'title': 'css','body': 'css is ...'},
    {'id' : 3, 'title': 'javascript','body': 'javascript is ...'}
]

#html 탬플릿 생성 함수
def template(contents,content,id = None):
    contextUI = ''

    if id !=None:
        contextUI =f'''
                <li><a href="/update/{id}">update</a></h1></li>
                <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
                '''
    #전체 HTML 탬플릿 반환
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1> <!-- 메인 페이지로 이동 -->
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li> <!-- 새 항목 추가 링크 -->
                {contextUI}
            </ul>
        </body>
    </html>
    '''
#topic 목록을 가져와 html리스트로 변환
def getContents():
    liTags = ''
    #주제 리스트를 순회하며 각 항목의 링크를 html리스트로 추가가
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/"> {topic["title"]}</a></li>'
    return liTags

#메인 페이지
@app.route('/')
def index():        
    return template(getContents(),'<h2>Welcome</h2>Hello,WEB')

#topic 읽는 페이지
@app.route('/read/<int:id>/')
def read(id):
    title = ' '
    body = ' '
    #ID 기준 topic 검색색
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic ['body']
            newTopic = {'title': title, 'body':body}
            break
    # 선택한 주제 제목과 본문 표시 
    return template(getContents(),f'<h2>{title}</h2>{body}',id)

# topic 생성 페이지 (GET POST)
@app.route('/create/', methods=['GET','POST']) #
def create():
    if request.method == 'GET': #GET 요청
        #HTML 폼 반환
        content='''
            <form action="/create/" method = "POST">
                    <p><input type ="text" name="title" placeholder="title"></p>
                    <p><textarea name ="body" placeholder="body"></textarea></p>
                    <p><input type="submit" value="create"></p>
            </form> 
        '''
        return template(getContents(),content)
    
    elif request.method == 'POST': #POST 요청 : 데이터 처리리
        global nextId
        #사용자가 제출한 제목과 본문 가져오기기
        title = request.form['title']
        body = request.form['body']
        #새로운 topic 생성하여 리스트 추가가
        newTopic = {'id': nextId, 'title': title , 'body': body }
        topics.append(newTopic)
        # 새로운 topic redirect
        url = '/read/'+str(nextId)+'/'
        nextId = nextId+1
        return redirect(url)

# topic 수정 페이지 (GET POST)
@app.route('/update/<int:id>/', methods=['GET','POST']) #
def update(id):
    if request.method == 'GET': # GET 요청 : 기존 데이터와 함께 HTML폼 반환환
        title = ' '
        body = ' '
        # ID를 기준으로 검색색
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic ['body']
                newTopic = {'title': title, 'body':body}
                break    
        #HTML 폼 반환
        content = f'''
            <form action="/update/{id}" method = "POST">
                    <p><input type ="text" name="title" placeholder="title" value={title}></p>
                    <p><textarea name ="body" placeholder="body">{body}</textarea></p>
                    <p><input type="submit" value="update"></p>
            </form> 
        '''
        return template(getContents(),content)
    
    elif request.method == 'POST': #POST 요청 : 데이터 수정
        global nextId 
        title = request.form['title'] #수정 제목
        body = request.form['body'] #수정 본문
        #ID 기준 topic 검색하여 데이터 업데이트트
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/'+str(id)+'/'     
        return redirect(url)

# topic 삭제 페이지 (GET POST)
@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    #ID 기준 주제 검색 후 삭제제
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    #메인 페이지로 redirect
    return redirect('/')

#FLASK app 실행
app.run(port=5001, debug=True) #포트 5001 실행 / 디버그 모드 활성화화