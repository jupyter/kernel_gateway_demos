# Kernel Gateway Microservice Demonstration

The [Kernel Gateway](https://github.com/jupyter-incubator/kernel_gateway) is a
[JupyterApp](https://github.com/jupyter/jupyter_core/blob/master/jupyter_core/application.py) that
implements different APIs and protocols for accessing Jupyter kernels.  We can use the Jupyter kernel gateway to
[process requests](https://github.com/jupyter-incubator/kernel_gateway#processing-requests) and transform an
annotated notebook into a HTTP API using the Jupyter kernel gateway.
 
This example shows how one can use the Jupyter kernel gateway to deploy an notebook as a
microservice at the heart of a Twitter bot, using a combination of [Alchemy API](http://www.alchemyapi.com/products/alchemylanguage/entity-extraction) with IFTTT's [Twitter](https://ifttt.com/twitter) and [Maker](https://ifttt.com/maker) channels, to respond to mentions with a search URL for relevant Meetups. You will need developer keys for [Alchemy](http://www.alchemyapi.com/api/register.html) and [Maker](https://ifttt.com/maker) to proceed, as well as an arbitrary Event Name for use with Maker.

### Build the docker container
```
make build
```

### Run the docker container for the service
Either set the ALCHEMY_KEY, MAKER_KEY, and MAKER_EVENT_NAME environment variables accordingly or pass them along directly in the arguments. These values are passed into the docker container, read and used by the notebook, and must still be set if running the Jupyter kernel gateway outside of a container.
```
make run ALCHEMY_KEY=your_key MAKER_KEY=your_other_key MAKER_EVENT_NAME=your_event
```

### Connecting the service to Twitter
To connect it all together, first create an `If Twitter Then Maker` Recipe on IFTTT using a Twitter mention to then make a web request to the docker container, on the default port 8888, with the relative URI:
```
/generate_search_url?text=<<<{{Text}}>>>&user={{UserName}}
```
and the GET method. Then, create an `If Maker Then Twitter` recipe starting from a Maker Event, using the event name chosen earlier, and have it then post a Tweet with the text:
```
.{{Value1}} you can find meetups near {{Value2}} at {{Value3}}
```
 Now assembled, a tweet at the bot will trigger the microservice, which in turn will call Alchemy and attempt to extract a location from the Tweet, and trigger the intended Maker event with a Meetup search URL, which will finally be Tweeted by the bot account.
 
 You can trigger the the `generate_search_url` endpoint manually with `curl`:
 ```
 curl -v 'http://host_ip:8888/generate_search_url?text=tweet+with+location&user=twitterHandle'
 ```
A running copy of the notebook can also be found at http://104.236.203.57:8887/api/generate_search_url , powering the @BluemixMeetups demo bot. Keep in mind that when using it through Twitter, there will be a slight delay between when mentions are tweeted and when the service is notified through IFTTT.