# PLANNER KNOWLEDGE
Project: CS50 IMDb `movies.db` SQL Planning RAG
Version: 1.0

---

## 1. PURPOSE

This knowledge file is used before SQL generation.

Its purpose is:

1. Decide whether a user question is related to the CS50 IMDb `movies.db` database.
2. Identify which table or tables should be used.
3. Identify which columns are relevant.
4. Suggest the correct join path when multiple tables are needed.
5. Identify required filters, ordering, aggregation, limits, and exclusion rules.
6. Produce structured planning information for the next step, where SQL code will be generated and executed.

This file does **not** generate final SQL by itself.
This file only performs database relevance detection, routing intelligence, and query-planning guidance.

---

## 2. AVAILABLE DATABASE

Database file:

```text
movies.db
```

Database domain:

```text
IMDb-style movie database used in CS50x / CS50 SQL exercises.
```

Available tables:

```text
movies
people
stars
directors
ratings
```

---

## 3. HIGH-LEVEL TABLE PURPOSES

### movies

Purpose:

- Stores movie identity, title, and release year.
- Use this table for questions about movie titles, release years, movie counts by year, movie filtering by title, and chronological ordering.

### people

Purpose:

- Stores people involved in movies, such as actors and directors.
- Use this table for questions about names, birth years, actor identity, director identity, and person lookup.

### stars

Purpose:

- Many-to-many relationship table between movies and people who starred in them.
- Use this table when the question is about actors, cast members, starred-in movies, co-stars, or movies involving one or more actors.

### directors

Purpose:

- Many-to-many relationship table between movies and people who directed them.
- Use this table when the question is about directors or movies directed by a person.

### ratings

Purpose:

- Stores IMDb rating and vote count per movie.
- Use this table when the question asks about rating, votes, highest rated movies, average rating, or filtering movies by rating threshold.

---

## 4. TABLE SCHEMAS AND SEMANTIC MEANINGS

### movies

```sql
CREATE TABLE movies (
    id INTEGER,
    title TEXT NOT NULL,
    year NUMERIC,
    PRIMARY KEY(id)
)
```

Columns:

- `id`
  - Role: primary key, movie identifier.
  - Meaning: Unique ID for each movie.
  - Join usage: Join to `stars.movie_id`, `directors.movie_id`, and `ratings.movie_id`.

- `title`
  - Role: descriptive attribute.
  - Meaning: Movie title.
  - Use for: Listing movies, filtering by title or franchise, alphabetical ordering.

- `year`
  - Role: temporal attribute.
  - Meaning: Movie release year.
  - Use for: Filtering movies by release year, chronological ordering, grouping by year.

---

### people

```sql
CREATE TABLE people (
    id INTEGER,
    name TEXT NOT NULL,
    birth NUMERIC,
    PRIMARY KEY(id)
)
```

Columns:

- `id`
  - Role: primary key, person identifier.
  - Meaning: Unique ID for each person.
  - Join usage: Join to `stars.person_id` and `directors.person_id`.

- `name`
  - Role: descriptive attribute.
  - Meaning: Person name.
  - Use for: Actor lookup, director lookup, listing names, filtering by exact person name.

- `birth`
  - Role: temporal/person attribute.
  - Meaning: Birth year of the person.
  - Use for: Returning birth year, ordering people by birth year, disambiguating people with the same name.

---

### stars

```sql
CREATE TABLE stars (
    movie_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    FOREIGN KEY(movie_id) REFERENCES movies(id),
    FOREIGN KEY(person_id) REFERENCES people(id)
)
```

Columns:

- `movie_id`
  - Role: foreign key.
  - Meaning: Movie in which the person starred.
  - Join usage: Join to `movies.id`.

- `person_id`
  - Role: foreign key.
  - Meaning: Person who starred in the movie.
  - Join usage: Join to `people.id`.

Analytical meaning:

