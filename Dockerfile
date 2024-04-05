# To run this Dockerfile from a Mac Apple M1 Sonoma
# Erro no Docker Desktop - Another application changed your Desktop configurations: https://github.com/docker/for-mac/issues/7109
# Solucao: 
#    jme1973 commented 2 weeks ago
#    This fixed it for me:
#    ln -sf /Applications/Docker.app/Contents/Resources/bin/docker-credential-ecr-login /usr/local/bin/docker-credential-ecr-login
#    
#    M1 MacBook Pro
#    Sonoma Version 14.3 (23D56)
#    Docker 4.28.0 (139021)
# docker build --platform linux/amd64 -t angelozero/py-backend .
# https://hub.docker.com/repository/docker/angelozero/backend-py/general
# docker run -p 8080:8080 -e SQLALCHEMY_DATABASE_URI=ELEPHANT_SQL_URL angelozero/backend-py
# docker run --platform linux/amd64 docker.io/angelozero/backend-py:latest

FROM python:3.11

WORKDIR /app_py

COPY . /app_py

RUN pip install --no-cache-dir virtualenv

RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

EXPOSE 8080

CMD ["/bin/bash", "-c", "source venv/bin/activate && python app.py"]