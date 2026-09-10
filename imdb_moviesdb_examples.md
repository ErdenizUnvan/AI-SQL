# IMDb movies.db Example Questions and Expected Query Plans
Version: 1.0

---

## 1. List the titles of all movies released in 2008

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "movies_by_exact_year",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": null, "person_name_2": null, "year": 2008, "rating": null, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "movies", "alias": null, "purpose": "Return movie titles and filter by release year."}],
  "columns": {"select": ["movies.title"], "filter": ["movies.year"], "join": [], "order_by": [], "aggregation": []},
  "joins": [],
  "filters": [{"column": "movies.year", "operator": "=", "value": 2008, "reason": "The question asks for movies released in 2008."}],
  "aggregation": null,
  "distinct": false,
  "ordering": [],
  "limit": null,
  "exclusions": [],
  "expected_output": "Movie titles.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "The question only requires the movies table because release year and title are both stored there."
}
```

---

## 2. Determine the birth year of Emma Stone

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "person_birth_year",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": "Emma Stone", "person_name_2": null, "year": null, "rating": null, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "people", "alias": null, "purpose": "Find the person and return their birth year."}],
  "columns": {"select": ["people.birth"], "filter": ["people.name"], "join": [], "order_by": [], "aggregation": []},
  "joins": [],
  "filters": [{"column": "people.name", "operator": "=", "value": "Emma Stone", "reason": "The question asks for Emma Stone's birth year."}],
  "aggregation": null,
  "distinct": false,
  "ordering": [],
  "limit": null,
  "exclusions": [],
  "expected_output": "Birth year.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "Birth year is stored in the people table."
}
```

---

## 3. List the titles of all movies with a release date on or after 2018, in alphabetical order

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "movies_after_year_alphabetical",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": null, "person_name_2": null, "year": 2018, "rating": null, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "movies", "alias": null, "purpose": "Filter movies by release year and sort titles alphabetically."}],
  "columns": {"select": ["movies.title"], "filter": ["movies.year"], "join": [], "order_by": ["movies.title"], "aggregation": []},
  "joins": [],
  "filters": [{"column": "movies.year", "operator": ">=", "value": 2018, "reason": "The question asks for movies released on or after 2018."}],
  "aggregation": null,
  "distinct": false,
  "ordering": [{"column": "movies.title", "direction": "ASC", "reason": "The question asks for alphabetical order."}],
  "limit": null,
  "exclusions": [],
  "expected_output": "Movie titles.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "Title and release year are both in the movies table."
}
```

---

## 4. Determine the number of movies with an IMDb rating of 10.0

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "count_movies_by_exact_rating",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": null, "person_name_2": null, "year": null, "rating": 10.0, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "ratings", "alias": null, "purpose": "Count movies with the target IMDb rating."}],
  "columns": {"select": [], "filter": ["ratings.rating"], "join": [], "order_by": [], "aggregation": ["COUNT(*)"]},
  "joins": [],
  "filters": [{"column": "ratings.rating", "operator": "=", "value": 10.0, "reason": "The question asks for movies with rating 10.0."}],
  "aggregation": {"function": "COUNT", "column": "*"},
  "distinct": false,
  "ordering": [],
  "limit": null,
  "exclusions": [],
  "expected_output": "Count of movies.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "The count can be computed directly from the ratings table."
}
```

---

