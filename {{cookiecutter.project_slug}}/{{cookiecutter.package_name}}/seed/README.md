Seeding Elasticsearch Indexes
=============================

This project's command-line interface (CLI) defines a subcommand called
`seed` that you can use to initialize the
[Elasticsearch](https://www.elastic.co/products/elasticsearch) indexes.

``` {.sourceCode .bash}
$ txauthor seed --help

Usage: txauthor seed [OPTIONS]

  Populate an Elasticsearch database with application seed data.

Options:
  --es-host TEXT   Identify Elasticsearch hosts.
  -r, --root PATH  Provide the path to the seed data root directory.
  -f, --force      Replace indices with seed data.
  --help           Show this message and exit.
```

Directory Structure
-------------------

The library contains a standard seed data set, but you can also use the
--root option to specify a different seed data set. If you do this,
you'll want to have some understanding of the seed data structure.

The seed data directory structure in the project is shown below.

``` {.sourceCode .bash}
$ tree seed

seed
|-- README.md
`-- indexes
    |-- cats
    |   `-- cat
    |       `-- ff1c371c-99e4-4e7f-94ff-f543c6157219
    `-- dogs
        `-- dog
            `-- 4a5649c5-aad6-429f-abf1-75fe9d3efa59
            `-- 62abf86e-2f6e-4d59-99c6-9d42b1e99fa0

```

### The Base Directory (*"seed"*)

This is the base directory that contains all the seed data. If you're
creating your own seed data set you may provide another name.

### Indexes

All of the [Elasticsearch
indexes](https://www.elastic.co/blog/what-is-an-elasticsearch-index) are
defined in a subdirectory called 'indexes'. An Elasticsearch index will
be created for each subdirectory and the name of the subdirectory will
be the name of the index.

The current indexes are:

* **languages** popular programming languages

### Document Types

Within each index directory there are
directories that define [document
types](https://www.elastic.co/guide/en/elasticsearch/guide/current/mapping.html).
The name of the subdirectory will be the name of the document type.

### Documents

Within each document type directory
are individual files that represent the individual documents that will
be indexed. The name of the file will be the
[id](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-id-field.html)
of the document.

### Special Fields

Each seed data document should specify an owner\_ field and a group\_
field. In both cases the value should be a string representation of a
[UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier).
These are not part of the actual document but are used by the API to
track stored documents.

``` {.sourceCode .python}
{
  "language": "python"
}

```

### "Blobbing"

In order to minimize database overhead, the API stores non-searchable
document content in binary form in a field called blob so once a
document has been indexed, if you inspect it within the index (for
example, using [Kibana](https://www.elastic.co/products/kibana)) you may
notice that the only visible fields are the
special fields &lt;seed\_data\_special\_fields&gt;.
