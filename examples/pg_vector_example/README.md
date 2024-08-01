# pg_vector_example

Integrates the `examples/vector_based_example.py` with a Postgres DB running pg_vector via Docker.

## start up

0. `cd examples/pg_vector_example`
1. `touch .env`
2. `echo POSTGRES_PASSWORD={your password} >> .env`
3. `docker-compose build`
4. `docker-compose up`
5. install from requirements.txt
6. `examples/pg_vector_example/main.py`

optionally, interact with the db directly via: `psql -h 0.0.0.0 -d vectordb -U vectoruser`