## 5. List the titles and release years of all Harry Potter movies, in chronological order

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "franchise_movies_chronological",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": null, "person_name_2": null, "year": null, "rating": null, "franchise_keyword": "Harry Potter", "limit": null},
  "tables": [{"name": "movies", "alias": null, "purpose": "Find franchise movies by title pattern and sort chronologically."}],
  "columns": {"select": ["movies.title", "movies.year"], "filter": ["movies.title"], "join": [], "order_by": ["movies.year"], "aggregation": []},
  "joins": [],
  "filters": [{"column": "movies.title", "operator": "LIKE", "value": "%Harry Potter%", "reason": "The question asks for Harry Potter movies."}],
  "aggregation": null,
  "distinct": false,
  "ordering": [{"column": "movies.year", "direction": "ASC", "reason": "Chronological order means release year ascending."}],
  "limit": null,
  "exclusions": [],
  "expected_output": "Movie titles and release years.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "Franchise matching and release year are both handled in the movies table."
}
```

---

## 6. Determine the average rating of all movies released in 2012

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "average_rating_by_year",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": null, "person_name_2": null, "year": 2012, "rating": null, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "movies", "alias": null, "purpose": "Filter movies by release year."}, {"name": "ratings", "alias": null, "purpose": "Compute average IMDb rating."}],
  "columns": {"select": [], "filter": ["movies.year"], "join": ["movies.id", "ratings.movie_id"], "order_by": [], "aggregation": ["ratings.rating"]},
  "joins": [{"left": "movies.id", "right": "ratings.movie_id", "type": "INNER", "reason": "Attach ratings to movies released in 2012."}],
  "filters": [{"column": "movies.year", "operator": "=", "value": 2012, "reason": "The question asks for movies released in 2012."}],
  "aggregation": {"function": "AVG", "column": "ratings.rating"},
  "distinct": false,
  "ordering": [],
  "limit": null,
  "exclusions": [],
  "expected_output": "Average IMDb rating.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "Release year is in movies and rating is in ratings, so a join is required."
}
```

---

## 7. List all movies released in 2010 and their ratings, in descending order by rating

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "movies_and_ratings_by_year_desc",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": null, "person_name_2": null, "year": 2010, "rating": null, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "movies", "alias": null, "purpose": "Filter and return movie titles."}, {"name": "ratings", "alias": null, "purpose": "Return and sort by rating."}],
  "columns": {"select": ["movies.title", "ratings.rating"], "filter": ["movies.year"], "join": ["movies.id", "ratings.movie_id"], "order_by": ["ratings.rating"], "aggregation": []},
  "joins": [{"left": "movies.id", "right": "ratings.movie_id", "type": "INNER", "reason": "Attach ratings to movies."}],
  "filters": [{"column": "movies.year", "operator": "=", "value": 2010, "reason": "The question asks for movies released in 2010."}],
  "aggregation": null,
  "distinct": false,
  "ordering": [{"column": "ratings.rating", "direction": "DESC", "reason": "The question requests descending order by rating."}],
  "limit": null,
  "exclusions": [],
  "expected_output": "Movie titles and ratings.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "This requires movies for year/title and ratings for rating values."
}
```

---

## 8. List the names of all people who starred in Toy Story

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "actors_in_movie",
  "confidence": "high",
  "target_entities": {"movie_title": "Toy Story", "person_name": null, "person_name_2": null, "year": null, "rating": null, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "movies", "alias": null, "purpose": "Filter the target movie title."}, {"name": "stars", "alias": null, "purpose": "Connect the movie to cast members."}, {"name": "people", "alias": null, "purpose": "Return actor names."}],
  "columns": {"select": ["people.name"], "filter": ["movies.title"], "join": ["movies.id", "stars.movie_id", "stars.person_id", "people.id"], "order_by": [], "aggregation": []},
  "joins": [{"left": "movies.id", "right": "stars.movie_id", "type": "INNER", "reason": "Find starring records for Toy Story."}, {"left": "stars.person_id", "right": "people.id", "type": "INNER", "reason": "Convert starring person IDs into names."}],
  "filters": [{"column": "movies.title", "operator": "=", "value": "Toy Story", "reason": "The question asks for people who starred in Toy Story."}],
  "aggregation": null,
  "distinct": false,
  "ordering": [],
  "limit": null,
  "exclusions": [],
  "expected_output": "Actor names.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "Actors are represented through the stars relationship table."
}
```

---

