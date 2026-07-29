# Fix Plan - Task List

- [x] Step 1: Fix `config.py` - Remove first 3 incorrect `os.getenv()` calls & duplicate `CHROMA_DB_PATH`
- [x] Step 2: Fix `app/main.py` - Remove duplicate `app = FastAPI()` & duplicate `/chat` route
- [x] Step 3: Fix `Dockerfile` - Fix `COPY ..` to `COPY . .`, fix `CMD` syntax
- [x] Step 4: Fix `docker-compose.yml` - Fix indentation, structure, `env-file` → `env_file`
- [x] Step 5: Test with correct command `uvicorn app.main:app --reload`

