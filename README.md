# smart-inventory-manager
An advanced and smart inventory management system

__Requirements:__  
Install postgres  
Install python3
create and enable virtual environment  
run "pip install -r requirements.txt"  
create a .env file in the root folder and add all the below mentioned environment variables  
including postgres credentials and database name  
run uvicorn main:app --reload --host 0.0.0.0 --port 80  
you are good to go!  
  
__Environment variables needed to run the app__  
secret=set_your_secret_salt  
algo=HS256  
db_user=your_pg_username  
db_password=your_pg_password  
db_name=your_database_name  
db_host=localhost  
db_port=5432  
  
__#below defaults are in hours__  
replenishment_forced_delay=1  
lead_time=1  
max_lead_time=1  
  
__#defaults for inventory thresholds__  
threshold=50  
critical_threshold=10  
  
__#timedelay before a PO is processed in minutes__  
#Once a PO is created this is the time it takes for actual restock.  
time_delay_for_po=30  
  
sales_trend_interval=1  
sales_trend_threshold=50  
