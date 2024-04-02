# Docker Backend
- Instale [Docker Desktop](https://docs.docker.com/get-docker/)
- Se caso seu sistema operacional for M1 MacBook Pro Sonoma Version e este erro estiver acontecendo `Another application changed your Desktop configurations`
    ```shell
        # Resposta do usuario jme1973 com a solucão: 
        #    This fixed it for me:
        #    ln -sf /Applications/Docker.app/Contents/Resources/bin/docker-credential-ecr-login /usr/local/bin/docker-credential-ecr-login

        #    M1 MacBook Pro
        #    Sonoma Version 14.3 (23D56)
        #    Docker 4.28.0 (139021)
    ```
    - *Fonte: [Issue: Another application changed your Desktop configurations](https://github.com/docker/for-mac/issues/7109)*
- O repositório se encontra em [Docker Hub angelozero/backend-py](https://hub.docker.com/repository/docker/angelozero/backend-py/general)
- Para executar digite `docker run -p 8080:8080 -e SQLALCHEMY_DATABASE_URI=ELEPHANT_SQL_URL angelozero/backend-py`
    - Lembre-se de alterar `ELEPHANT_SQL_URL` para a url gerada em [ElephantSQL](https://www.elephantsql.com/) e não se esqueça de alterar a url criadada de `postgres://...` para `postgresql://...`