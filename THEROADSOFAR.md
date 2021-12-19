---
## The process
This file describes the main ideas used to complete the challenge.

---
## Choosing Pandas as the library for the DataFrame
In this challenge I use Pandas DataFrames because:
- The response from the API is relatively small, and we do not need parallel processing to boost our application performance.
- The installation is easy and don't require extra components to our docker image (like Java, OpenJDK, etc)

---
## Results directory
Doing the Challenge I did feel the need to implement some sort of Datalake layer approach. 
In this challenge, it only contains the Raw and the Cleaned directories. The Raw folder contains all the results gotten from the API.
In the Cleaned directory the application writes the json file after all the requested processing is done.

---
## Tests
To perform the tests I choose the python library unittest because it is native, and it provides an easy way to implement the tests

---
## Challenges and learning
Making this challenge I ask myself several times what library to use to process the DataFrame and I even implemented a simple version in Spark.
The problem with that was the size of the final docker image. It was a lot bigger and took much more time to be built.
In terms of processing time it had not much gain using, so I decided to stay with Pandas.
I choose the solution implementation as application instead of using a Databricks or Jupyter notebook because it is easier to maintain over time,
and make the code easier to test, modulate and run.
The Dataframe thought is only printed and can be used after by reading again the json output.