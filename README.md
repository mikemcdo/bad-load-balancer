# Problem
A service with variable processing times is behind a load balancer. Although all requests have some variability, about 5% of requests take significantly longer than others to complete. As a result, the round-robin load balancer (which delivers requests evenly) does not work well, and some servers occasionally back up. This leads to a poor customer experience where some servers are overloaded and slow, while others remain idle. The task is to use the load balancer API to maintain a reasonable load distribution across all servers.
# Solution
In this solution, we will use the load balancer API to maintain a reasonable load distribution across all servers. The following approach will be used:

	1. Set a minimum number of available servers that must be enabled at all times to prevent all servers from being disabled.
	2. Set a percentage of server capacity; if surpassed, the server is considered overloaded.
	3. Disable all enabled servers that are overloaded.
	4. Enable all disabled servers that are not overloaded.
	5. Check the servers at a predefined interval and repeat the process.

## Dockerfile
The Dockerfile builds an image on python:3.11-slim. It:

	1. Ensures the system and libraries are up to date.
	2. Installs the required Python packages.
	3. Copies the source code to the container.
	4. Ensures the formatting of the code is correct using Black.
	5. Ensures the unit tests pass.
	6. Sets the command to sleep infinity to keep the container running.

## Docker Compose

There are two Docker Compose files, both allowing you to customize the values used by the program via environment variables. These values are:
```      
- MIN_NUMBER_OF_SERVERS=INT
- UPDATE_INTERVAL=INT
- MAX_ACCEPTABLE_LOAD=FLOAT
- LOG_LEVEL=STRING
```

Both Compose files will build the image if it hasn’t already been built. They will run the image and be able to connect to the load balancer via the Docker network.

The main difference is that the docker-compose.yml file will run the image in an infinite sleep, so you have to exec into the image to run the program. The docker-compose-prod.yml file will run the program automatically.

## Running the Program
To run the program, follow these steps:
1. Pull down the repository
2. From the root directory run `docker compose up`, this will trigger the image to build and start the load balancer service
3. Open up another terminal and exec into the container `docker exec -it solution /bin/bash`
4. From inside the container execute the command `./app/solution.py`
5. From there you can monitor the logs and see when servers are disabled and enabled. You should see the performance of the load balancer improve and distribute much more effectively. Your logs will look like
```
INFO:root:System started...
INFO:root:UPDATE_INTERVAL: 10
INFO:root:MIN_NUMBER_OF_SERVERS: 4
INFO:root:MAX_ACCEPTABLE_LOAD_FOR_ENVIRONMENT: 0.75
INFO:root:MAX_LOAD: 375.0
INFO:root:LOG_LEVEL: INFO
INFO:root:API_BASE_URL: http://bad_load_balancer:8188
INFO:root:Checking server status...
INFO:root:Disabling node server-04, queued requests: 436
INFO:root:Waiting for next update...
INFO:root:Checking server status...
INFO:root:Enabling node server-04, queued requests: 200
INFO:root:Waiting for next update...
INFO:root:Checking server status...
INFO:root:Disabling node server-10, queued requests: 376
INFO:root:Disabling node server-15, queued requests: 417
INFO:root:Waiting for next update...
INFO:root:Checking server status...
INFO:root:Enabling node server-10, queued requests: 258
INFO:root:Enabling node server-15, queued requests: 42
```

## Testing
The unit tests are ran when the image is built. To run both the unit and integration tests, exec into the container and run `pytest /app`.

## Running the prod docker compose
To run the production Docker Compose file, use the command `docker compose -f docker-compose-prod.yml up`. When you run this command, you will only see the load balancer logs, but you’ll notice that as servers pass the threshold, they switch to disabled and are then enabled appropriately.


