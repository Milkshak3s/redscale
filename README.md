# redscale
But it  --||  S C A L E S  ||--


## service-target
Provides endpoints for managing active implants

Features:
- `localhost:80/checkIn` - Implants to check in and get the next command (if available)
- `localhost:8000/activeTargets` - Users to get a list of all active endpoints
- `localhost:9000/target` - Users to get information about a single target


## service-command
Provides endpoints for managing implant commands

Features:
- `localhost:12000/nextCommand` - Implants to get the next command to execute
- `localhost:10000/commandHistory` - Users to get a list of all commands logged
- `localhost:11000/addCommand` - Users to upload new commands for implants to consume
