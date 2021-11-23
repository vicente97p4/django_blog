# django_blog

공부하면서 만드는 장고 블로그

목표 기능  
1. 회원가입  
2. 댓글 작성, 수정, 삭제  
3. 게시글 검색  
4. 관리자 권한이 있는 계정은 블로그 작성 가능. 즉, 권한 설정 가능  
5. 복잡한 가입 절차가 필요 없는 소셜 로그인 기능  
6. 인터넷 상에서 접속 가능  
7. 보안을 위해 HTTPS 인증 받음  

- TDD로 진행  

개발하려는 항목에 대한 점검 사항을 테스트 코드로 만들고 그 테스트를 통과시키는 방식으로 개발 진행

> **내가 무엇을 하고 있는지 분명히 정의하고 개발을 시작하기 위해**  

> **종속성과 의존성이 낮은 모듈로 조합된 개발을 위해**  

> **다양한 예외상황에 대해 생각해보고 대처하여 완성도 높은 설계를 위해 TDD 개발 방식을 선택했다.**  

## 웹 페이지  

- Landing page  
- Blog page  
- 자기소개 page  
- blog, single_pages 2개의 앱으로 구성됨  

URL 구조

|페이지|URL|
|---|---|
|Landing page|도메인/|
|블로그 페이지 - 포스트 목록|도메인/blog/|
|블로그 페이지 - 포스트 상세|도메인/blog/포스트pk|
|자기소개 페이지|도메인/about_me|

## 모델 구조  

Post: 포스트의 형태 정의

블로그 기능을 위한 blog 앱, landing page와 자기소개 page를 위한 single_pages 앱으로 구성되어 있다.

- 다대일 관계  

여러 개의 모델이 하나의 모델에 연결되는 관계를 말한다.  

User - Post - Category와 User - Comment - Post가 있다.  

![이미지](./readme_img/relationN-1.PNG)

Post 모델은 author를 Foreign key로 두어 User와 연결한다.  

```buildoutcfg
author = models.ForeignKey(User, on_delete=models.SET_NULL)
```

- 다대다 관계  

모델이 여러 모델과 연결되는 관계를 말한다.  

Post - Tag가 있다.  

![이미지](./readme_img/relationN-N.PNG)

## 장고의 작동 구조  

장고로 만든 웹 사이트에서 일어나는 과정을 그린 것  

