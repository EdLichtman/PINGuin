# PINGuin
##### An API endpoint to check all your API Endpoints   
PINGuin is a REST application that you can post a JSON list of requests to and it will send each request and return the status it recieved. 
<br/>
JSON request is build on:

<br/>
* saveas: file_name.  

* When you add this field the application will remove it, take the remaining JSON request and store it at /routes/file_name. There is no need to add ".json" to the end since this application manages the filetype

<br/>
* urls: [ { }, { }, ... ]
  * { }.url: "http[s]://*.[MY_URL_TO_PING].*"
  * { }.method: ["POST" OR "GET" OR "PUT" OR "DELETE"]
  * { }.body: { body_of_request }
  * { }.headers: { headers_of_request_as_JSON }  

* The urls is an array of objects. Each Object can contain the properties: url, method, body, headers. Body is only used in PUT and POST. The url and method properties are required.

Example Call:

```javascript
{"urls":
  [
    {
      "url":"http://www.example.com",
      "method":"GET",
      "headers":
        {
          "apikey":"11111111-1111-1111-1111-111111111111",
          "other":"test"
        }
    },
    {
      "url":"http://www.example.com",
      "method":"POST",
      "body":
        {
          "test":"test"
        },
      "headers":
        {
          "apikey":"11111111-1111-1111-1111-111111111111",
          "other":"test"
        }
    }
  ]
}
