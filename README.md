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
- Edit the `schedule.txt` file (Else it won't start.)

- Define the days you wish a permit for (comma-separated).
- Define the times of the day you wish a permit for (min. 10 hours apart, comma-separated)
- Define a phone number - For a receipt (do not define the 45 prefix)
- Define a license plate number (Upper or lowercase)

`schedule.txt` example
```
days: monday, tuesday, wednesday, thursday, friday
times: 08:00
phone_no: 12345678
license_plate: AB12345
```
The parking rules allows for 30 min parking using a parking-disc. Make sure to define a starttime for which after you are certain that the docker container has started.

To use with docker.
* Make sure to have docker installed.
* CD to the root directory of the project in a terminal and run:

```
docker-compose build
docker-compose up
```

If using docker desktop, make sure to configure it to start with your pc.
