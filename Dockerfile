# 기본 이미지로 python 3.12.2 버전 사용
FROM python:3.12.2

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 작업 디렉토리 설정
WORKDIR /app

# Node.js 설치
ARG NODE_MAJOR=18
RUN apt-get update \
    && apt-get install -y ca-certificates curl gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean

# AWS CLI 및 Gunicorn 설치
RUN pip install --no-cache-dir awscli gunicorn

# 애플리케이션 파일 및 의존성 복사 및 설치
COPY . .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Django Tailwind 설정 및 정적 파일 컴파일
RUN python manage.py tailwind install --no-input \
    && python manage.py tailwind build --no-input \
    && python manage.py collectstatic --no-input

# 수정된 라이브러리 파일 복사
COPY static/custom_django_quill/django_quill.js /usr/local/lib/python3.12/site-packages/django_quill/static/django_quill/
COPY static/custom_django_quill/widget.html /usr/local/lib/python3.12/site-packages/django_quill/templates/django_quill/

# COPY the launch.sh script into the image and set execute permissions
COPY launch.sh /app/
RUN chmod +x /app/launch.sh

# Set the CMD to run the launch script
CMD ["/app/launch.sh"]