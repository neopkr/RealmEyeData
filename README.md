# RealmEyeData
This proyect was made for the people who wants to get information from RealmEye with code. The proyect was made in Python3 using Flask, beautifulsoup4, request.

## Query Params
At the moment only exist 1 paramater
```sh
GET data?player=neopkr
# example:
https://realmdata.herokuapp.com/data?player=neopkr
```

### Query Examples with JS, Python3
- Vanilla Javascript
```javascript
async function getRealmData() {
  try {
    const response = await fetch('https://realmdata.herokuapp.com/data?player=neopkr')
    
    if(!response.ok) {
      throw new Error(`Error! status: ${response.status}`)
    }
    
    const result = await response.json()
    return result
  } catch (err) {
    console.log(err)
  }
}

getRealmData().then((res) => console.log(res))
```
- Python3 (lib: requests)
```py
import requests as r
url = 'https://realmdata.herokuapp.com/data?player=neopkr'

res = r.get(url)
data = res.json() # URL response to JSON
print(data)

```
With that you can retrieve all data of the player

# Issues
There is a big issue at the moment, not all errors are handled so the API can literally destroy the server.
If there any issue, please post in [Issues](https://github.com/neopkr/RealmEyeData/issues) section.
#### Update 5 Sep
Need handled all errors in getRealmEyeData().
