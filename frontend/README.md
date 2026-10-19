# Frontend

The React/Vite application is in `src/`. From this folder:

```powershell
npm ci
npm run dev
```

Vite proxies local `/api` requests to Flask at `http://127.0.0.1:5000`. For a production build, set `VITE_API_URL` to the deployed backend's HTTPS base URL. Run `npm run lint` and `npm run build` to check the frontend.
