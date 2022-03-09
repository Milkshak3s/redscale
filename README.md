# redscale
But it    S C A L E S


## Target Service
```
cd target-service
docker-compose build && docker-compose up -d
```

### Routes
Check In
`GET http://localhost:80/checkIn?id=[IMPLANT_ID]`
Side Effects:\t PUTs target in DB, updates active targets
Returns:\t\t A JSON list of active targets

Active Targets
`GET http://localhost:8000/activeTargets`
Side Effects:\t None
Returns:\t\t A JSON list of active targets

Target
`GET http://localhost:9000/checkIn?id=[IMPLANT_ID]`
Side Effects:\t None
Returns:\t\t Returns a JSON representation of a target