- Each row means: this person starred in this movie.
- Use for actor/movie relationship questions.
- Use this table twice for co-star questions or questions asking whether two actors starred in the same movie.

---

### directors

```sql
CREATE TABLE directors (
    movie_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    FOREIGN KEY(movie_id) REFERENCES movies(id),
    FOREIGN KEY(person_id) REFERENCES people(id)
)
```

Columns:

- `movie_id`
  - Role: foreign key.
  - Meaning: Movie directed by the person.
  - Join usage: Join to `movies.id`.

- `person_id`
  - Role: foreign key.
  - Meaning: Person who directed the movie.
  - Join usage: Join to `people.id`.

Analytical meaning:

- Each row means: this person directed this movie.
- Use for director/movie relationship questions.

---

### ratings

```sql
CREATE TABLE ratings (
    movie_id INTEGER NOT NULL,
    rating REAL NOT NULL,
    votes INTEGER NOT NULL,
    FOREIGN KEY(movie_id) REFERENCES movies(id)
)
```

Columns:

- `movie_id`
  - Role: foreign key.
  - Meaning: Movie being rated.
  - Join usage: Join to `movies.id`.

- `rating`
  - Role: metric.
  - Meaning: IMDb rating score.
  - Use for: Filtering by rating, sorting by rating, average rating, highest-rated movies.

- `votes`
  - Role: metric/context.
  - Meaning: Number of IMDb votes.
  - Use for: Popularity, confidence, optional tie-breaking, filtering by vote count if requested.

---

## 5. COMMON DATA MODEL UNDERSTANDING

This database has two entity tables and three relationship/metric tables.

Entity tables:

```text
movies
people
```

Relationship tables:

```text
stars
directors
```

Metric table:

```text
ratings
```

Important meaning:

- A person can star in many movies.
- A movie can have many stars.
- A person can direct many movies.
- A movie can have one or more directors.
- A movie can have one rating row.

---

## 6. JOIN RULES

### Rule 1: Movie to rating

Use when question involves rating, votes, highest rated, average rating, or rating threshold.

Join:

```sql
movies.id = ratings.movie_id
```

Confidence: High

---

### Rule 2: Movie to actor / cast

Use when question involves actors, stars, cast, starred in, appeared in, or co-stars.

Join path:

```sql
movies.id = stars.movie_id
stars.person_id = people.id
```

Confidence: High

---

### Rule 3: Movie to director

Use when question involves directors, directed by, or people who directed movies.

Join path:

```sql
movies.id = directors.movie_id
directors.person_id = people.id
```

Confidence: High

---

### Rule 4: Movie + actor + rating

Use when question asks for rated movies involving a specific actor.

Join path:

```sql
people.id = stars.person_id
stars.movie_id = movies.id
movies.id = ratings.movie_id
```

Confidence: High

---

### Rule 5: Movie + director + rating

Use when question asks for directors of high-rated movies or ratings of directed movies.

Join path:

```sql
people.id = directors.person_id
directors.movie_id = movies.id
movies.id = ratings.movie_id
```

Confidence: High

---

### Rule 6: Two actors in the same movie

Use when question asks for movies where both Actor A and Actor B starred.

Use `stars` twice and `people` twice.

Join logic:

```sql
movies.id = s1.movie_id
movies.id = s2.movie_id
s1.person_id = p1.id
s2.person_id = p2.id
p1.name = actor_1
p2.name = actor_2
```

Equivalent condition:

```sql
s1.movie_id = s2.movie_id
```

Confidence: High

---

### Rule 7: Co-stars of a target actor

Use when question asks for people who starred in a movie with a target actor.

Use `stars` twice and `people` twice.

Join logic:

```sql
p_target.id = s_target.person_id
s_target.movie_id = s_other.movie_id
s_other.person_id = p_other.id
```

Required exclusion:

```sql
p_other.id != p_target.id
```

