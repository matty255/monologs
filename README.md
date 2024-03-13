
# Monologs

## 프로젝트 개요

배포 주소 : http://43.200.237.70:8000/

- Django Monolithic Blog Project
`monologs`는 사용자가 블로그 포스트를 작성하고, 로그인 및 회원가입 기능을 통해 사용자 인증을 관리하는 동시에, 게시글을 올릴 수 있는 게시판을 제공하는 웹 애플리케이션입니다. AI가 초안 작성을 도와주니다.

## 편의 기능

- **블로그 포스트 작성**
  블로그 포스트 작성은 편리한 quill 에디터를 통해 이루어집니다. quill은 이미지 업로드와 동영상을 쉽게 임베드할 수 있는 리치 텍스트 에디터로, 사용자 친화적인 인터페이스를 제공하여 누구나 쉽게 글을 작성할 수 있게 합니다. 풍부한 텍스트 편집 기능을 제공하여 복잡한 포맷의 포스트도 손쉽게 작성할 수 있습니다.

- **회원가입 및 로그인**
  사용자는 간단한 회원가입 및 로그인 절차를 통해 플랫폼에 액세스할 수 있습니다. 회원가입을 완료하면, 사용자는 개인화된 경험을 즐길 수 있으며 게시글 및 댓글 작성 등의 기능을 이용할 수 있습니다. 안전하고 편리한 인증 과정을 통해 사용자 정보를 보호합니다.

- **프로필 이미지 기능**
  사용자는 이미지를 크롭하여 프로필로 사용할 수 있습니다. 프로필이 없으면 기본 프로필 이미지가 주어집니다.

- **게시판 기능**
  사용자는 자신이 작성한 블로그 포스트를 게시할 수 있으며, 다른 사용자의 포스트도 열람할 수 있습니다. 이 게시판은 사용자 간의 상호작용을 촉진하고, 다양한 주제와 아이디어를 공유하는 공간으로 기능합니다. 사용자는 흥미로운 내용을 쉽게 찾아볼 수 있습니다.

- **팔로우 기능**
  관심 있는 다른 사용자를 팔로우할 수 있는 기능을 제공합니다. 이를 통해 사용자는 팔로우한 다른 사용자의 최신 포스트를 쉽게 확인할 수 있으며, 개인적인 네트워크를 확장할 수 있습니다. 팔로우 시스템은 사용자 간의 커뮤니티 형성에 기여합니다.

- **공유 기능**
  사용자는 자신의 퍼블릭 프로필 페이지를 손쉽게 공유할 수 있습니다. 이를 통해 더 많은 사람들과 자신의 포스트를 공유하고, 개인 브랜딩을 강화할 수 있습니다. 소셜 미디어 통합 기능을 통해 다양한 플랫폼에서 공유가 가능합니다.

- **AI 글 작성**
  AI 기반의 글 초안 작성 기능을 제공하여 사용자가 보다 쉽게 포스트를 시작할 수 있게 돕습니다. 이 기능은 사용자의 작성 스타일을 학습하여, 개인화된 글쓰기 도움을 제공합니다. 커스텀 설정을 통해 다양한 글쓰기 요구에 맞춤화된 도움을 받을 수 있습니다.

- **북마크**
  사용자는 관심 있는 글이나 댓글을 북마크하여, 나중에 쉽게 찾아볼 수 있습니다. 이 기능은 사용자가 정보를 효율적으로 관리하고, 중요한 내용을 빠르게 접근할 수 있도록 합니다. 사용자의 프라이빗 프로필 페이지에서 북마크한 내용을 확인할 수 있습니다.

- **Like**
  사용자는 글이나 댓글에 '좋아요'를 표시할 수 있습니다. 이는 긍정적인 피드백을 제공하고, 커뮤니티 내에서 상호작용을 촉진합니다. 자신의 컨텐츠에는 '좋아요'를 할 수 없으며, 이는 공정한 상호작용을 유도합니다.

- **카테고리 편집**
  사용자는 퍼블릭 프로필 페이지에서 자신의 블로그를 더욱 전문적으로 보이게 하기 위해 카테고리를 편집할 수 있습니다. 이를 통해 방문자들이 관심 있는 내용을 더 쉽게 찾을 수 있도록 돕습니다. 사용자는 자신의 포스트를 주제별로 구분하여 표시할 수 있습니다.

