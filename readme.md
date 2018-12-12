There are ways to organize the flask codebase, I suggest this one, which follows TDD and RESTful philosophy. Taking a typical store-items context as an example
1/ RESTful: this revolves around the "resource" concept, we have a folder name "resource", and say, if we want to navigate to the "GET" of resource "store", it is as easy as navigating to resource/items.py 

2/ TDD: there are several sub-folders: unit, integration, system

"unit" folder includes tests involve single unit only, in the example, I have a folder "models" to deal with data layer (ORM, for e.g) which has a StoreModel(db.Model) as follows

"integration" folder includes tests that have interactions among more than one units, e.g. store-items relationship test can be here

"system" folder includes tests as the whole system run


3/ Test runners: running tests locally should be easy and fast, whether it is running a single test, a bunch of tests under "unit", or all the tests including "integration" or "system". It should all be as easy as right-click-select or a hot key... when there are interactions with other system (dynamodb, redis,...), some developers set up their own local environment. I propose here a way to use docker-compose within the IDE environment (PyCharm), local docker is a bit slower than local native runner, but the plus is the set-up process is easy, and any developer can get up to speed very fast avoiding the annoying set up phase.

The docker-compose.yml e.g. set up the flask app and a postgres instance

Then we have another docker-compose.dev.yml to set up the environment variables for dev

And then add both of the files to pycharm project interpreter setting

And boom from here, whenever the test runner runs, it will interact with the local dockers instead, debugging works the same...
