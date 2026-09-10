# IMDb movies.db Intent Router and Rule Injection Guide
Version: 1.0

---

## 1. PURPOSE

This file defines deterministic rules that should run before RAG retrieval and LLM planning.

The goal is to inject strong constraints into the planner so the LLM does not guess table usage or join logic.

Pipeline position:

```text
User Question
  -> Intent Router
  -> Rule Injection Engine
  -> RAG Retrieval
  -> LLM Planner
  -> Plan Validator
  -> SQL Generator
  -> SQL Validator
  -> Execution Engine
  -> Answer Generator
```

---

## 2. INTENT FAMILIES

```python
intent_keywords = {
    "movie_lookup": [
        "movie", "movies", "title", "titles", "film", "films", "released", "release", "year"
    ],
    "person_lookup": [
        "person", "people", "name", "names", "birth", "born", "birth year"
    ],
    "actor_star": [
        "starred", "stars", "actor", "actress", "cast", "appeared", "acted", "co-star", "costar"
    ],
    "director": [
        "directed", "director", "directors", "filmmaker"
    ],
    "rating": [
        "rating", "rated", "imdb rating", "highest rated", "average rating", "votes", "score", "at least"
    ],
    "aggregation": [
        "number of", "count", "how many", "average", "avg", "mean"
    ],
    "ordering": [
        "order", "ordered", "sort", "sorted", "alphabetical", "chronological", "descending", "ascending", "highest", "lowest"
    ],
    "limit": [
        "top", "first", "five", "5", "ten", "10", "highest rated"
    ],
    "co_star": [
        "both", "together", "same movie", "also starred", "co-star", "costar", "with"
    ],
    "franchise": [
        "harry potter", "star wars", "lord of the rings", "franchise", "series"
    ]
}
```

---

## 3. DETERMINISTIC QUESTION TYPE RULES

### Rule A: Movies by exact year

Signals:

- Mentions movie titles.
- Mentions released in a specific year.
- Does not mention actors, directors, or ratings.

Forced question type:

```text
movies_by_exact_year
```

Required tables:

```text
movies
```

Preferred columns:

```text
movies.title
movies.year
```

Required filter:

```text
movies.year = target_year
```

---

### Rule B: Person birth year

Signals:

- Mentions birth year or born.
- Mentions a person name.

Forced question type:

```text
person_birth_year
```

Required tables:

```text
people
```

Preferred columns:

```text
people.name
people.birth
```

Required filter:

```text
people.name = target_person_name
```

---

### Rule C: Movies after year alphabetically

Signals:

- Mentions movies released on or after a year.
- Mentions alphabetical order.

Forced question type:

```text
movies_after_year_alphabetical
```

Required tables:

```text
movies
```

Required filter:

```text
movies.year >= target_year
```

Required ordering:

```text
movies.title ASC
```

---

### Rule D: Count movies by rating

Signals:

- Mentions number/count.
- Mentions IMDb rating equal to a numeric value.

Forced question type:

```text
count_movies_by_exact_rating
```

Required tables:

```text
ratings
```

Preferred columns:

```text
ratings.rating
```

Required aggregation:

```text
COUNT(*)
```

Required filter:

```text
ratings.rating = target_rating
```

---

### Rule E: Franchise title search

Signals:

- Mentions a franchise or title family, such as Harry Potter.
- Asks for title and release year.
- Mentions chronological order.

Forced question type:

```text
franchise_movies_chronological
```

Required tables:

```text
movies
```

Required filter:

```text
movies.title LIKE '%target_franchise_keyword%'
```

Required ordering:

```text
movies.year ASC
```

---

### Rule F: Average rating by release year

Signals:

- Mentions average rating.
- Mentions movies released in a specific year.

Forced question type:

```text
average_rating_by_year
```

Required tables:

```text
movies
ratings
```

Required join:

```text
movies.id = ratings.movie_id
```

Required aggregation:

```text
AVG(ratings.rating)
```

Required filter:

```text
movies.year = target_year
```

---

### Rule G: Movies with ratings by year

Signals:

- Mentions movies released in a specific year.
- Asks for their ratings.
- Mentions descending order by rating.

Forced question type:

```text
movies_and_ratings_by_year_desc
```

Required tables:

```text
movies
ratings
```

Required join:

```text
movies.id = ratings.movie_id
```

Required output columns:

```text
movies.title
ratings.rating
```