- **태그 필터 기능**
  사용자는 자신이 선호하는 태그에 따라 포스트를 필터링할 수 있는 검색 페이지를 이용할 수 있습니다. 이 기능을 통해 관심 있는 주제의 글만을 모아볼 수 있으며, 사용자의 취향과 관심사에 맞춘 콘텐츠를 쉽게 발견할 수 있습니다.



## 효율성 향상 및 최적화

- **사이트 내 이미지 WebP 변환기**
  관리자 페이지에는 이미지를 WebP 형식으로 자동 변환하는 컨버터가 탑재되어 있습니다. 이는 웹 성능 최적화의 핵심 요소로, 페이지 로딩 시간을 단축시키고 사용자 경험을 개선합니다.

- **업로드 되는 이미지 자동 WebP 변환 및 이름 변경**
  보안과 성능을 동시에 고려하여, 업로드되는 이미지들(썸네일, 프로필 사진)은 자동으로 WebP 형식으로 변환되며, 파일명도 변경됩니다. 이 과정은 서버 자원의 효율적 사용과 빠른 콘텐츠 전송을 목적으로 합니다.

- **Quill 에디터 내에서의 이미지 압축**
  Webp을 별도의 설정 없이 일괄변환하면 동적인 이미지를 얻을 수 없기 때문에, Quill 에디터 내에 업로드되는 이미지는 Webp 변환을 하지 않고, 다양한 확장자의 이미지를 지원하게 두었습니다. 다만, 이미지 용량을 제한하고 quill-image-compress로 압축을 합니다. 

- **템플릿 내 컴포넌트 분리**
  재사용 가능한 컴포넌트 단위로 코드를 분리하여 `include` 폴더에 저장합니다. 코드의 가독성을 높이고, 개발자가 유지보수를 보다 쉽게 할 수 있도록 했습니다.

- **커스텀 명령어**
  Django 몬롤로그 프로젝트에 최적화된 커스텀 명령어를 제공하여, 커맨드 입력과정을 자동화하고 효율을 증가시킵니다. 특히나 tailwind를 따로 같이 켜야 되는 프로젝트에서 터미널 2개 켜는 시간을 다 줄이면 3시간은 나올거 같습니다. 이러한 커스텀 명령어는 Bash 스크립트를 통해 실행되며, 반복 작업을 간소화합니다.

- **브라우저 핫 리로드**
  cdn이 아닌, Django-Tailwind와 npm을 사용하여 프로젝트 내에서 Tailwind CSS의 플러그인들을 활용할 수 있게 했습니다. 개발 중인 클라이언트 사이드 코드에 대해 페이지를 새로 고침하지 않고도 실시간으로 변경 사항을 반영할 수 있는 환경을 제공합니다. 역시 새로고침 하는 시간을 줄여서 기능을 더 만들 수 있게 합니다.

- **Docker Compose를 이용한 컨테이너 오케스트레이션**
  Docker Compose를 활용한 컨테이너화는 복수의 서비스가 결합된 애플리케이션을 효율적으로 관리하고 배포할 수 있는 강력한 방법입니다. 본 프로젝트에서는 Django 애플리케이션과 Tailwind CSS를 포함하는 독립적인 환경을 단일 컨테이너 내에서 구성하고 관리합니다. 이러한 컨테이너화는 배포 과정을 대폭 간소화하며, DockerHub를 통한 공유는 프로젝트의 재사용성과 확장성을 높입니다.
 

- **AWS Lightsail을 통한 배포**
  DockerHub와 AWS Lightsail을 연동하여 애플리케이션을 배포했니다. 이 방법은 효율적이며 비용 효과적인 서버 관리를 가능하게 합니다. 아직은 무료이니까요. 단, 정보수집의 부족으로 nginx가 설정되어 있지 않기에 현재 HTTPS가 아닌 HTTP를 사용하고 있어 보안상 위험이 있습니다. 테스트 배포는 내일 중지 됩니다. 


## 엔티티 관계 다이어그램(ERD)

![데이터베이스 ERD](./static/images/readme/erd-final-final.webp)

- **Post_Tags 중계 테이블**을 사용하여 `CustomUser`와 `Tag` 사이의 다대다(m:n) 관계를 설정합니다. 이 구조는 한 게시물이 여러 태그를 가질 수 있으며, 한 태그가 여러 게시물에 할당될 수 있음을 나타냅니다.
  
