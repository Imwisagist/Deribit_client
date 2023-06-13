# Test_for_Mera_capital

### **Task description:**
<details>
    <summary>Click to show</summary>

![screenshot](https://github.com/imwisagist/Test_for_Mera_capital/blob/main/task.png?raw=true)

</details>

### Clone this repository and enter:
```
git clone https://github.com/Imwisagist/Test_for_Mera_capital.git 
cd Test_for_Mera_capital/
```
### Install poetry:
```
pip install poetry
```
##### Installing dependencies:
```
poetry install
```
##### Running the client:
```
poetry run python client.py
```
##### Running the api:
```
poetry run uvicorn api:app
```
##### Running tests:
```
poetry run pytest -vv test.py
```
### Examples of both requests and response:
```
Request
http://127.0.0.1:8000/get_all_data_about_ticker?ticker=eth_usd

Response
[{"ticker":"eth_usd","price":1747.33,"timestamp":1686632328840437},
{"ticker":"eth_usd","price":1747.47,"timestamp":1686632434879312},
{"ticker":"eth_usd","price":1750.71,"timestamp":1686633307399571},
{"ticker":"eth_usd","price":1750.78,"timestamp":1686633313400012},
{"ticker":"eth_usd","price":1750.69,"timestamp":1686633314382924}]

Request
http://127.0.0.1:8000/get_last_price_of_ticker?ticker=eth_usd

Response
{"ticker":"eth_usd","price":1750.66,"timestamp":1686633318408778}

Request
http://127.0.0.1:8000/get_price_of_ticker_by_time?ticker=eth_usd&timestamp=1686632328840437

Response
{"ticker":"eth_usd","price":1747.33,"timestamp":1686632328840437}
```
