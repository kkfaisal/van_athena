## van_athena - Query Athena using AI and plain English.

This is customisation of awesome library [vanna.ai](https://github.com/vanna-ai/vanna) with following changes 
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
- change `athena_utils` to update aws profile, and s3 bucket names
- change `init.sql` to set up username and password for postgres vector db.
- Update vector db connecytion strings in `train.py` and `app.py` accordingly
- in `train_doc_1.txt` add documentions you have about your tables
- in `train.py` change the SQL statement to extract coulm details of table as you needed - add more tables or cols
- For first time run use `docker-compose up --build` which build the Dockerfile
- Once containers are up, change athena db and tabl names in `train.py`, add any docs in `train_doc1.txt` and then run train.py
To run it enter to the docker container
```
docker exec -it vannaai-vanna-app-1 bash
python train_vanna.py
```
- Once training is done data is feeded to vector store, then restart the app service `docker-compose restart vanna-app`
- Now the UI is available in `localhost:5000`

## Screenshots
## Asking Questions
![alt text](https://github.com/kkfaisal/van_athena/blob/main/img/git_img_1.png)

## Add SQL pair to vector store 
![alt text](https://github.com/kkfaisal/van_athena/blob/main/img/git_img_2.png)

## Redraw Chart
![alt text](https://github.com/kkfaisal/van_athena/blob/main/img/git_img_3.png)

## Training Data
![alt text](https://github.com/kkfaisal/van_athena/blob/main/img/git_img_4.png)

## Deelete Training Data
You can delete each entry one by one. If you want to delete in bulk got to Postgres vector DB and delete entries using SQL
![alt text](https://github.com/kkfaisal/van_athena/blob/main/img/git_img_5.png)

