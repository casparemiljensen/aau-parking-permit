# AAU Parking Permit
A scheduled parking permit issuer for avoiding fines when parking at AAU-Cassiopeia.

* Select day(s)
* Select time(s)
* Mimics the request made from the browser based page 
* Handles Daylights savings
* Docker support - Run on your own laptop, avoid paying for hosting
* Stateful and persistent - Saves "last-run" as a state
* Intended to work on a laptop (Non 24/7 env.) - The scheduler can handle the app being restarted