# Project Chandra Bot
The [Annual Meeting](http://www.trb.org/AnnualMeeting/AnnualMeeting.aspx) of the [Transportation Research Board (TRB)](http://www.trb.org/Main/Home.aspx) is attended by over 10,000 participants. The core feature of the meeting are sessions devoted to the presentation of research. Research papers are submitted to TRB and assigned to TRB committees. The TRB committees are comprised of volunteers from academia and industry. These committees must review research papers and curate worthy entries into TRB sessions during the narrow time window from the paper deadline on August 31st to the posting of the preliminary Annual Meeting agenda in early December. For committees that receive large numbers of papers, this is a difficult task. The purpose of Project Chandra Bot is to use data and analysis to make the review process more efficient, effective, and fair. The Project name is an homage to [Professor Chandra Bhat](http://www.caee.utexas.edu/prof/bhat/home.html) of the University of Texas -- the idea being that if we could only clone Professor Bhat and have him review each paper, the review process would be perfect.

## Data Model
In order to organize our thinking and structure our code, we started with a data model. It includes:
* Humans -- humans write papers and review papers;
* Papers -- research articles submitted to the Annual Meeting;
* Reviews -- reviews of submitted papers; and,
* Numerous other supporting data types and relationships.

The data model is realized as a [Protocol Buffer](https://developers.google.com/protocol-buffers), which allows a bit of abstraction between the model and the underlying software implementation. 

## Prototype Software
Prototype software is created to efficiently explore the underlying data. It allows for any number of easy examinations. For example, say Reviewer A only uses a portion of the one to five scale used to rate TRB papers, giving each paper a score of 3, 4, or 5. Reviewer B similarly uses a portion of the scale, giving each paper a score of 1, 2, or 3. When a TRB committee receives scores from Reviewer A and Reviewer B, would it not be more efficient, effective, and fair if the committee could easily normalize these scores to each reviewers internal scoring system? The proposition puct forward here is that a useful data model paired with software is the first step in implementing committees with such tooling. A relatively unique feature of the TRB Annual Meeting is that a relatively small number of reviewers review papers from a relatively small number of authors every year. This allows the opportunity to find patterns and extract information from a time series of data that can be made useful in a relatively short period of time.  

## Fake Data
The reviews of academic papers contain sensitive information. To facilitate testing and exploration of the Project's tools, we have created a time series of fake data based on open databases of names, affiliations, and sentences. Any resemblence to real people or reviews is unintentional.

## Humans & Affiliations
One challenge in assembling the database is there is no canonical database of the `humans` that write and review papers. For example, during the course of his career, David Ory (sometimes David T. Ory or D. T. Ory) has been affiliated with Parsons Brinckerhoff (often referred to as PB), the University of California Davis (often referred to as UC Davis), Metropolitan Transportation Commission (sometimes referred to as MTC), Sidewalk Labs, and WSP (which acquired Parsons Brickerhoff and was briefly called WSP|PB). In  order to connect the humans in our community across the papers they author and reviews they write, we need a database that connects canonical names and affiliations with aliases. To do this, we have created an open Google spreadsheet with our first pass at this information. It can be edited by anyone. Please raise an `issue` in the `project-chandra-bot-humans-affiliations` repository or send [David Ory](david.ory@gmail.com) an email if you would like your name removed from this spreadsheet.   

## Project Team
The Project is being led by TRB's Standing Committee on Travel Demand Forecasting. [David Ory](david.ory@gmail.com) is the current chair of this committee and is responsible for the Project. Other team members contributing to the project are:
* [Sijia Wang](https://github.com/i-am-sijia); and,
* [Gayathri Shivaraman](https://github.com/gshivaraman). 