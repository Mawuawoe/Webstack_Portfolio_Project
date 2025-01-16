# Webstack Portfolio Project

The Salinity App is a specialized web application designed to streamline and automate the tracking, monitoring, and analysis of salinity levels in the salt production process. It enables Brine Attendants to manually log salinity and brine levels across various crystallizing pans and reservoirs. Additionally, the app provides Production Managers with real-time access to this data through an intuitive dashboard, facilitating informed decision-making and enhancing operational efficiency.

This is a capstone project for the online Software Engineering program at ALX, where learners are tasked with creating their own projects to demonstrate their understanding of backend and frontend concepts. For my project, I developed the Salinity App for Electrochem GH LTD, a salt production company in Ghana.

---

## Features

- **Data Entry**: Brine Attendants can log into the system, select specific pans, and enter salinity readings along with the brine levels.
- **Monitoring & Visualization**: The app presents Production Managers with an up-to-date overview of salinity levels across all pans, allowing for informed decision-making and optimization of the salt production process.
- **Reporting**: Managers can generate reports based on specific time periods, and export the data in formats like CSV
- **Role-Based Access Control**: Role-based access ensures users only have access to the features relevant to their role (e.g., Admins, Brine Attendants).

---

## Technologies Used  
- **Backend**: Flask, SQLAlchemy, JWT for authentication.  
- **Frontend**: HTML, CSS, JavaScript.  
- **Database**: MySQL.  
- **Containerization**: Docker and Docker Compose.  
- **Others**: cURL for API testing.  

---

## Installation

To run the **Salinity App** on your local machine using Docker, follow these steps:

### Prerequisites

Ensure the following are installed on your machine:
- **[Docker]** – To create and manage containers.
- **[Docker Compose]** – To manage multi-container Docker applications.

### Using Docker

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mawuawoe/Webstack_Portfolio_Project/
   cd salinity-web-app
   ```

2. Build the Docker container:
   ```bash
   docker-compose build
   ```

3. Run the app using Docker:
   ```bash
  docker-compose up
   ```

4. Visit the app in your browser at [http://localhost:5000](http://localhost:5000).

### Without Docker

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mawuawoe/Webstack_Portfolio_Project/
   ```

2. Run the app:
   ```bash
  ./setup.sh
   ```
**Warning: Running without Docker requires the correct Python version and dependencies installed. Compatibility issues may arise if your system is not configured properly.**

---

## Application Structure

The **Salinity App** has a dual-route setup:

1. **Frontend Routes**: Serve the web-based user interface.
2. **API Routes**: Expose RESTful endpoints under the `/api/v1/` namespace for external programmatic interaction.

---

### Frontend Routes

The following routes define the user interface and their functionalities:

| **Route**          | **Description**                                                                                                   |
|---------------------|-------------------------------------------------------------------------------------------------------------------|
| `/`                 | **Landing Page**: Provides information about the app. Contains a "Get Started" button. Redirects to `/register` for the first admin user registration, or to `/login` if an admin user exists. Unprotected route. |
| `/register`         | **Register Page**: Allows the first admin user to register if no admin exists.                                   |
| `/login`            | **Login Page**: Allows users to log in and generates a JWT for authenticated access. Unprotected route.          |
| `/dashboard`        | **Dashboard**: Displays salinity records on a site map, with live updates as new data is submitted.              |
| `/data_entry`       | **Data Entry**: Used by Brine Attendants to submit salinity and brine level records.                             |
| `/reports`          | **Reports**: Allows managers to generate and download reports based on selected time periods.                    |
| `/create_user`      | **Create User**: Allows admins to create other users with specified roles. Accessible only to admin users.        |
| `/logout`           | **Logout**: Logs the user out and invalidates their session.                                                     |

---

### API Services

The **API** operates under the `/api/v1/` namespace and provides endpoints for programmatic access. All API requests and responses are JSON-based.

#### Base URL
[http://localhost:5000/api/v1]


#### API Endpoints

| **HTTP Method** | **Endpoint**               | **Description**                                                                                     |
|------------------|----------------------------|-----------------------------------------------------------------------------------------------------|
| `POST`          | `/initialize_first_user`   | Registers the first admin user. This route is disabled if an admin user already exists.            |
| `POST`          | `/auth/login`              | Logs in the user and generates a JWT for authorization.                                            |
| `GET`           | `/users`                   | Retrieves all users. Requires authorization.                                                       |
| `POST`          | `/users`                   | Creates a new user. Requires admin authorization.                                                  |
| `GET`           | `/users/<user_id>`         | Retrieves a specific user by their ID. Requires authorization.                                     |
| `PUT`           | `/users/<user_id>`         | Updates details of a specific user. Requires admin authorization.                                  |
| `DELETE`        | `/users/<user_id>`         | Deletes a user. Requires admin authorization.                                                      |
| `GET`           | `/pans`                    | Retrieves all pans. Requires authorization.                                                        |
| `POST`          | `/pans`                    | Creates a new pan. Requires admin authorization.                                                   |
| `GET`           | `/pans/<pan_id>`           | Retrieves details of a specific pan. Requires authorization.                                       |
| `PUT`           | `/pans/<pan_id>`           | Updates a specific pan. Requires admin authorization.                                              |
| `DELETE`        | `/pans/<pan_id>`           | Deletes a pan. Requires admin authorization.                                                       |
| `GET`           | `/salinity`                | Retrieves all salinity records. Supports filters (e.g., by date, pan type) and pagination. Requires authorization. |
| `POST`          | `/salinity`                | Logs a new salinity record. Requires authorization.                                                |
| `GET`           | `/salinity/<salinity_id>`  | Retrieves details of a specific salinity record. Requires authorization.                           |
| `PUT`           | `/salinity/<salinity_id>`  | Updates a specific salinity record. Requires admin authorization.                                  |
| `DELETE`        | `/salinity/<salinity_id>`  | Deletes a salinity record. Requires admin authorization.                                          

#### Salinity Query Parameters

The `/salinity` endpoint supports the following query parameters for filtering and pagination:

- `date`: Filter records by a specific date or date range.
- `pan_type`: Filter records by the type of pan.
- `offset`: Pagination offset. Default is `0`.
- `limit`: Number of items per page. Default is `10`.

The response includes URLs for the next and previous pages (if applicable).

#### Example cURL Request

To fetch salinity data with filters:
```bash
curl -X GET "http://localhost:5000/api/v1/salinity?date=2024-01-01&pan_type=Pan&limit=5" \
-H "Authorization: Bearer <your_token>"
```

---

## Usage

**For Brine Attendants**
- Log in to your account.
- Navigate to the Data Entry page.
- Input salinity and brine level readings for specific locations.
- Submit entries to save them to the database.

**For Production Managers/Admin**
- Log into your account.
- Access the Dashboard for an overview of salinity trends.
- Use the Reports page to filter data by location, date, or other parameters.
- Export detailed reports in CSV format.

![Dashboard Screenshot](./ALXPP1.jpg)
![Dashboard Screenshot](./ALXPP2.jpg)

Overall Benefits
Efficiency: By streamlining data collection and providing real-time access to information, the Salinity App enhances operational efficiency in monitoring salinity levels.
Improved Decision-Making: The app’s reporting and visualization features enable Production Managers to make data-driven decisions that optimize the salt production process.
User-Friendly Interface: The intuitive design of the app ensures that both Brine Attendants and Production Managers can navigate it easily, reducing training time and improving user adoption.