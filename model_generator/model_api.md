### Model APIS

Base Url: indraabm.herokuapp.com/

Schemes: HTTPS

#### /models/props/{number}
- Descriptions
  Submit the parameters
- Method: PUT
- Parameters: 
  - number
    - type: number
- Request Payload:
```python
  {
  "population": {
    "val": 40,
    "question": "What is the population of the town?",
    "atype": "INT",
    "lowval": 1,
    "hival": 500,
    "defaultVal": 40,
    "errorMessage": "",
    "disabledButton": false
  },
  "memory": {
    "val": 7,
    "question": "What is the memory capacity of drinkers?",
    "atype": "INT",
    "lowval": 1,
    "hival": 50,
    "defaultVal": 7,
    "errorMessage": "",
    "disabledButton": false
  },
  "user_type": {
    "val": "api",
    "question": null,
    "atype": "STR",
    "lowval": null,
    "hival": null,
    "defaultVal": "api",
    "errorMessage": "",
    "disabledButton": false
  },
  "OS": {
    "val": "Linux",
    "question": null,
    "atype": "STR",
    "lowval": null,
    "hival": null,
    "defaultVal": "Linux",
    "errorMessage": "",
    "disabledButton": false
  },
  "exec_key": {
    "val": 880729821,
    "question": null,
    "atype": "INT",
    "lowval": null,
    "hival": null,
    "defaultVal": 880729821,
    "errorMessage": "",
    "disabledButton": false
  }
}
```

- Response
```python
  {
    env: object,
    exec_key: number,
    module: string,
    period: number,
    props: object
    switches: array,
    type: string,
    user: object,
    user_type: string,
  }
  ```

##### /models
- Method: GET
- Descriptions
  Fetch all the available models

- Parameters: 
  - active
    - type: boolean
    - default: false
- Response:
```python
{
    active: boolean,
    doc: string,
    graph: string,
    modelID: number,
    module: string,
    name: string,
    package: string,
}
```
- Example:
  - Request URL: https://indraabm.herokuapp.com/models?active=true
  - Response: 
```python
[
    {
        active: true,
        doc: "A toy model to test the system.",
        graph: "scatter",
        modelID: 0,
        module: "basic",
        name: "Basic",
        package: "models",
    }
]
```

##### /models/props/{number}
- Method: GET
- Descriptions: 
Fetch the input parameters for the model

- Parameters: 
  - number
    - type: number
- Response:
```python
{
  LABEL_NAME: {
    "val": any,
    "question": string,
    "atype": string,
    "lowval": number,
    "hival": number
  },
}
```
- Example:
  - Request URL: https://indraabm.herokuapp.com/models/props/3
  - Response: 
```python
{
  "grid_height": {
    "val": 20,
    "question": "What is the grid height?",
    "atype": "INT",
    "lowval": 2,
    "hival": 100
  },
  "grid_width": {
    "val": 20,
    "question": "What is the grid width?",
    "atype": "INT",
    "lowval": 2,
    "hival": 100
  },
  "num_tsetters": {
    "val": 8,
    "question": "How many fashion trendsetters do you want?",
    "atype": "INT",
    "lowval": 1,
    "hival": 100
  },
  "num_followers": {
    "val": 24,
    "question": "How many fashion followers do you want?",
    "atype": "INT",
    "lowval": 1,
    "hival": 100
  },
  "user_type": {
    "val": "api",
    "question": null,
    "atype": "STR",
    "lowval": null,
    "hival": null
  },
  "OS": {
    "val": "Linux",
    "question": null,
    "atype": "STR",
    "lowval": null,
    "hival": null
  },
  "exec_key": {
    "val": 207518708,
    "question": null,
    "atype": "INT",
    "lowval": null,
    "hival": null
  }
}
```

##### /pophist/{id}
- Method: GET
- Description
Fetch the data for the histgram
- Parameters: 
  - id:
    - type: number
- Response
```python
{
  "periods": number,
  "pops": {
    GROUP_NAME: number[],
  }
}
```
- Example:
  - Request URL: https://indraabm.herokuapp.com/pophist/3842183
  - Response:
