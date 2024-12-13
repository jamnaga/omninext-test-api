Test tecnico per OmniNext utilizzando Serverless per il provisioning automatico dei servizi su AWS (API Gateway, Lambda e DynamoDB)

*Endpoint API:*
https://pj0s1icg33.execute-api.eu-central-1.amazonaws.com/dev/

*Metodi disponibili*
| Method | Name | Params |
|--------|------|--------|
|POST|createUser|userId: string, name: string|
|GET|getUserById/[userId]|userId: string|

*Deploy (Frankfurt):*
`sls deploy --region eu-central-1`
