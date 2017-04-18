# PINGuin
##### An API endpoint to check all your API Endpoints   
PINGuin is a REST application that you can post a JSON list of requests to and it will send each request and return the status it recieved. 
<br/>
##### Accepted routes:
* GET: "/" 
  * Returns Readme
* GET: "/{created_path}
  * Requires that a path has been created through POST "/"
  * Returns a status check of all URLs listed in this route
* POST: "/" 
  * Requires JSON Request. See section JSON Format
  * If "saveas" has been specified, saves JSON to new route
  * Returns a status check of all URLs posted in the Request Body
* PUT: "/{created_path}" 
  * Requires JSON Request. See section JSON Format
  * Requires that a path has been created through POST "/"
  * Overwrites the JSON file associated with this route 
  * Returns a status check of all URLs listed in this route
* DELETE: "/{created_path}"
  * Requires that a path has been created through POST "/"
  * Deletes the JSON file associated with this route, and this route
<br/>

##### JSON Format
JSON request is build on:
<br/>
* saveas: file_name.  

* When you add this field the application will remove it, take the remaining JSON request and store it at PINGuin_domain/file_name. There is no need to add ".json" to the end since this application manages the filetype

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