## 9. List the names of all people who starred in a movie released in 2004, ordered by birth year

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "actors_in_movies_by_year_order_birth",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": null, "person_name_2": null, "year": 2004, "rating": null, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "movies", "alias": null, "purpose": "Filter movies by release year."}, {"name": "stars", "alias": null, "purpose": "Find people who starred in those movies."}, {"name": "people", "alias": null, "purpose": "Return names and order by birth year."}],
  "columns": {"select": ["people.name"], "filter": ["movies.year"], "join": ["movies.id", "stars.movie_id", "stars.person_id", "people.id"], "order_by": ["people.birth"], "aggregation": []},
  "joins": [{"left": "movies.id", "right": "stars.movie_id", "type": "INNER", "reason": "Find starring records for movies released in 2004."}, {"left": "stars.person_id", "right": "people.id", "type": "INNER", "reason": "Convert actor IDs to names and birth years."}],
  "filters": [{"column": "movies.year", "operator": "=", "value": 2004, "reason": "The question asks for movies released in 2004."}],
  "aggregation": null,
  "distinct": true,
  "ordering": [{"column": "people.birth", "direction": "ASC", "reason": "The question asks for ordering by birth year."}],
  "limit": null,
  "exclusions": [],
  "expected_output": "Distinct actor names ordered by birth year.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "The stars relationship connects people to movies, and birth year is stored in people."
}
```

---

## 10. List the names of all people who have directed a movie that received a rating of at least 9.0

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "directors_of_high_rated_movies",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": null, "person_name_2": null, "year": null, "rating": 9.0, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "people", "alias": null, "purpose": "Return director names."}, {"name": "directors", "alias": null, "purpose": "Connect people to movies they directed."}, {"name": "movies", "alias": null, "purpose": "Bridge director records to ratings."}, {"name": "ratings", "alias": null, "purpose": "Filter by rating threshold."}],
  "columns": {"select": ["people.name"], "filter": ["ratings.rating"], "join": ["people.id", "directors.person_id", "directors.movie_id", "movies.id", "ratings.movie_id"], "order_by": [], "aggregation": []},
  "joins": [{"left": "people.id", "right": "directors.person_id", "type": "INNER", "reason": "Find movies directed by each person."}, {"left": "directors.movie_id", "right": "movies.id", "type": "INNER", "reason": "Connect director records to movies."}, {"left": "movies.id", "right": "ratings.movie_id", "type": "INNER", "reason": "Attach rating data to directed movies."}],
  "filters": [{"column": "ratings.rating", "operator": ">=", "value": 9.0, "reason": "The question asks for movies with rating at least 9.0."}],
  "aggregation": null,
  "distinct": true,
  "ordering": [],
  "limit": null,
  "exclusions": [],
  "expected_output": "Distinct director names.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "This requires director relationships and rating threshold filtering."
}
```

---

