# van_athena - Query Athena using AI and plain English.

This is customisation of awesome library (vanna.ai)[https://github.com/vanna-ai/vanna] with following changes 
- Using everything locally running except LLM. LLM used is deep-seek V3. It is cheap and works really well for this
- Using Athena for SQL, using boto3 APIs to query Athena, you can use [AWS data wrangler](https://github.com/aws/aws-sdk-pandas) as well for query - but it is heavy module
- Using custom Authentication - very simple user/password - also changed logo image etc...

# Things to consider
- in 
