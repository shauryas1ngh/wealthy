Hi Somit ,
Setup postgresql on your device at port 5432 and password as "   " (three blank spaces)or update the details in .env if configured otherwise. 

Once this is setup you can run the command :
 uvicorn app.main:app --reload   in tty to start the Fast API server . 

 Open http://localhost:8000/docs
 on any web browser to access the API endpoints via the free swaggerUI .

 You can check the functionality of endpoints from this webpage. 

 
<img width="1254" height="602" alt="Screenshot 2025-11-17 at 3 21 30 PM" src="https://github.com/user-attachments/assets/79d72c2a-7a3b-4a8a-b0c0-1bda6c2e26ec" />
