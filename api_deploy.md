# Deploying the FastAPI Web API

## Local Development
1. Ensure all dependencies are installed:
   ```sh
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```sh
   uvicorn api:app --reload
   ```
3. Visit http://127.0.0.1:8000/docs for the interactive API docs.

## Deploy to Cloud (e.g., Render, Railway, Azure, Heroku)
1. Make sure `api.py` is present and working.
2. Add a `Procfile` with this content:
   ```
   web: uvicorn api:app --host 0.0.0.0 --port $PORT
   ```
3. Push your repo to your chosen cloud platform and follow their Python/FastAPI deployment guide.

- For Render: https://render.com/docs/deploy-fastapi
- For Railway: https://docs.railway.app/guides/deploy-fastapi
- For Azure: https://learn.microsoft.com/en-us/azure/developer/python/tutorial-deploy-app-service-cli-01
- For Heroku: https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app

## Notes
- Ensure your cloud service exposes the correct port and allows incoming HTTP traffic.
- For production, remove `--reload` and consider using `gunicorn` with `uvicorn.workers.UvicornWorker` for robustness.
