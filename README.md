<img width="613" height="540" alt="image" src="https://github.com/user-attachments/assets/825adbe3-b8f7-4b9a-900f-bcddbf03d76a" /> 
<br>

Docke file
To build and start all services:
```bash
"docker compose up --build -d"
To stop : 
 "docker compose down"


### Explanation (brief)
'docker compose up --build -d':builds images and runs containers in background
'docker compose down': stops and removes containers, network, and default volumes
'docker compose stop':stops without removing containers

### Optional additions (recommended)
```md
## View logs
```bash
docker compose logs -f
