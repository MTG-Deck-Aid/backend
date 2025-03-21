# IMPORTANT FOR RUNNING THIS FILE

### In order to run this file an Auth0 token is needed. To avoid possible security issues the only way to retrieve it is to 
1. run the Heroku procfile and launch the localhost link 
1. Login into an account 
1. edit the URL to look like "http://localhost:3000/tests/get-token"
1. check Server terminal to see log where the auth token will be
1. Place the auth token inside the setup_and_teardown() functions header variable where the "\<Token\>"is sitting

## Now the test file can be properly executed