![이미지](https://media.vlpt.us/images/jcinsh/post/a6efe003-2522-4401-9661-8c8654d1f31f/%E1%84%8C%E1%85%A1%E1%86%BC%E1%84%80%E1%85%A91.png)  

1. 먼저 클라이언트(웹 브라우저)는 일련의 과정을 거쳐 장고 웹페이지가 있는 서버를 찾아간다.  

2. urls.py를 요청해 개발자가 써놓은 내용을 확인한다. urls.py에는 'A URL로 접속했을 때는 B 함수를 실행시킨다'는 내용이 기술되어있다.  

3. urls.py에서 언급하는 함수 또는 클래스는 views.py에서 정의한다.  

4. 장고에서는 자료의 형태를 정의한 클래스를 모델이라고 한다.  

5. models.py에서 정의한 모델에 맞게 DB에서 필요한 데이터를 가져온다.  

6. DB에서 가져온 자료를 템플릿의 빈 칸에 채워서 사용자의 웹 브라우저로 보낸다.  

- MTV 패턴이란  

장고로 만든 웹 사이트는 모델(model)로 자료의 형태를 정의하고, 뷰(view)로 어떤 자료를 어떤 동작으로 보여줄지 정의하고, 템플릿(template)으로 웹페이지에서 출력할 모습을 정의한다. 이러한 작동 구조를 줄여서 MTV 패턴이라고 부른다.  

이렇게 분리하여 웹 사이트 기능을 관리함으로써 백엔드 로직과 프런트엔드 디자인이 뒤죽박죽인 코드가 되어 어디서 무엇을 수정해야 할지 모르는 사태를 방지할 수 있다.  

### Migration  

- 데이터베이스에 적용시켜야 하는 변화에 대한 기록  

예를 들어 댓글 기능이 없던 블로그에 댓글 작성 기능을 추가했다고 하면 DB에 댓글을 저장하기 위한 Table이 필요하다.  

이를 DB에 반영해야 서버를 실행했을 때 웹 사이트에 추가한 댓글 기능을 사용할 수 있다.  

※ 장고를 처음 시작할 때 아무 기능도 만들지 않았는데 적용해야 할 migration이 존재한다.(3.2.9버전 기준으로 18개 존재)  

장고는 새 프로젝트를 생성할 때 DB에 기본적으로 필요한 Table을 미리 마련해두기 때문이다.  

### SQLite3  

장고는 기본적으로 SQLite3를 DB로 사용한다.  

SQLite3의 특징은 파일 하나로 관리하는 DB라는 점인데, MySQL, MongoDB, PostgreSQL 등 다른 DB들은 복잡한 설치 과정을 거쳐야 한다.  

또한 백업을 하기 위해서는 DB에 대한 지식이 추가적으로 더 필요하다.  

하지만 SQLite3는 파일 하나만 관리하면 되고, 백업을 할 때도 파일 하나만 안전한 곳에 복사해두면 된다. 이런 간편함 때문에 장고에서는 SQLite3를 기본 DB로 사용한다.  

- 단점  

SQLite3는 파일 기반의 DB이기 때문에 읽고 쓰기가 빈번하게 일어나는 대형 프로젝트에는 불리하다.  

예를 들어 수천, 수만 명의 사용자가 동시에 몰리는 웹 사이트에는 적합하지 않다. 이럴 경우, 고성능의 다른 DB를 사용해야 한다.  

이 프로젝트에서는 SQLite3를 사용하여 DB를 다루고 배포 전 PostgreSQL로 전환한다.  

- 깃에서 DB를 버전관리 하지 않도록 .gitignore에 등록한다.  

로컬에서 테스트를 진행하며 개발을 진행하고 개발이 끝나면 프로젝트 파일 전체를 깃허브를 통해 옮긴다.  

그런데 db.sqlite3까지 옮기게 되면 테스트 과정에서 만든 정보가 모두 서버로 넘어가게 된다.  

만일 이미 운영 중인 서버에 db.sqlite3가 있다면 로컬에서 온 db.sqlite3와 충돌을 일으킬 것이고, 오류가 발생할 것이다.  

이를 방지하기 위해 db.sqlite3는 깃으로 관리하지 않는다.

### 앱  

장고 프로젝트는 보통 1개 이상의 앱을 가진다. 여기서 앱은 특정 기능을 수행하는 단위 모듈을 의미한다.  

안드로이드 애플리케이션을 의미하는 앱과는 다르다.  

### 모델  

장고의 장점 중 하나는 모델을 이용해 장고 웹 프레임워크 안에서 DB를 관리할 수 있다는 점이다.  

모델은 데이터를 저장하기 위한 하나의 단위이다.  

일반적으로 DB를 다루려면 SQL 등의 언어를 배워야 하는데, 장고의 모델을 이용하면 CRUD 기능을 쉽게 구현할 수 있고 여러가지 폼도 쉽게 만들 수 있다.  

### Admin에 모델 적용 순서  

1. 프로젝트에 있는 settings.py에 INSTALLED_APPS 리스트에 앱 추가  
2. models.py에 원하는 모델 작성  
3. makemigrations, migrate  
4. 앱에 있는 admin.py에 admin.site.register(모델(클래스명))  

장고의 모델을 만들면 기본적으로 pk필드가 만들어진다.  

pk는 각 레코드에 대한 고유값이다. 처음 pk 값은 1이고 1씩 증가한다.  

### urls.py  

사용자가 장고로 개발한 웹 사이트에 방문했을 때 어떤 페이지로 들어가야 하는지 알려준다. 즉, 이정표와 같은 역할을 한다.  

장고 프로젝트 안에 있는 urls.py에 urlpatterns 리스트에 path('url', include('해당 url로 왔을 때 실행할 동작이 명시되어있는 파일명')) 추가해준다.

### views  

urls.py에 들어갈 함수나 클래스 등을 정의한다.  

FBV(Function Based View)는 함수에 기반을 둔 방법이다. 함수를 직접 만들어서 원하는 기능을 직접 구현할 수 있는 장점이 있다.  

CBV(Class Based View)는 장고가 제공하는 클래스를 활용해 구현하는 방법이다. 장고는 웹 개발 시 반복적으로 많이 구현하는 것들을 클래스로 미리 만들어서 제공하는데, 이 클래스들을 이용하는 방법이다.  

### 사용한 CBV  

- ListView  

여러 레코드를 목록 형태로 보여줄 때 사용한다.

ListView는 모델명 뒤에 _list.html 이 붙은 html 파일을 기본 템플릿으로 사용한다. 모델명_list.html 파일이 필요하다.  

예를 들어 Post 모델을 사용하면 Post_list.html 파일이 필요하다.  

해당 파일을 만들어도 되고, 해당 클래스에서 template_name을 지정해줘도 된다.  

또한 템플릿에서 ListView로 만든 클래스의 모델 객체를 가져오려면 object_list 명령어를 사용하면 된다. 또는 모델명_list 명령어를 써도 자동으로 인식한다.  

- DetailView  

한 레코드를 자세히 보여줄 때 사용한다.  

모델명 뒤에 _detail.html 이 붙은 html 파일을 기본 템플릿으로 사용한다. 모델명_detail.html 파일이 필요하다.  

예를 들어 Post 모델을 사용하면 Post_detail.html 파일이 필요하다. 

역시 해당 클래스에서 template_name을 지정해줘도 된다.  

또한 템플릿에서 DetailView로 만든 클래스의 모델 객체를 가져오려면 object_detail 명령어를 사용하면 된다. 또는 모델명_detail 명령어를 써도 자동으로 인식한다.  

### template  

데이터를 채워넣고 사용자에게 보여주기 위한 틀이다.  

앱 폴더에 있는 templates 폴더의 html 파일은 정적인 파일이 아니다. templates 폴더에 css, js 파일을 함께 넣어 두어도 해당 파일에 접근할 수 없다.  

css, js 파일은 고정된 내용만 제공하면 되므로 특정 URL로 접근하면 해당 css, js 파일을 제공할 수 있도록 설정한다.  

count() 함수보다 exists() 함수가 서버에 부담을 덜 준다.

템플릿에서 함수를 호출할 때는 괄호를 사용하지 않는다.

### static, 미디어 사용  

css, js 파일은 고정된 내용만 제공하면 되므로 특정 URL로 접근하면 해당 css, js 파일을 제공할 수 있도록 설정한다.  

templates이 있는 곳. 즉, html 파일이 있는 디렉토리에 바로 css, js 파일을 두면 사용할 수 없다.  

templates는 정적이 아닌 동적 파일로 간주하기 때문이다.  

따라서 앱이 디렉토리 하위에 static 디렉토리를 만들어서 css, js 파일을 두고 사용한다.

```
STATIC_URL = '/static/'
```

도메인 뒤에 /static/이라는 경로가 따라오면 static 파일을 사용하겠다는 의미이다.

---

장고는 이미지 업로드를 위한 ImageField를 제공한다.  

ImageField를 사용하기 위해 사용자가 업로드할 이미지를 저장할 위치를 먼저 설정해야 한다.  

settings.py에 

```
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '_media')
```

를 추가한다.  

이미지 파일은 MEDIA_ROOT 설정을 통해 프로젝트 폴더 아래 _media 라는 이름의 폴더를 만들고 그 안에 저장하도록 한다.  

그리고 MEDIA_URL은 /media/로 지정했다. 웹 브라우저에서 도메인 뒤에 /media/라는 경로가 따라오면 미디어 파일을 사용하겠다는 의미이다.  

또한 ImageField를 사용하기 위해서는 Pillow 라이브러리가 필요하다.

```buildoutcfg
pip install Pillow
```

로 Pillow를 가상환경에 설치 후 migration 한다.  

이제 media 가 url에 있을 때 인식시키기 위하여 django_plog_prj/urls.py에 

```buildoutcfg
from django.conf import settings
from django.conf import path, include

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

를 추가해준다.  

### Template 모듈화  

디자인이 일관되게 유지되어야 편리한 경우가 많다.  

하나의 페이지에 메인 영역을 뺀 나머지 영역을 만들어 놓고 그 부분만 채워주면 편리하게 쓸 수 있다.  

모듈화한 template에 따로 채워넣어야 하는 부분을 아래와 같이 {% block 블록명 %}, {% endblock %}으로 감싸준다.  

```buildoutcfg
<div class="container my-3">
    <div class="row">
        <div class="col-md-8 col-lg-9" id="main-area">
            {% block 블록명 %}
            {% endblock %}
        </div>
    </div>
</div>
```

채워넣을 내용이 있는 html 문서에서는 다음과 같이 {% extends '파일명' %}을 선언해주고 전달할 내용을 {% block 블록명 %}, {% endblock %}으로 감싸준다.  

```buildoutcfg
{% extends 'blog/base.html' %}

{% block 블록명 %}
내용
{% endblock %}
```

만일 다음과 같이 블록 사이에 값이 들어 있다면, 해당 블록에 해당하는 값이 채워지지 않을 경우 나타나는 기본값임을 의미한다.  

```buildoutcfg
{% block 블록명 %}
안 채워졌을 경우 나타나는 기본값
{% endblock %}
```

템플릿을 붙여넣고 싶을 때 원하는 위치에 아래 코드를 입력한다.  

```buildoutcfg
{% include '템플릿' %}
```

