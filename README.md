# AI-SQL

Download the `movies.db` file from:

https://cs50.harvard.edu/x/psets/7/movies/

Read the `logic.txt` file.

Check the Jupyter Notebook files for examples of how to use the Harvard `movies.db` database.

Check the `.env` file and configure the required environment variables.

Open Google Colab and select a G4 or A100 GPU runtime.

Upload the `sql_rag_autogen_gpt_oss_20b_baai_bge.ipynb` file to Google Colab.

Upload the `.env` file to the active Google Colab session.

Upload the `requirements_imdb_faiss_autogen_colab_gptoss20b.txt` file to the active Google Colab session.

Install the required dependencies in Google Colab:

```bash
pip install -r requirements_imdb_faiss_autogen_colab_gptoss20b.txt
```

Upload the `movies.db` file to the active Google Colab session.

Upload the following RAG knowledge files to the active Google Colab session:

* `imdb_moviesdb_examples.md`
* `imdb_moviesdb_intent_rules.md`
* `imdb_moviesdb_planner_knowledge.md`
* `imdb_moviesdb_query_plan_schema.md`

Run the Jupyter Notebook in Google Colab.

Execution examples:

Question 1:

await run_question(
    "List the names of all people who starred in Toy Story"
)

Tom Hanks
Tim Allen
Don Rickles
Jim Varney


Question 2:

await run_question(
    "List the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred"
)

Silver Linings Playbook
Serena
American Hustle
Joy

Question 3:

await run_question(
    "List the names of all people who starred in a movie in which Kevin Bacon also starred"
)

Steve Guttenberg
Mickey Rourke
Daniel Stern
Orson Bean
Tommy Citera
Mark Keyloun
David Strathairn
Maria Tucci
Didi Velez
John Lithgow
Lori Singer
Dianne Wiest
Jami Gertz
Rudy Ramos
Paul Rodriguez
Bob Balaban
Michael Beach
Barbara Barrie
Lindsay Crouse
Kyra Sedgwick
Tom Atkins
Sean Astin
K.C. Martel
Jonathan Ward
Alec Baldwin
Elizabeth McGovern
James Ray
Jennifer Jason Leigh
J.T. Walsh
Emily Longstreth
Gary Oldman
Tess Harper
Karen Young
Julia Roberts
William Baldwin
Kiefer Sutherland
Finn Carter
Michael Gross
Fred Ward
Anthony LaPaglia
Nathan Lane
Elizabeth Perkins
Kristin Dattilo
Bruce Payne
Linda Fiorentino
John Malkovich
Joe Mantegna
Tom Cruise
Demi Moore
Jack Nicholson
Charles Gitonga Maina
Winston Ntshona
Yolanda Vazquez
Meryl Streep
Joseph Mazzello
Tom Hanks
Bill Paxton
Gary Sinise
Bridget Fonda
Bob Hoskins
Jim Cummings
Christian Slater
Embeth Davidtz
Brad Pitt
Robert De Niro
Jason Patric
Mary Stuart Masterson
Marian Seldes
Evan Rachel Wood
Jennifer Aniston
Olympia Dukakis
Jay Mohr
Brad Renfro
Calista Flockhart
Maximilian Schell
Neve Campbell
Matt Dillon
Denise Richards
James Doohan
Elya Baskin
Michael Harkins
Diane Lane
Frankie Muniz
Luke Wilson
Elisabeth Shue
Josh Brolin
Kim Dickens
Illeana Douglas
Kathryn Erbe
Zachary David Cope
Charlize Theron
Courtney Love
Stuart Townsend
Tim Robbins
Sean Penn
Emmy Rossum
David Alan Grier
Yasiin Bey
Colin Firth
David Hayman
Alison Lohman
Campbell Scott
Dominic Scott Kay
Brendan Fraser
Andy Garcia
Sarah Michelle Gellar
Jeff Bridges
Mary-Louise Parker
Ryan Reynolds
John Goodman
Kelly Preston
Garrett Hedlund
Marcia Gay Harden
Marin Hinkle
Miles Heizer
Frank Langella
Sam Rockwell
Michael Sheen
Jeffrey Baxter
Russell Ali
Johnny A.
Renée Zellweger
Logan Lerman
Mark Rendall
James McAvoy
Michael Fassbender
Jennifer Lawrence
Liv Tyler
Ellen Page
Rainn Wilson
Ben Affleck
Minnie Driver
Peter Gallagher
Michael Cera
Zooey Deschanel
Rob Corddry
Brittany Flickinger
Djimon Hounsou
Jirantanin Pitakporntrakul
Markus Waldow
Judd Apatow
Henry Beard
Danny Abelson
Tippi Hedren
Robert Patrick
Ray Stevenson
Radha Mitchell
David Mazouz
Lucy Fry
Carmine Appice
Joanna Angel
Jill Anenberg
Kevin Costner
Clint Eastwood
Morgan Freeman
John Calley
Joel Cox
Bill Gerber
Michael Bacon
Pete Seeger
N. Paul Stookey
Nicolas Cage
James Caan
Andreas Michera
Shea Whigham
Hays Wellford
James Freedson-Jackson
Vicky Jenson
Max Chaiet
Barbara Chase-Riboud
Christophe Beck
Richard Blade
Air Supply
Stephen Fellows
Mik Glaisher
Andy Peake
Karen Anderson
Margie Adam
Melanie DeMore



