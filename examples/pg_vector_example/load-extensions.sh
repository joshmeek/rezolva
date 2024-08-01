#!/bin/sh

# You could probably do this fancier and have an array of extensions
# to create, but this is mostly an illustration of what can be done

cd /tmp
git clone --branch v0.4.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
make install # may need sudo

psql -v ON_ERROR_STOP=1 --d "$POSTGRES_DB"  -U "$POSTGRES_USER" <<EOF
CREATE EXTENSION vector;
SELECT * FROM pg_extension;
EOF