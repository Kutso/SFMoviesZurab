# SF Movies

SF Movies is a website, which shows where movies have been filmed in San Francisco.

https://sfmovieszurab.herokuapp.com/

## Technical tracks

Application focuses on both front-end and back-end.
I tried to make more working application like, then just a prototype.

## Technical choices and architecture

The architecture gives clean separation between front-end and back-end.
The communicaton is through rest-api services.

Since connecting directly to the third party data provider is a bad idea,
I've implemented data initiator (data_init.py), which is reading all the data, 
normalizing it, and adding some useful missing information (movie poster, imdb ranking) which is probably interesting for the user
and just good addition for the UI.

## Technical choices and justification
	
Front-end : ReactJS - We needed single page application. React is emerging and trending front-end framework, which has insanely good performance.
Web-Api : Python flask - lightweight, reliable, micro-framework. 
Database connecton : SQL ALchemy.
Database : PostgreSQL - open source sql database, with pretty good performance (well supported on heroku).

I am fairly new to the technical stack, especially with react and flask.

## Deploying app

### Front - Building React js

You need npm to build the source code.

```sh
npm install
```
#### Setting development environment
Please open command line tool and run

For Windows
```
set NODE_ENV=development
```
For MacOS and Linux

```
export NODE_ENV=development
```
Run webpack development server

```js
npm run dev
```
and open [http://localhost:1234](http://localhost:1234).

#### Optimize bundle size

To optimize bundle size and prepare for production please set `NODE_ENV` as `production` and run in commandline tool:

```
npm run build
```
There will be generated `app.min.js` in `project/static` folder

#### Production files
* /project/index.html
* /project/static/css/
* /project/static/app.min.js

You have to copy /project/index.html file in template folder and contents of /project/static/ in folder static.


These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

##Backend

You need python to be able to run the application.

#### REST api

The front-end is communicating with back-end using RestAPI Services.
Here are some api endpoints

https://sfmovieszurab.herokuapp.com/api/movies/
https://sfmovieszurab.herokuapp.com/api/movies/2/

https://sfmovieszurab.herokuapp.com/api/locations/
https://sfmovieszurab.herokuapp.com/api/locations/1/

https://sfmovieszurab.herokuapp.com/api/movies/autocomplete/nee/

The api is built using python flask.

#### Database

The data powering the website is stored in PostgreSQL.



#### Requirments

All the requirements are written in requirements.txt folder.
Make sure you pip install all of them in your python environment.

After building the front-end, fill templates and static folders with html, css and js
And to make app launch, run app.py file and open http://localhost:5000/

#### Testing
Run tests.py file to make sure all the tests are OK.



## Authors

* **Zurab Kutsia** 

