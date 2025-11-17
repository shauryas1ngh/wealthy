Hi Somit ,
Setup postgresql on your device at port 5432 and password as "   " (three blank spaces)or update the details in .env if configured otherwise. 

Once this is setupo you can run the command :
 uvicorn app.main:app --reload   in tty to start the Fast API server . 

 Open http://localhost:8000/docs
 on any web browser to access the API endpoints via the free swaggerUI .

 You can check the functionality of endpoints from this webpage. 

 