## van_athena - Query Athena using AI and plain English.

This is customisation of awesome library (vanna.ai)[https://github.com/vanna-ai/vanna] with following changes 
- Using everything locally running except LLM. LLM used is deep-seek V3. It is cheap and works really well for this
- Using Athena for SQL, using boto3 APIs to query Athena, you can use [AWS data wrangler](https://github.com/aws/aws-sdk-pandas) as well for query - but it is heavy module
- Using custom Authentication - very simple user/password - also changed logo image etc...

## Things to consider
- `pg_vector` is used as vector store and is created and initiated while `docker-compose up`
- If you want to use aws credential keys instead of profile add those in `docker-compose` like this :
```
services:
  vanna-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_DEFAULT_REGION=me-south-1
    volumes:
      - .:/app
    extra_hosts:
      - "host.docker.internal:host-gateway"
    depends_on:
      - postgres-vector
```
- If you want to change pg vector db/user details change in `init.sql`
## How to run

- For first time run use `docker-compose up --build` which build the Dockerfile
- Once containers are up, change athena db and tabl names in `train.py`, add any docs in `train_doc1.txt` and then run train.py
To run it enter to the docker container
```
docker exec -it vannaai-vanna-app-1 bash
python train_vanna.py
```
- Once training is done data is feeded to vector store, then restart the app service `docker-compose restart vanna-app`
- Now the UI is available in `localhost:5000`

  https://www.awesomescreenshot.com/video/35579541?key=45b42367030bd3235ae59e5b216d7de7
