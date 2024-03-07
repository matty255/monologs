
# Monolog

## 프로젝트 개요
`Monolog`는 사용자가 CK 에디터를 사용하여 블로그 포스트를 작성하고, JWT를 이용한 로그인 및 회원가입 기능을 통해 사용자 인증을 관리하는 동시에, 게시글을 올릴 수 있는 게시판을 제공하는 웹 애플리케이션입니다. 이 프로젝트는 Django 프레임워크를 기반으로 하며, TailwindCSS를 사용하여 스타일링을 합니다.

## 기능
- **CK 에디터를 통한 블로그 포스트 작성**: 사용자는 풍부한 텍스트 편집 기능을 제공하는 CK 에디터를 사용하여 블로그 포스트를 작성할 수 있습니다.
- **회원가입 및 로그인**: 회원으로 가입하면 게시글과 댓글을 쓸 수 있습니다.
- **게시판 기능**: 사용자는 자신의 블로그 포스트를 게시하고 다른 사용자의 포스트를 볼 수 있습니다.


## ERD
![Database ERD](./static/images/readme/erd.png)

- tags 중계 테이블
- GenericForeignKey를 사용해서 post와 comment에 like와 bookmark 추가

```
Table CustomUser {
  id int [pk, increment] // auto-increment
  username varchar
  email varchar
  profile_status varchar
  profile_message text
}

Table Tag {
  id int [pk, increment]
  name varchar [unique]
}

Table Post {
  id int [pk, increment]
  title varchar(100)
  summary  varchar(200)
  author_id int [ref: > CustomUser.id]
  content text
  thumbnail varchar
  created_at datetime
  updated_at datetime
}

Table Comment {
  id int [pk, increment]
  content text
  author_id int [ref: > CustomUser.id]
  created_at datetime
  updated_at datetime
  post_id int [ref: > Post.id]
  parent_id int [null, ref: > Comment.id] 
}

Table Like {
  id int [pk, increment]
  user_id int [ref: > CustomUser.id]
  content_type_id int
  object_id int
}

Table Bookmark {
  id int [pk, increment]
  user_id int [ref: > CustomUser.id]
  content_type_id int
  object_id int
}

Table Follow {
  id int [pk, increment]
  follower_id int [ref: > CustomUser.id]
  following_id int [ref: > CustomUser.id]
}

// M:N 관계인 Post와 Tag를 위한 중계 테이블
Table Post_Tags {
  post_id int [ref: > Post.id]
  tag_id int [ref: > Tag.id]
}

// GenericForeignKey를 직접적으로 표현하는 것은 dbdiagram.io에서 지원하지 않습니다.
// Like 및 Bookmark 모델에서 사용되는 content_type_id와 object_id는 
// 실제 구현시 ContentType 프레임워크와 연결되어야 하며, 여기서는 간략화하여 표현하였습니다.
```
## 설치 방법
프로젝트를 설치하고 실행하기 위한 단계별 지침은 다음과 같습니다.

1. **프로젝트 클론**:
    ```
    git clone
    cd Monolog
    ```

2. **가상 환경 설정 및 활성화**:
    ```
    python -m venv venv
    source venv/bin/activate
    ```

3. **필요한 패키지 설치**:
    ```
    pip install -r requirements.txt
    ```

4. **환경 변수 설정**:
    `secrets.json` 파일을 프로젝트 루트 디렉토리에 생성하고, 아래와 같이 `SECRET_KEY`를 설정합니다.
    ```json
    {
        "SECRET_KEY": "여기에_당신의_시크릿_키를_입력하세요"
    }
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

6. **run server**:
    ```
   python manage.py runserver
    ```


7. **custom commands**:
    ```
    ./commands.sh
    reinstall

    # 설치 후 가상환경이 deactivate 됩니다.
    ./commands.sh
    run
    ```

## 사용된 기술
- Django 
- Django-quill-editor
- Django-tailwind
- Django_browser_reload
- Django-ajax_select
- Tom Select

## 개발 환경 설정
개발을 시작하기 전에, 다음 도구들이 시스템에 설치되어 있어야 합니다:
- Python (3.8 이상)
- pip
- Git

