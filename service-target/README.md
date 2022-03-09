# Target Service
```
cd service-target
docker-compose build && docker-compose up -d
```  

## Routes
### Check In
```GET http://localhost:80/checkIn?id=[IMPLANT_ID]```  
Side Effects:
- PUTs target in DB, updates active targets
Returns:
- A JSON list of active targets

### Active Targets
```GET http://localhost:8000/activeTargets```  
Side Effects: 
- None  
Returns:
- A JSON list of active targets

### Target
```GET http://localhost:9000/target?id=[IMPLANT_ID]```  
Side Effects:
- None  
Returns:
- Returns a JSON representation of a target