Use `DISTINCT` to avoid duplicate names because the same co-star may appear with the target actor in multiple movies.

Confidence: High

---

## 7. TABLE GRAINS

### movies

Primary grain:

```text
one row per movie
```

Primary key:

```text
id
```

---

### people

Primary grain:

```text
one row per person
```

Primary key:

```text
id
```

---

### stars

Primary grain:

```text
one row per movie-person actor relationship
```

Composite relationship:

```text
movie_id, person_id
```

---

### directors

Primary grain:

```text
one row per movie-person director relationship
```

Composite relationship:

```text
movie_id, person_id
```

---

### ratings

Primary grain:

```text
one row per rated movie
```

Join key:

```text
movie_id
```

---

## 8. PRIMARY ROUTING RULES

If the question is mainly about movie titles or release years:

```text
Route primarily to movies
```

If the question is mainly about a person name or birth year:

```text
Route primarily to people
```

If the question asks who starred in a movie, which movies an actor starred in, or co-stars:

```text
Route to movies + stars + people
```

If the question asks who directed a movie or which directors meet a condition:

```text
Route to movies + directors + people
```

If the question asks about ratings, votes, highest rated, rating thresholds, or average rating:

```text
Route to movies + ratings
```

If the question combines actors with ratings:

```text
Route to people + stars + movies + ratings
```

If the question combines directors with ratings:

```text
Route to people + directors + movies + ratings
```

If the question asks about two actors in the same movie:

```text
Route to people + stars + movies using self-join logic on stars
```

---

## 9. KEYWORD-BASED INTENT SIGNALS

### movie intent signals

- movie
- movies
- title
- titles
- film
- films
- released
- release date
- release year
- year
- chronological
- alphabetical

### person intent signals

- person
- people
- name
- names
- birth
- born
- birth year

### actor/star intent signals

- starred
- stars
- actor
- actress
- cast
- appeared in
- acted in
- co-star
- costar
- with

### director intent signals

- directed
- director
- directors
- filmmaker

### rating intent signals

- rating
- rated
- IMDb rating
- highest rated
- average rating
- votes
- vote count
- score
- at least

### aggregation intent signals

- number of
- count
- how many
- average
- avg
- mean

### ordering intent signals

- order
- ordered
- sort
- sorted
- alphabetical
- chronological
- descending
- ascending
- highest
- lowest

### limit intent signals

- top
- first
- five
- 5
- ten
- 10
- highest rated

---

## 10. QUESTION TYPE ROUTING TEMPLATES

### Template A: Movies by exact release year

Use when question asks:

- List titles of all movies released in a specific year.

Primary table:

```text
movies
```

Required columns:

```text
title, year
```

Filter:

```text
movies.year = target_year
```

Output:

```text
title
```

Typical SQL pattern:

```sql
SELECT title
FROM movies
WHERE year = :target_year;
```

---

### Template B: Person birth year

Use when question asks:

- Determine the birth year of a named person.

Primary table:

```text
people
```

Required columns:

```text
name, birth
```

Filter:

```text
people.name = target_person_name
```

Output:

```text
birth
```

Typical SQL pattern:

```sql
SELECT birth
FROM people
WHERE name = :person_name;
```

---

### Template C: Movies released on or after a year, alphabetical

Use when question asks:

- Movies released on or after a target year.
- Ordered alphabetically.

Primary table:

```text
movies
```

Required columns:

```text
title, year
```

Filter:

```text
movies.year >= target_year
```

Ordering:

```text
ORDER BY title ASC
```

Typical SQL pattern:

```sql
SELECT title
FROM movies
WHERE year >= :target_year
ORDER BY title ASC;
```

---

### Template D: Count movies by exact rating

Use when question asks:

- Number of movies with a specific IMDb rating.

Primary table:

```text
ratings
```

Optional table:

```text
movies, only if movie details are requested
```

Required columns:

```text
rating
```

Aggregation:

```text
COUNT(*)
```

