



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/orhannurkan/AI-for-Document-Automation">
    <img src="partena.jpg" alt="Logo" width="240" height="180">
  </a>
  <a href="https://github.com/orhannurkan/AI-for-Document-Automation">
    <img src="KPMG.jpg" alt="Logo" width="240" height="180">
  </a>

  <h1 align="center">KPMG project</h1>
  <h3 align="center">Last Becode project for KPMG</h3>

  <p align="center">
    by  Opap's D., Orhan N., Dilara P., Ankita H. and Adam F.
    <br />
    
  </p>
</p>




## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
* [Building The Database](#building-the-database)
* [Text Extraction](#text-extraction)
* [Data Structuring](#data-structuring)
* [User Interface](#user-interface)
* [How went our project?](#how-went-our-project?)




## About The Project

Partena reached out KPMG to optimize the tool they use to find information in law text stored in pdf files on a government. The real issue was the fact that they lose much of their time in searching the information they need. In order to solve it, we provided a solution that improve by far the search process. Designed from the user interface to the database, we also made a text extraction system so every bits of important data is reachable within seconds.


## Getting Started

To get started, we began by scraping the government's website to get all the stored PDF. We've quickly done that because we noticed that it was just working with basic API calls. We then made a pipeline so it'll update by itself to gather every new PDF uploaded.


## Building The Database

We made a SQL database to store all the pdf and their data.


## Text Extraction

It was the tricky part. 

As it is a government website and Belgium is a multilingual country, all pdf has one side in Dutch and the other in French. 
Not always on the same side.
The pdf were not in great quality and sometimes they contain handwritting. 
So it was quite challenging to have a nice text extraction method working.





## Data Structuring

In order to make the product more efficient, we manage to structure the text in chapters, articles and sub-articles.
It is not working perfectly yet, but we had some good results about it.



## User Interface 

You can find it on this link.

The user can choose between several themes, and select a topic. The web app will display all the CLA from the themes and the topic that the user had chosen.
You can directly click on the CLA that interest you the most and it will display the pdf as well as all the relevant data that concerns it.




## How went our project?

This has been a great experience for us all. This is the first time that we have a project that lasts 3 weeks. And we could build more functionalities if we had a bit more time.





