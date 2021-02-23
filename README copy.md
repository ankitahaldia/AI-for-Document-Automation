This repo serves as a way to download about 3000 Pdf containing joint commissions (commissions paritaires) ranging from jan 2018 to febr 2020.

# Why 

In the context of the project assigned to us by KPMG, we need to extract pdfs containing joint commissions statements from https://emploi.belgique.be/ 

# How
Note that the pdf files are already downloaded, but the code is still provided so you could do it yourself if need be.

if you dont already have `virtualenv`, here's a [link](https://virtualenv.pypa.io/en/latest/installation.html) on how to install it.

1. Download the repo
2. open a python terminal and navigate to the repo folder
3. type : `venv/Scripts/activate` to activate the virtual environement.
4. from that same terminal launch the `jc_dowload_script.py` file

this should download all the pdfs in the repo folder.

# What
this repo is containing
- a json file (`jc.json`). Each of it's json object contains a route to each pdf (`documentLink` field)
- `venv` folder containing the needed virtual envirement if you wish to run the code yourself.
- `data` folder containing all the pdfs
- `jc_dowload_script.py` file script to download all the pdfs

the json object looks like this:
![alt text](https://github.com/Cassik6/commissions-paritaires/main/assets/requestjson.jpg)

if you want to create your own `jc.json` you can do so by querying the https://emploi.belgique.be/ API endpoint https://public-search.emploi.belgique.be/website-service/joint-work-convention/search using a POST request containing a json in the body. The request json looks like this:









