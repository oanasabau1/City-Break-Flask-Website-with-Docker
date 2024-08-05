# CityBreak Gateway Service

## Project Description
CityBreak Gateway Service is a Flask-based API that acts as a gateway for handling city break information. It integrates event and weather data for a given city and date, providing a unified response. The service uses Flask-RESTful for API development and SQLAlchemy for database interactions.

## Features
- **City Break Information**: Fetches and combines event and weather data for a specific city and date.
- **Proxy Requests**: Proxies POST, PUT, and DELETE requests to the respective event and weather services.
- **Database Integration**: Uses SQLAlchemy to manage database interactions.

## Services
This project is composed of the following services:
- **CityBreak Gateway**: The main service that integrates event and weather data.
- **Weather Service**: A service that provides weather data.
- **Events Service**: A service that provides event data.
- **Redis**: Used by the Weather Service for caching purposes.
- **MySQL Database**: Used by the Gateway and Events services to store and manage data.


## Running the application
In order to run the city break web application, you need to ensure that you have Docker and Docker Compose. Clone the repository to your local machine and run the following command to start all the services declared in docker-compose.yml file:
```bash
git clone https://github.com/oanasabau1/City-Break-Flask-Website-with-Docker
docker-compose up
```

## Accessing the Service and fetching the data
Once all services are up and running, you can access the CityBreak Gateway Service at [http://localhost:8080/citybreak?city=<input_name>&date=<input_date>.](http://localhost:8080/citybreak?city=<input_name>&date=<input_date>) by introducing the city and date.

You can access the Events service at [http://localhost:5000/events?city=<input_name>&date=<input_date>](http://localhost:5000/events?city=<input_name>&date=<input_date>), but the parameteres can be optional.

You can also access the Weather service at [http://localhost:5001/weather?city=<input_name>&date=<input_date>](http://localhost:5001/weather?city=<input_name>&date=<input_date>), but the parameteres are mandatory, otherwise it fails to fetch data.

The other CRUD operations can be done using cURL commands.

cURL (short for Client URL) is a command-line tool and library used to transfer data to or from a server using various protocols. It supports a wide range of protocols, including HTTP, HTTPS, FTP, and more. cURL is commonly used for making network requests, debugging, and interacting with APIs.
A relevant example for this application is:

```bash
CURL -X POST -F "city=New York" -F "date=2024-08-05" -F "name=Beyonce World Tour" -F "description=Your favourite singer is back in town for a great concert!" http://localhost:5000/events
```

## Further Development

The CityBreak application can be significantly enhanced by incorporating several key features. 

Adding authentication and authorization will secure access to the API, allowing for controlled and secure interactions with the system through methods such as OAuth 2.0 or JWT. This will enable role-based access control, ensuring that only authorized users can access or modify data. 

Additionally, integrating Docker volumes for data persistence will prevent data loss during container restarts, providing a reliable storage solution for MySQL and Redis data.




