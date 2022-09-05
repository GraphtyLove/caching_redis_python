from fastapi import FastAPI, Response
from cache_service import Cache


app = FastAPI()
cache = Cache()


@app.get("/")
async def index():
	return "alive!"


@app.get("/home")
async def home(username: str, response: Response):

	root_key = f"/home:{username}"
	data = cache.get_data_from_cache(key=root_key)
	if data:
		response.headers['X-cache'] = "hit"
		return data

	print("No cache found...")
	data = {"success": True, "message": "2 World"}
	state = cache.save_data_to_cache(root_key, data)
	print("Cache saved: ", state)
	response.headers['X-cache'] = "miss"
	return data