Required ordering:

```text
ratings.rating DESC
```

---

### Rule H: Actors in a movie

Signals:

- Mentions people who starred in a named movie.

Forced question type:

```text
actors_in_movie
```

Required tables:

```text
movies
stars
people
```

Required joins:

```text
movies.id = stars.movie_id
stars.person_id = people.id
```

Required filter:

```text
movies.title = target_movie_title
```

---

### Rule I: Actors in movies by year ordered by birth

Signals:

- Mentions people who starred in movies released in a year.
- Mentions ordered by birth year.

Forced question type:

```text
actors_in_movies_by_year_order_birth
```

Required tables:

```text
movies
stars
people
```

Required joins:

```text
movies.id = stars.movie_id
stars.person_id = people.id
```

Required filter:

```text
movies.year = target_year
```

Required ordering:

```text
people.birth ASC
```

Use distinct:

```text
true
```

---

### Rule J: Directors of highly rated movies

Signals:

- Mentions people who directed movies.
- Mentions rating at least X.

Forced question type:

```text
directors_of_high_rated_movies
```

Required tables:

```text
people
directors
movies
ratings
```

Required joins:

```text
people.id = directors.person_id
directors.movie_id = movies.id
movies.id = ratings.movie_id
```

Required filter:

```text
ratings.rating >= target_rating
```

Use distinct:

```text
true
```

---

### Rule K: Highest rated movies by actor

Signals:

- Mentions highest rated movies.
- Mentions a named actor.
- Mentions limit, such as five.

Forced question type:

```text
highest_rated_movies_by_actor
```

Required tables:

```text
people
stars
movies
ratings
```

Required joins:

```text
people.id = stars.person_id
stars.movie_id = movies.id
movies.id = ratings.movie_id
```

Required filter:

```text
people.name = target_actor_name
```

Required ordering:

```text
ratings.rating DESC
```

Required limit:

```text
target_n
```

Optional tie-break:

```text
ratings.votes DESC
```

---

### Rule L: Movies with two specific actors

Signals:

- Mentions movies in which both Actor A and Actor B starred.

Forced question type:

```text
movies_with_two_actors
```

Required tables:

```text
movies
stars AS s1
stars AS s2
people AS p1
people AS p2
```

Required self-join logic:

```text
s1.movie_id = s2.movie_id
s1.person_id = p1.id
s2.person_id = p2.id
movies.id = s1.movie_id
```

Required filters:

```text
p1.name = actor_1
p2.name = actor_2
```

---

### Rule M: Co-stars of target actor

Signals:

- Mentions people who starred in a movie in which target actor also starred.

Forced question type:

```text
costars_of_actor
```

Required tables:

```text
people AS target_person
stars AS target_stars
stars AS other_stars
people AS other_people
```

Required self-join logic:

```text
target_person.id = target_stars.person_id
target_stars.movie_id = other_stars.movie_id
other_stars.person_id = other_people.id
```

Required filter:

```text
target_person.name = target_actor_name
```

Required exclusion:

```text
other_people.id != target_person.id
```

Use distinct:

```text
true
```

---

## 4. RULE INJECTION OUTPUT FORMAT

The Rule Injection Engine should return a dictionary like this:

```json
{
  "detected_intents": ["actor_star", "rating", "limit"],
  "forced_question_type": "highest_rated_movies_by_actor",
  "required_tables": ["people", "stars", "movies", "ratings"],
  "required_joins": [
    {"left": "people.id", "right": "stars.person_id"},
    {"left": "stars.movie_id", "right": "movies.id"},
    {"left": "movies.id", "right": "ratings.movie_id"}
  ],
  "preferred_columns": ["movies.title", "ratings.rating", "ratings.votes", "people.name"],
  "required_filters": ["people.name = target_actor_name"],
  "required_ordering": [{"column": "ratings.rating", "direction": "DESC"}],
  "required_limit": 5,
  "use_distinct": false,
  "forbidden_tables": [],
  "reason": "The question asks for the five highest rated movies starring a named actor."
}
```

---

## 5. FORBIDDEN / SAFETY RULES

SQL generation should not produce:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
PRAGMA write operations
ATTACH
DETACH
```

Only read-only `SELECT` queries are allowed.

The generated SQL must use only these tables:

```text
movies
people
stars
directors
ratings
```

The generated SQL must use only columns documented in the schema.

