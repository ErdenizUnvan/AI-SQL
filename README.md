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