Filter:

```text
ratings.rating = target_rating
```

Typical SQL pattern:

```sql
SELECT COUNT(*)
FROM ratings
WHERE rating = :target_rating;
```

---

### Template E: Franchise movies by title pattern

Use when question asks:

- Movies from a franchise, e.g. Harry Potter movies.

Primary table:

```text
movies
```

Required columns:

```text
title, year
```

Filter:

```text
movies.title LIKE '%franchise_keyword%'
```

Ordering:

```text
ORDER BY year ASC
```

Typical SQL pattern:

```sql
SELECT title, year
FROM movies
WHERE title LIKE :title_pattern
ORDER BY year ASC;
```

---

### Template F: Average rating of movies released in a year

Use when question asks:

- Average rating of all movies released in a specific year.

Tables:

```text
movies, ratings
```

Join:

```text
movies.id = ratings.movie_id
```

Aggregation:

```text
AVG(ratings.rating)
```

Filter:

```text
movies.year = target_year
```

Typical SQL pattern:

```sql
SELECT AVG(rating)
FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE year = :target_year;
```

---

### Template G: Movies and ratings by release year ordered by rating

Use when question asks:

- Movies released in a specific year and their ratings.
- Ordered by rating.

Tables:

```text
movies, ratings
```

Join:

```text
movies.id = ratings.movie_id
```

Output:

```text
title, rating
```

Filter:

```text
movies.year = target_year
```

Ordering:

```text
ORDER BY ratings.rating DESC
```

Typical SQL pattern:

```sql
SELECT title, rating
FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE year = :target_year
ORDER BY rating DESC;
```

---

### Template H: Actors who starred in a specific movie

Use when question asks:

- List names of people who starred in a named movie.

Tables:

```text
movies, stars, people
```

Join:

```text
movies.id = stars.movie_id
stars.person_id = people.id
```

Filter:

```text
movies.title = target_movie_title
```

Output:

```text
people.name
```

Typical SQL pattern:

```sql
SELECT name
FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE title = :movie_title;
```

---

### Template I: Actors in movies released in a year, ordered by birth year

Use when question asks:

- People who starred in movies released in a target year.
- Ordered by birth year.

Tables:

```text
movies, stars, people
```

Join:

```text
movies.id = stars.movie_id
stars.person_id = people.id
```

Filter:

```text
movies.year = target_year
```

Output:

```text
people.name
```

Ordering:

```text
ORDER BY people.birth ASC
```

Use `DISTINCT` when duplicate people may appear in multiple movies in the same year.

Typical SQL pattern:

```sql
SELECT DISTINCT name
FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE year = :target_year
ORDER BY birth ASC;
```

---

### Template J: Directors of movies with rating threshold

Use when question asks:

- People who directed a movie that received rating at least X.

Tables:

```text
people, directors, movies, ratings
```

Join:

```text
people.id = directors.person_id
directors.movie_id = movies.id
movies.id = ratings.movie_id
```

Filter:

```text
ratings.rating >= target_rating
```

Output:

```text
people.name
```

Use `DISTINCT` because a director may have multiple highly rated movies.

Typical SQL pattern:

```sql
SELECT DISTINCT name
FROM people
JOIN directors ON people.id = directors.person_id
JOIN movies ON directors.movie_id = movies.id
JOIN ratings ON movies.id = ratings.movie_id
WHERE rating >= :target_rating;
```

---

### Template K: Top rated movies starring a specific actor

Use when question asks:

- Titles of top N highest rated movies that a named actor starred in.

Tables:

```text
people, stars, movies, ratings
```

Join:

```text
people.id = stars.person_id
stars.movie_id = movies.id
movies.id = ratings.movie_id
```

Filter:

```text
people.name = target_actor_name
```

Ordering:

```text
ORDER BY ratings.rating DESC
```

Limit:

```text
LIMIT target_n
```

Optional tie-break:

```text
ratings.votes DESC
```

Typical SQL pattern:

```sql
SELECT title
FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
JOIN ratings ON movies.id = ratings.movie_id
WHERE people.name = :actor_name
ORDER BY rating DESC
LIMIT :n;
```

---

### Template L: Movies where two actors both starred

Use when question asks:

- Movies in which Actor A and Actor B both starred.

Tables:

```text
movies, stars AS s1, stars AS s2, people AS p1, people AS p2
```

Join:

```text
movies.id = s1.movie_id
movies.id = s2.movie_id
s1.person_id = p1.id
s2.person_id = p2.id
```

Filters:

```text
p1.name = actor_1
p2.name = actor_2
```

Output:

```text
movies.title
```

Typical SQL pattern:

```sql
SELECT movies.title
FROM movies
JOIN stars AS s1 ON movies.id = s1.movie_id
JOIN people AS p1 ON s1.person_id = p1.id
JOIN stars AS s2 ON movies.id = s2.movie_id
JOIN people AS p2 ON s2.person_id = p2.id
WHERE p1.name = :actor_1
  AND p2.name = :actor_2;
```

---

### Template M: Co-stars of a target actor

Use when question asks:

- People who starred in a movie in which target actor also starred.

Tables:

```text
people AS target_person
stars AS target_stars
stars AS other_stars
people AS other_people
```

Join:

```text
target_person.id = target_stars.person_id
target_stars.movie_id = other_stars.movie_id
other_stars.person_id = other_people.id
```

Filter:

```text
target_person.name = target_actor_name
```

Required exclusion:

```text
other_people.id != target_person.id
```

Output:

```text
DISTINCT other_people.name
```

Typical SQL pattern:

```sql
SELECT DISTINCT other_people.name
FROM people AS target_person
JOIN stars AS target_stars ON target_person.id = target_stars.person_id
JOIN stars AS other_stars ON target_stars.movie_id = other_stars.movie_id
JOIN people AS other_people ON other_stars.person_id = other_people.id
WHERE target_person.name = :actor_name
  AND other_people.id != target_person.id;
```

---

## 11. RELEVANCE DECISION POLICY

Set `is_related = true` when:

- The question is about movies, titles, release years, actors, directors, people, birth years, ratings, votes, casts, co-stars, or film relationships represented in `movies.db`.
- The question asks for SQL-like retrieval, filtering, sorting, counting, averaging, or joining over the IMDb database.
- The question can be answered using the available tables: `movies`, `people`, `stars`, `directors`, `ratings`.

Set `is_related = false` when:

- The question is unrelated to the IMDb database.
- The question requires external movie facts not stored in the database.
- The question asks for opinions, summaries, reviews, plot details, genres, countries, box office, awards, streaming availability, or other fields not represented in the database.
- The question is about general SQL theory without needing this database.

---

## 12. IMPORTANT ASSUMPTIONS

1. `movies.id` is the canonical movie key.
2. `people.id` is the canonical person key.
3. `stars` represents actor/cast relationships, not directors.
4. `directors` represents director relationships, not actors.
5. `ratings.rating` is the IMDb rating score.
6. `ratings.votes` is available only when vote count or tie-breaking is needed.
7. Exact name filters should use `people.name = ?` unless fuzzy search is explicitly requested.
8. Exact title filters should use `movies.title = ?` unless franchise/pattern search is requested.
9. Use `DISTINCT` when joining through many-to-many relationships and the requested output may duplicate.
10. The SQL generator should verify that selected columns exist before execution.

---

## 13. FINAL DECISION PRINCIPLE

Always select the smallest correct set of tables and columns needed to answer the question.

Do not include unnecessary tables.
Do not include unnecessary columns.
Prefer exact routing first.
Use self-joins only when the question explicitly requires co-star or same-movie relationship logic.
Use aggregation only when the question asks for count, number, average, or similar summary result.