- **GenericForeignKey**를 활용하여 `Post`와 `Comment`에 `Like`와 `Bookmark` 기능을 추가합니다. 이 기능들은 Mixin을 통해 재사용 가능하게 구현되어, 코드의 재사용성과 확장성을 높이며 다형성을 활용한 관계 설정을 가능하게 합니다.

- `Comment`의 삭제는 실제 인스턴스를 삭제하는 대신 내용을 오버라이드하고, 이를 클라이언트 측에서 처리하여 사용자에게 삭제된 것처럼 보이게 합니다. 이 방법은 데이터의 무결성을 유지하며, 필요시 복구할 수 있는 가능성을 열어둡니다.

- **CustomUser 모델의 profile_picture**는 이미지 크롭 기능과 연동되어 있으며, `OneToOneField`를 사용하여 사용자당 하나의 프로필 사진만을 가지도록 설정합니다. 이 관계는 데이터베이스 설계에서 1:1 관계를 나타내며, 사용자 프로필과 밀접하게 연결된 데이터의 일관성을 보장합니다.

- `Category`는 `CustomUser`와 다대일(N:1) 관계로 설정되어 있어, 한 명의 사용자가 여러 카테고리를 생성할 수 있습니다. 반면, `Post`는 `Category`와 다대일(N:1) 관계에 있어, 여러 게시물이 하나의 카테고리에 속할 수 있음을 나타냅니다. 이러한 구조는 웹 애플리케이션에서 컨텐츠의 분류 및 조직화를 용이하게 합니다.
- 
- `Like`와 `Bookmark`모델은 ERD에서 그 관게가 잘 나타나지 않는데, 어떤 모델의 인스턴스에도 '좋아요'나 '북마크'를 할 수 있는 범용성과 다형성을 지원하기 위해 이렇게 만들었습니다. 여러 모델에 걸쳐 재사용 가능해야 하기 때문에 Django의 `ContentType` 프레임워크를 사용하여, `mixin`으로 사용합니다.


## 폴더 트리

