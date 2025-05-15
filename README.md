# AAU Parking Permit
A scheduled parking permit issuer for avoiding fines when parking at AAU-Cassiopeia.


### Features
* Select day(s)
* Select time(s)
* Mimics the request made from the browser based page 
* Handles Daylights savings
* Docker support - Run on your own laptop, avoid paying for hosting
* Stateful and persistent - Saves "last-run" as a state
* Intended to work on a laptop (Non 24/7 env.) - The scheduler can handle the app being restarted

### How to use it

- Clone the project.
- Make a file in the root directory of the project, name it `schedule.txt`

- Define the days you wish a permit for (comma-separated).
- Define the times of the day you wish a permit for (min. 10 hours apart, comma-separated)
- Define a phone number - For a receipt (do not define the 45 prefix)
- Define a license plate number (Upper or lowercase)

```
days: monday, tuesday, wednesday, thursday, friday
times: 08:00
phone_no: 12345678
license_plate: AB12345
```

To use with docker.
Make sure to have docker installed.
CD to the root directory of the project in a terminal and run:

If using docker desktop, make sure to configure it to start with windows

```
docker-compose build
docker-compose up
```