## BEDS 24 - Statements Maker ##

#### Installation
```
pip install -r requirements.txt
```

#### Run app
```
py run.py
```

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
    └── exceptions
app_api_handlers/
    ├── init
    ├── beds_api_handler
    ├── generic_handler
    ├── properties
    ├── token
    └── xero_api_handler
code_updates/
    ├── init
    └── git_process
handler/
    ├── init
    └── app_handler
statement_maker/
    ├── init
    ├── property_rules
    └── statement_maker
xero/
    └── TBD
app.py
run.py
README.md
requirements.txt
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