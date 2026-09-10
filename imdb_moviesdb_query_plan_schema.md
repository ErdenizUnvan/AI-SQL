# IMDb movies.db Query Plan JSON Schema
Version: 1.0

---

## 1. PURPOSE

This file defines the structured JSON variable that the LLM planner should produce before SQL generation.

The SQL generator should consume this JSON instead of relying directly on the raw user question.

---

## 2. REQUIRED JSON OUTPUT SHAPE

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "highest_rated_movies_by_actor",
  "confidence": "high",
  "target_entities": {
    "movie_title": null,
    "person_name": "Chadwick Boseman",
    "person_name_2": null,
    "year": null,
    "rating": null,
    "franchise_keyword": null,
    "limit": 5
  },
  "tables": [
    {
      "name": "people",
      "alias": null,
      "purpose": "Filter the target actor by name."
    },
    {
      "name": "stars",
      "alias": null,
      "purpose": "Connect the actor to movies they starred in."
    },
    {
      "name": "movies",
      "alias": null,
      "purpose": "Return movie titles."
    },
    {
      "name": "ratings",
      "alias": null,
      "purpose": "Sort movies by IMDb rating."
    }
  ],
  "columns": {
    "select": ["movies.title"],
    "filter": ["people.name"],
    "join": ["people.id", "stars.person_id", "stars.movie_id", "movies.id", "ratings.movie_id"],
    "order_by": ["ratings.rating"],
    "aggregation": []
  },
  "joins": [
    {
      "left": "people.id",
      "right": "stars.person_id",
      "type": "INNER",
      "reason": "Connect each person to the movies they starred in."
    },
    {
      "left": "stars.movie_id",
      "right": "movies.id",
      "type": "INNER",
      "reason": "Connect starring records to movie titles."
    },
    {
      "left": "movies.id",
      "right": "ratings.movie_id",
      "type": "INNER",
      "reason": "Attach IMDb ratings to each movie."
    }
  ],
  "filters": [
    {
      "column": "people.name",
      "operator": "=",
      "value": "Chadwick Boseman",
      "reason": "The question asks about movies starring Chadwick Boseman."
    }
  ],
  "aggregation": null,
  "distinct": false,
  "ordering": [
    {
      "column": "ratings.rating",
      "direction": "DESC",
      "reason": "The question asks for highest rated movies first."
    }
  ],
  "limit": 5,
  "exclusions": [],
  "expected_output": "A list of movie titles.",
  "requires_self_join": false,
  "safety": {
    "read_only": true,
    "allowed_statement": "SELECT",
    "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]
  },
  "reason": "The question asks for the five highest rated movies starring Chadwick Boseman, so it requires people, stars, movies, and ratings."
}
```

---

## 3. FIELD DEFINITIONS

### is_related

Boolean.

Set to `true` if the question can be answered using `movies.db`.
Set to `false` if unrelated.

---

### database

Always:

```text
movies.db
```

---

### sql_dialect

Always:

```text
sqlite
```

---

### question_type

Allowed values:

```text
movies_by_exact_year
person_birth_year
movies_after_year_alphabetical
count_movies_by_exact_rating
franchise_movies_chronological
average_rating_by_year
movies_and_ratings_by_year_desc
actors_in_movie
actors_in_movies_by_year_order_birth
directors_of_high_rated_movies
highest_rated_movies_by_actor
movies_with_two_actors
costars_of_actor
unrelated
```

---

### confidence

Allowed values:

```text
high
medium
low
```

---

### target_entities

Use this to store extracted variables from the user question.

Possible fields:

```json
{
  "movie_title": null,
  "person_name": null,
  "person_name_2": null,
  "year": null,
  "rating": null,
  "franchise_keyword": null,
  "limit": null
}
```

---

### tables

Each table object should explain why the table is needed.

Example:

```json
{
  "name": "movies",
  "alias": null,
  "purpose": "Return movie titles and filter by release year."
}
```

---

### columns

Group columns by role:

```json
{
  "select": [],
  "filter": [],
  "join": [],
  "order_by": [],
  "aggregation": []
}
```

---

### joins

Each join must include:

```json
{
  "left": "movies.id",
  "right": "ratings.movie_id",
  "type": "INNER",
  "reason": "Attach ratings to movies."
}
```

For self-joins, aliases must be used.

---

### filters

Each filter must include:

```json
{
  "column": "movies.year",
  "operator": "=",
  "value": 2008,
  "reason": "The question asks for movies released in 2008."
}
```

---

### aggregation

Use `null` if there is no aggregation.

Examples:

```json
{"function": "COUNT", "column": "*"}
{"function": "AVG", "column": "ratings.rating"}
```

---

### distinct

Boolean.

Use `true` when many-to-many joins can produce duplicate requested rows.

Common true cases:

```text
actors_in_movies_by_year_order_birth
directors_of_high_rated_movies
costars_of_actor
```

---

### ordering

Use an empty list if no ordering is requested.

Example:

```json
[
  {"column": "movies.title", "direction": "ASC", "reason": "Alphabetical order requested."}
]
```

---

### limit

Integer or null.

---

### exclusions

Use for rules like excluding the target actor from co-star results.

Example:

```json
[
  {
    "condition": "other_people.id != target_person.id",
    "reason": "The target actor should not be returned as their own co-star."
  }
]
```

---

### requires_self_join

Boolean.

Use `true` for:

```text
movies_with_two_actors
costars_of_actor
```

---

## 4. PLAN VALIDATION RULES

A valid plan must satisfy:

1. `is_related` must be boolean.
2. `database` must equal `movies.db`.
3. `sql_dialect` must equal `sqlite`.
4. Every selected table must be one of:
   - `movies`
   - `people`
   - `stars`
   - `directors`
   - `ratings`
5. Every selected column must exist in the selected table.
6. Every join must use documented PK/FK logic.
7. Actor questions must use `stars`, not `directors`.
8. Director questions must use `directors`, not `stars`.
9. Rating questions must use `ratings`.
10. Co-star and two-actor questions must use aliases/self-join logic.
11. SQL generation must be read-only.
12. If `is_related = false`, tables, columns, joins, filters, and SQL should be empty/null.