```
📦accounts
 ┣ 📜admin.py
 ┣ 📜apps.py
 ┣ 📜context_processors.py
 ┣ 📜forms.py
 ┣ 📜mixins.py
 ┣ 📜models.py
 ┣ 📜tests.py
 ┣ 📜urls.py
 ┣ 📜views.py
 ┗ 📜__init__.py
 📦blog
 ┣ 📜admin.py
 ┣ 📜apps.py
 ┣ 📜forms.py
 ┣ 📜lookups.py
 ┣ 📜mixins.py
 ┣ 📜models.py
 ┣ 📜signals.py
 ┣ 📜tests.py
 ┣ 📜urls.py
 ┣ 📜views.py
 ┗ 📜__init__.py
 📦config
 ┣ 📜asgi.py
 ┣ 📜settings.py
 ┣ 📜test_settings.py
 ┣ 📜urls.py
 ┣ 📜wsgi.py
 ┗ 📜__init__.py
 📦main
 ┣ 📜admin.py
 ┣ 📜apps.py
 ┣ 📜mixins.py
 ┣ 📜models.py
 ┣ 📜tests.py
 ┣ 📜urls.py
 ┣ 📜utils.py
 ┣ 📜views.py
 ┗ 📜__init__.py
 📦static
 ┣ 📂css
 ┃ ┣ 📜style-exgamples.css
 ┃ ┗ 📜styles.css
 ┣ 📂custom_django_quill
 ┃ ┣ 📜django_quill.js
 ┃ ┗ 📜widget.html
 ┣ 📂images
 ┃ ┣ 📂banners
 ┃ ┃ ┣ 📜background.webp
 ┃ ┃ ┣ 📜darkmode-background.webp
 ┃ ┃ ┣ 📜erd-final.webp
 ┃ ┃ ┗ 📜profile-header.webp
 ┃ ┣ 📂logos
 ┃ ┃ ┣ 📜bird-logo.webp
 ┃ ┃ ┣ 📜dark-logo.webp
 ┃ ┃ ┣ 📜favicon.ico
 ┃ ┃ ┣ 📜hr-logo.webp
 ┃ ┃ ┗ 📜picture-default.webp
 ┃ ┗ 📂readme
 ┃ ┃ ┗ 📜erd-final-final.webp
 ┗ 📂js
 ┃ ┣ 📜crop.js
 ┃ ┣ 📜easyQuill.js
 ┃ ┣ 📜prompt.js
 ┃ ┗ 📜utils.js
📦templates
 ┣ 📂accounts
 ┃ ┣ 📂include
 ┃ ┃ ┣ 📜crop.html
 ┃ ┃ ┣ 📜following_list.html
 ┃ ┃ ┗ 📜user_following_list.html
 ┃ ┣ 📜category_create.html
 ┃ ┣ 📜login.html
 ┃ ┣ 📜private_profile.html
 ┃ ┣ 📜public-profile-category.html
 ┃ ┣ 📜public_profile.html
 ┃ ┣ 📜register.html
 ┃ ┗ 📜user_confirm_delete.html
 ┣ 📂blog
 ┃ ┣ 📂include
 ┃ ┃ ┣ 📜comment_confirm_delete.html
 ┃ ┃ ┣ 📜comment_form.html
 ┃ ┃ ┣ 📜comment_list.html
 ┃ ┃ ┣ 📜comment_update_form.html
 ┃ ┃ ┣ 📜post_confirm_delete.html
 ┃ ┃ ┣ 📜reply_form.html
 ┃ ┃ ┣ 📜reply_update_form.html
 ┃ ┃ ┗ 📜search_form.html
 ┃ ┣ 📜blog_detail.html
 ┃ ┣ 📜blog_list.html
 ┃ ┣ 📜post_create.html
 ┃ ┣ 📜post_update.html
 ┃ ┗ 📜search_results.html
 ┣ 📂main
 ┃ ┣ 📜about.html
 ┃ ┗ 📜index.html
 ┣ 📜base.html
 ┗ 📜custom_404.html
 📦theme
 ┣ 📂static
 ┃ ┣ 📂css
 ┃ ┃ ┗ 📂dist
 ┃ ┃ ┃ ┗ 📜styles.css
 ┃ ┗ 📂fonts
 ┃ ┃ ┣ 📜HappinessSansVF.ttf
 ┃ ┃ ┣ 📜nanum-hippie.ttf
 ┃ ┃ ┣ 📜nanum-white-tail.ttf
 ┃ ┃ ┗ 📜NanumSquareNeo-Variable.ttf
 ┣ 📂static_src
 ┃ ┣ 📂node_modules
 ┃ ┃ ┣ 📂.bin
 ┃ ┃ ┃ ┣ 📜bin.mjs
 ┃ ┃ ┃ ┣ 📜LICENSE
 ┃ ┃ ┃ ┣ 📜package.json
 ┃ ┃ ┃ ┣ 📜README.md
 ┃ ┃ ┃ ┗ 📜util.js
 ┃ ┃ ┗ 📜.package-lock.json
 ┃ ┣ 📂src
 ┃ ┃ ┗ 📜styles.css
 ┃ ┣ 📜.gitignore
 ┃ ┣ 📜package-lock.json
 ┃ ┣ 📜package.json
 ┃ ┣ 📜postcss.config.js
 ┃ ┗ 📜tailwind.config.js
 ┣ 📂templates
 ┃ ┗ 📜base.html
 ┣ 📜apps.py
 ┗ 📜__init__.py
┣ 📜.gitignore
┣ 📜commands.sh
┣ 📜db.sqlite3
┣ 📜manage.py
┣ 📜README.md
┣ 📜requirements.txt
```



# 배포 방법
```
http://43.200.237.70:8000/

# AWS lightsail 인스턴스에 docker, docker compose 설치
# SSH로 인스턴스의 루트 경로에 docker-compose.yml 전송
# 로컬에서 docker image를 만들어서 dockerHub에 push 한 후에

docker pull 유저이름/django-app:web-latest
docker-compose up -d

# 로컬에서 도커 빌드 시
docker-compose up -d 
docker build -t 유저이름/django-app:web-latest .

docker push 유저이름/django-app:web-latest

```
## WBS

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title       Django Monolithic Blog Development Schedule

    section 계획
    WBS 생성              :done,    wbs, 2024-03-02, 1d
    요구사항 분석          :done,    req, after wbs, 2d
    기획                  :done,    req, after wbs, 1d
    
    section 설계
    ERD 생성              :done,    erd, 2024-03-03, 1d
    모델 관계 설정         :done     uides, after proto, 2d

    section 개발
    URL 디자인            :done,    urldes, 2024-03-05, 1d
    CRUD 구현             :done,    crud, after urldes, 2d

    section UI 제작 및 추가 기능 
    백엔드 추가 기능           :done         backend, 2024-03-08, 3d
    피그마 디자인             :done     backend, 2024-03-08, 3d
    프론트엔드 기능            :done        backend, 2024-03-08, 3d

    section 테스트 & 배포
    테스팅                :done         test, 2024-03-10, 2d
    배포                  :done       deploy, after test, 1d
    
    section 종료
    프로젝트 종료          :done       end, 2024-03-11, 2d
