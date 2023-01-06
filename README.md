# Cataloger CLI


<!-- ABOUT THE PROJECT -->

## About The Project

## Development

### Running the test locally

After installing all the requirements you should:

1. Run the test:

   ```sh
   ENV=test pytest -vv --junitxml=pytest.xml --cov=./ --cov-report=xml --cov-config=.coveragerc --cov-branch tests
   ```

The -vv option is for having even more information about the local execution in case for some reason you have problems for instance finding the ini file with the configuration

