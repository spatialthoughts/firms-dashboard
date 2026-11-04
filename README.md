# Daily Fire Dashboard

A simple dashboard showing active fire detections from [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/) in one Admin2 region (district) over the past 24 hours. The data is updated every 12 hours by GitHub Actions and the dashboard is hosted on GitHub Pages.

## Files

- `01_select_aoi.ipynb`: Selects an Admin2 region and saves it as `data/aoi.geojson`.
- `02_fetch_fires.ipynb`: Fetches fire detections in the AOI from the past 24 hours and saves them as `data/fires.geojson`.
- `03_update_fires.py`: The same steps as notebook 02 as a script. GitHub Actions runs it on a schedule.
- `index.html`: The dashboard.
- `.github/workflows/update-fires.yml`: The GitHub Actions workflow that runs `03_update_fires.py` every 12 hours and commits the updated `data/fires.geojson`.

## Add the FIRMS API Key as a Secret

The workflow needs your FIRMS MAP_KEY to fetch the data. Request a free key at the [FIRMS MAP_KEY page](https://firms.modaps.eosdis.nasa.gov/api/map_key/). Store it as a repository secret, so it is never visible in the code or the workflow logs.

1. Open your repository on GitHub and go to *Settings*.
2. In the left sidebar, select **Secrets and variables &rarr; Actions**.
3. Click *New repository secret*.
4. Enter **FIRMS_MAP_KEY** as the *Name* and paste your key as the *Secret*. Click *Add secret*.

To update the key later, click the pencil icon next to `FIRMS_MAP_KEY` on the same page, paste the new key and click *Update secret*.

## Run the Workflow

The workflow runs every 12 hours. To run it right away:

1. Go to the *Actions* tab of your repository.
2. Select **update-fires** from the left sidebar.
3. Click *Run workflow* and then the green *Run workflow* button.

Once the run finishes, the workflow commits the new `data/fires.geojson` and GitHub Pages republishes the dashboard.

> Note: GitHub pauses scheduled workflows in public repositories after 60 days without any activity. Run the workflow manually or push a commit to restart it.

## Run Locally

To run the notebooks in VS Code, create a file named `.env` in the project folder with your key. VS Code loads it into the notebook kernel.

```
FIRMS_MAP_KEY=your_key
```

The `.env` file is listed in `.gitignore`, so it is never committed. To view the dashboard, start a local web server in the project folder and open http://localhost:8000.

```
python -m http.server
```