```

## figma

- 와이어프레임(제작 중)
[피그마](https://www.figma.com/files/project/212207199/monologs?fuid=1012359410667987596)

- 디자인

## 설치 방법
프로젝트를 설치하고 실행하기 위한 단계별 지침은 다음과 같습니다.

1. **프로젝트 클론**:
    ```
    git clone
    cd monologs
    ```

2. **가상 환경 생성 및 활성화**:
    ```
    python -m venv venv
    # custom commands는 7번으로

    source venv/bin/activate

    ```

3. **필요한 패키지 설치**:
    ```
    pip install -r requirements.txt
    ```

4. **환경 변수 설정**:
    `.env` 파일을 프로젝트 루트 디렉토리에 생성하고, 아래와 같이 `SECRET_KEY`를 설정합니다.
    ```
    SECRET_KEY: "여기에_당신의_시크릿_키를_입력하세요"
    DEBUG=True
    ```

5. **가상환경 실행**:
    ```
    # git bash
    source ./venv/Scripts/activate
    ```

    ```
    # powerShall
    ./venv/Scripts/activate
    ```

6. **기본 커맨드(PowerShell)**:
    ```
   python manage.py runserver
    ```
    **다른 터미널에서 동시 실행**
    ```
    python manage.py tailwind start
    ```


7. **custom commands(Git Bash)**:
    ```
    ./commands.sh
    reinstall

    ./commands.sh
    add_admin(admin 유저 생성)

    # 설치 후 가상환경이 deactivate 됩니다.
    # ./ 세션 내 실행
    # . `공백` 인스턴스 내 실행
    ./commands.sh
    run
    ```

## 사용된 기술
- Django 
- Pillow
- Django-quill-editor
- Django-image-cropping
- Django-tailwind
- Django_browser_reload
- Django-ajax_select
- Tom Select
- daisyUI
- google-auth 
- google-auth-oauthlib 
- requests 
- google-analytics-data
- django-tree-queries
- jsTree
- django-environ


## 테스트 주소
```

```


## 개발 환경 설정
개발을 시작하기 전에, 다음 도구들이 시스템에 설치되어 있어야 합니다:
- Python (3.8 이상)
- Node.js (18.18 이상)
- pip
- Git

## 트러블 슈팅

### 1. django-quill-editor custom
ai 서비스를 위해, 전역 객체에 접근. 한국
패키지를 뜯기는 그러니까
docker compose

### 2. django-tailwind docker image 설성
1에서 뜯은 docker compose로 tailwind도 말려듦


### 3. AWS Lightsail instance
배포를 위해 컨테이너 설정
docker compose 오케스트레이션

instance로 전환

### 4. Docker login


### 5. mix-in Circular import
앱 전체의 다양한 콘텐츠 유형 간의 상호 참조가 필요한 Like, Bookmark를 코드의 모듈성과 재사용성을 강화하기 위해 우리는 믹스인 기반 접근 방식을 채택했습니다,
그래서 모든 콘텐츠에 대한 좋아요 및 북마크 상태를 확인하기 위한 로직을 만들고 이걸 content type이랑 object id를 가지고 어디에서나 쓸수 있게 LikeMixin. BookmarkMixin 이라는 이름으로 캡슐화했습니다.
그런데 이걸 실제 모델 내에서 쓰려니 Circular import 순환참조 문제가 발생하였습니다.

그래서 채택한 방법, 믹스인에서 Django의 ContentType 라이브러리가 가지고 있는 apps.get_model 동적 모델 검색을 사용해서 모델 클래스가 런타임에 모델을 직접 가져오게 해서 순환 종속성을 방지했습니다.