```python
{
  "periods": 10,
  "pops": {
    "Blue Trendsetters": [
      0,
      7,
      2,
      0,
      0,
      1,
      2,
      3,
      5,
      7,
      5
    ],
    "Red Trendsetters": [
      8,
      1,
      6,
      8,
      8,
      7,
      6,
      5,
      3,
      1,
      3
    ],
    "Blue Followers": [
      24,
      24,
      23,
      17,
      13,
      9,
      4,
      4,
      5,
      11,
      13
    ],
    "Red Followers": [
      0,
      0,
      1,
      7,
      11,
      15,
      20,
      20,
      19,
      13,
      11
    ]
  }
}
```

##### /user/msgs/{periods}
- Method: GET
- Description
Fetch the Model Status

- Parameters
  - periods
    - type: number
- Response:
```python
string
```
- Example:
  - Request Url: https://indraabm.herokuapp.com/user/msgs/3842183
  - Response:
  ```python
  "\n==================\nCensus for period 0\n==================\nGroup census:\n==================\n  Blue Trendsetters: 0\n  Red Trendsetters: 8\n  Blue Followers: 24\n  Red Followers: 0\n==================\n Agent census:\n==================\n  Agents who moved: 32\n  Agents who switched groups: 0\n\n==================\nCensus for period 1\n==================\nGroup census:\n==================\n  Blue Trendsetters: 7\n  Red Trendsetters: 1\n  Blue Followers: 24\n  Red Followers: 0\n==================\n Agent census:\n==================\n  Agents who moved: 32\n  Agents who switched groups: 7\n\n==================\nCensus for period 2\n==================\nGroup census:\n==================\n  Blue Trendsetters: 2\n  Red Trendsetters: 6\n  Blue Followers: 23\n  Red Followers: 1\n==================\n Agent census:\n==================\n  Agents who moved: 32\n  Agents who switched groups: 8\n\n==================\nCensus for period 3\n==================\nGroup census:\n==================\n  Blue Trendsetters: 0\n  Red Trendsetters: 8\n  Blue Followers: 17\n  Red Followers: 7\n==================\n Agent census:\n==================\n  Agents who moved: 32\n  Agents who switched groups: 8\n\n==================\nCensus for period 4\n==================\nGroup census:\n==================\n  Blue Trendsetters: 0\n  Red Trendsetters: 8\n  Blue Followers: 13\n  Red Followers: 11\n==================\n Agent census:\n==================\n  Agents who moved: 32\n  Agents who switched groups: 4\n\n==================\nCensus for period 5\n==================\nGroup census:\n==================\n  Blue Trendsetters: 1\n  Red Trendsetters: 7\n  Blue Followers: 9\n  Red Followers: 15\n==================\n Agent census:\n==================\n  Agents who moved: 32\n  Agents who switched groups: 5\n\n==================\nCensus for period 6\n==================\nGroup census:\n==================\n  Blue Trendsetters: 2\n  Red Trendsetters: 6\n  Blue Followers: 4\n  Red Followers: 20\n==================\n Agent census:\n==================\n  Agents who moved: 32\n  Agents who switched groups: 8\n\n==================\nCensus for period 7\n==================\nGroup census:\n==================\n  Blue Trendsetters: 3\n  Red Trendsetters: 5\n  Blue Followers: 4\n  Red Followers: 20\n==================\n Agent census:\n==================\n  Agents who moved: 32\n  Agents who switched groups: 1\n\n==================\nCensus for period 8\n==================\nGroup census:\n==================\n  Blue Trendsetters: 5\n  Red Trendsetters: 3\n  Blue Followers: 5\n  Red Followers: 19\n==================\n Agent census:\n==================\n  Agents who moved: 32\n  Agents who switched groups: 5\n\n==================\nCensus for period 9\n==================\nGroup census:\n==================\n  Blue Trendsetters: 7\n  Red Trendsetters: 1\n  Blue Followers: 11\n  Red Followers: 13\n==================\n Agent census:\n==================\n  Agents who moved: 32\n  Agents who switched groups: 8\n"
  ```