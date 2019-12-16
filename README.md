# Simple mailing service

This project is a very simple email website. It takes parameters from a user on the frontend, validates it's correctness and sends it to the backend. The backend has one endpoint `/mail/` which takes form data and pushes it to a Redis queue or starts a background task on server (depending on setting the `USE_REDIS` environment variable). 


The `background task/queue worker` is defined in `mail_sender.py`. It loops over available email providers, trying to send the message until any of them responds with a success status code. Also, if some of the providers fail to respond, the sender will wait an exponential amount of time (limited to one minue max, then the timer is reset) for that particular provider.


The solution is full-stack.


To start:
* make sure you have installed `make`, `docker` and `docker-compose`
* set the following environment variables with values from email: `MAILGUN_URL`, `MAILGUN_KEY`, `SENDGRID_KEY`
* in the root directory run `make dev-build`
* after previous point is finished, in the root directory run `make dev-start`
* to visit application go to `http://localhost:3000`
* to visit API docs go to `http://localhost:8080/docs`

To run tests:
* in the root directory run `make test-build`
* run `make test-back-start` and `make test-front-start`
