# MyBots
## Install locally
1. Run `pip install -r requirements.txt`.
2. Run `python server.py`.

## Install on Render.com
Merge your changes to `main` branch and Render.com will automatically deploy it.
mybot_server: https://dashboard.render.com/web/srv-cihqdn59aq012evjbm20

## Database
App uses cloud PostgreSQL database from Render.com.
mybotdb: https://dashboard.render.com/d/dpg-cihslbtgkuvojjb72m60-a

## Common Commands
* Set `OPENAI_API_KEY` in environments.
* To access Flask Shell, run `python -m flask --app server shell`.


## Sync model with DB (DB Migration)
To sync model changes to PostgreSQL:
1. Open Flask Shell and run:
```
from server import db
db.create_all()
```
2. Run `python -m flask --app server db init`.
3. Run `python -m flask --app server db migrate -m "Initial migration"`.
4. Run `python -m flask --app server db upgrade`.