# API View
## Accounts
- /api/accounts/register/
### Send Request
```json
{
    "first_name" : "aakash",
    "last_name" : "Mahajan",
    "email" : "aakashmahajan25@gmail.com",
    "password" : "1234"
}
```
### Return Request
If email is not valid
```json
{
    "error": true,
    "mssg": "Invalid Email",
}
```
If email already exist
```json
{
    "error": true,
    "mssg": "Email Exist!",
}
```
If internal server error
```json
{
    "error": true,
    "mssg": "Internal Server Error",
}
```
Success Mssg
```json
{
    "error": false,
    "mssg": ""
}
```

- /api/accounts/login/
