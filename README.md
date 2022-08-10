# Open Fibre Data Standard

Welcome to the GitHub repository for the Open Fibre Data Standard.

## Contributing

To contribute to the development of the standard, check out the [discussion tracker](https://github.com/Open-Telecoms-Data/open-fibre-data-standard/discussions).

## Background

The [World Bank](https://worldbank.org), the [International Telecommunications Union](https://itu.int) (ITU), [Mozilla Corporation](https://mozilla.com), the [Internet Society](https://isoc.org) (ISOC), [Liquid Intelligent Technologies](https://liquid.tech), [CSquared](https://www.csquared.com), and [Digital Council Africa](https://www.digitalcouncil.africa/) are partnering to promote the collaborative development of open data standards for describing telecommunications infrastructure. The first challenge we have taken on is that of terrestrial fibre optic infrastructure.

You can read more about the project on the World Bank's blog: [Making it Possible for the World to Log On](https://www.worldbank.org/en/news/feature/2022/06/06/making-it-possible-for-the-world-to-log-on).

## Building the documentation

### Build the docs locally
  
Assuming a unix based system:

```
# Make sure you have python3 venv, e.g. for Ubuntu
# If you're not sure, try creating a venv, and see if it errors
sudo apt-get install python3-venv

# Install submodules
git submodule init
git submodule update

# Create a venv
python3 -m venv .ve    

# Enter the venv, needs to be run for every new shell
source .ve/bin/activate

# Install requirements
pip install --upgrade pip setuptools
pip install -r requirements.txt

# Build the docs
cd docs
make dirhtml
```

Built docs are in `docs/_build/dirhtml`.


Viewing the docs:
```
cd _build/dirhtml
python -m http.server
```

Then go to http://localhost:8000/ in a browser.


## Contact

Please direct any correspondence to [info@opentelecomdata.net](mailto:info@opentelecomdata.net)
