# Normandy Load tests

## Installation
This project uses [pipenv](https://pipenv.readthedocs.io/en/latest/) to manage dependencies.
After checking out this repo, run the following commands to create the virtual environment and
install the required dependencies.

`pipenv install`

## Configuration

This project uses environment files to store values unique to the target load testing
environment. Copy the file `.env.dist` to `.env` and set the environment variables
to their required values.

Then use the following command to activate the virtual environment:

`pipenv shell`

pipenv will automatically set any environment variables found in the `.env` file when
you activate the virtual environment. If you change anything in `.env` you need to
exit the virtual environment and reenter using the following commands:

`exit`

`pipenv shell`

## Running Load Tests.
The load tests were written using [Molotov](https://molotov.readthedocs.io/en/stable/)
and can be started using the following command:

`molotov -c -v d <duration> api_tests.py`

where `<duration>` is the length of time in seconds that you want the load test to run.

Check the Molotov documentation for details on other options available to run the tests.

