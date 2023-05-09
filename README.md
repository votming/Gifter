# Gifter

Gifter is a backend application that provides API interfaces to generate dynamic content for web pages. It is designed to generate titles, paragraphs, images, and HTML blocks on demand, enabling easy content generation for various use cases.

## Features

- Generate dynamic content for web pages:
  - Titles
  - Paragraphs (supports generating multiple paragraphs)
  - Images
  - HTML blocks

## Technologies Used

Gifter is developed using the following technologies and frameworks:

- Python: The core programming language
- FastAPI: The main framework for building the API interfaces
- SQLAlchemy: For working with the database
- Pydantic: Used for data mapping and validation

## Installation

To install and set up Gifter on your local machine, follow these steps:

1. Clone the project repository to your local machine.
2. Build the project locally using Docker Compose: `docker-compose build`
3. Start the project: `docker-compose up -d`

## Usage

After successfully installing and running Gifter, you can interact with the API interfaces by accessing the Swagger documentation at [http://localhost:8000/docs](http://localhost:8000/docs). The Swagger documentation provides detailed information about the available APIs and their usage.
