## BEDS 24 - Statements Maker ##

This is the project structure

```
window/
    ├── init
    └── window_maker
utils/
    ├── init
    ├── api_handler
    ├── consts
    ├── logger
    ├── tools
    └── window_maker
beds24/
    ├── init
    └── beds_api_handler
app.py
README.md
```

#### Python proyect
Important note: Token file is not present in proyect due to project security. Create token file on beds24/ folder and with following structure:
```
{
    "token": null
    "valid_token": false,
    "refresh_token": null
}
```