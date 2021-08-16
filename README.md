# DSA 2021 National Convention Data Analysis

This repository contains a jupyter notebook for generating data models and dashboards for sharing these models in an interactive format.

## Generating Models

Load the ipynb file in `/generate_models` into your preferred notebook environment. I wrote it with Google Colab in-mind, and the notebook as-written expects to read voter data from Google Drive.

In the setup section, update data input and output location variables (`voter_data_input_loc`, `clustered_data_output_loc`).

To run the notebook on Google Colab, upload the raw convention voter data to your google drive and set `voter_data_input_loc` appropriately.
To run the notebook locally you can simply point these variables to your local filesytem.

## Building the Site

### Install dependencies

**Setup your python environment:**

1. Create and activate a virtual environment for this project however you prefer. I use conda, so:
   - `conda create --name dsa-natcon-analysis`
   - `conda activate dsa-natcon-analysis`
2. `pip install -r requirements.txt`

**If you wish to deploy the site, you can use the Heroku CLI:**

- [Install and configure heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

### Running the Site Locally

`python app.py`

### Deploying to Heroku

1. Create an empty Heroku application.

   `heroku create dsa-natcon-analysis`

2. Push repository to the Heroku remote.

   `git push heroku main`

3. Whenever you make changes, remember to push them up to Heroku's remote to deploy them.