## 11. List the titles of the five highest rated movies that Chadwick Boseman starred in, starting with the highest rated

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "highest_rated_movies_by_actor",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": "Chadwick Boseman", "person_name_2": null, "year": null, "rating": null, "franchise_keyword": null, "limit": 5},
  "tables": [{"name": "people", "alias": null, "purpose": "Filter the actor by name."}, {"name": "stars", "alias": null, "purpose": "Find movies starring the actor."}, {"name": "movies", "alias": null, "purpose": "Return movie titles."}, {"name": "ratings", "alias": null, "purpose": "Sort by IMDb rating."}],
  "columns": {"select": ["movies.title"], "filter": ["people.name"], "join": ["people.id", "stars.person_id", "stars.movie_id", "movies.id", "ratings.movie_id"], "order_by": ["ratings.rating"], "aggregation": []},
  "joins": [{"left": "people.id", "right": "stars.person_id", "type": "INNER", "reason": "Find starring records for Chadwick Boseman."}, {"left": "stars.movie_id", "right": "movies.id", "type": "INNER", "reason": "Return movie titles."}, {"left": "movies.id", "right": "ratings.movie_id", "type": "INNER", "reason": "Attach ratings for sorting."}],
  "filters": [{"column": "people.name", "operator": "=", "value": "Chadwick Boseman", "reason": "The question asks for movies he starred in."}],
  "aggregation": null,
  "distinct": false,
  "ordering": [{"column": "ratings.rating", "direction": "DESC", "reason": "Highest rated movies should appear first."}],
  "limit": 5,
  "exclusions": [],
  "expected_output": "Five movie titles.",
  "requires_self_join": false,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "Actor-to-movie relationship comes from stars, and ranking comes from ratings."
}
```

---

## 12. List the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "movies_with_two_actors",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": "Bradley Cooper", "person_name_2": "Jennifer Lawrence", "year": null, "rating": null, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "movies", "alias": null, "purpose": "Return movies shared by both actors."}, {"name": "stars", "alias": "s1", "purpose": "Starring records for the first actor."}, {"name": "people", "alias": "p1", "purpose": "Filter first actor name."}, {"name": "stars", "alias": "s2", "purpose": "Starring records for the second actor."}, {"name": "people", "alias": "p2", "purpose": "Filter second actor name."}],
  "columns": {"select": ["movies.title"], "filter": ["p1.name", "p2.name"], "join": ["movies.id", "s1.movie_id", "s2.movie_id", "s1.person_id", "p1.id", "s2.person_id", "p2.id"], "order_by": [], "aggregation": []},
  "joins": [{"left": "movies.id", "right": "s1.movie_id", "type": "INNER", "reason": "Connect movies to first actor starring records."}, {"left": "movies.id", "right": "s2.movie_id", "type": "INNER", "reason": "Connect the same movies to second actor starring records."}, {"left": "s1.person_id", "right": "p1.id", "type": "INNER", "reason": "Filter first actor."}, {"left": "s2.person_id", "right": "p2.id", "type": "INNER", "reason": "Filter second actor."}],
  "filters": [{"column": "p1.name", "operator": "=", "value": "Bradley Cooper", "reason": "First actor."}, {"column": "p2.name", "operator": "=", "value": "Jennifer Lawrence", "reason": "Second actor."}],
  "aggregation": null,
  "distinct": false,
  "ordering": [],
  "limit": null,
  "exclusions": [],
  "expected_output": "Movie titles where both actors starred.",
  "requires_self_join": true,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "The same movie must have starring records for both actors, so stars and people need aliases."
}
```

---

## 13. List the names of all people who starred in a movie in which Kevin Bacon also starred

```json
{
  "is_related": true,
  "database": "movies.db",
  "sql_dialect": "sqlite",
  "question_type": "costars_of_actor",
  "confidence": "high",
  "target_entities": {"movie_title": null, "person_name": "Kevin Bacon", "person_name_2": null, "year": null, "rating": null, "franchise_keyword": null, "limit": null},
  "tables": [{"name": "people", "alias": "target_person", "purpose": "Identify Kevin Bacon."}, {"name": "stars", "alias": "target_stars", "purpose": "Find movies starring Kevin Bacon."}, {"name": "stars", "alias": "other_stars", "purpose": "Find other people in the same movies."}, {"name": "people", "alias": "other_people", "purpose": "Return co-star names."}],
  "columns": {"select": ["other_people.name"], "filter": ["target_person.name"], "join": ["target_person.id", "target_stars.person_id", "target_stars.movie_id", "other_stars.movie_id", "other_stars.person_id", "other_people.id"], "order_by": [], "aggregation": []},
  "joins": [{"left": "target_person.id", "right": "target_stars.person_id", "type": "INNER", "reason": "Find movies starring Kevin Bacon."}, {"left": "target_stars.movie_id", "right": "other_stars.movie_id", "type": "INNER", "reason": "Find other starring records in the same movies."}, {"left": "other_stars.person_id", "right": "other_people.id", "type": "INNER", "reason": "Return names of the other people."}],
  "filters": [{"column": "target_person.name", "operator": "=", "value": "Kevin Bacon", "reason": "The question asks for people who starred with Kevin Bacon."}],
  "aggregation": null,
  "distinct": true,
  "ordering": [],
  "limit": null,
  "exclusions": [{"condition": "other_people.id != target_person.id", "reason": "Kevin Bacon should not be returned as his own co-star."}],
  "expected_output": "Distinct names of Kevin Bacon co-stars.",
  "requires_self_join": true,
  "safety": {"read_only": true, "allowed_statement": "SELECT", "forbidden_operations": ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]},
  "reason": "This requires finding movies starring Kevin Bacon and then other people who starred in those same movies."
}
```
