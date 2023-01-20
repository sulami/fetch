# fetch.py

## Docker Setup

Build the image:

```sh
docker build . -t fetch
```

Then run it with:

```sh
docker run -it fetch
poetry shell
./fetch.py -h
```

## Usage

```sh
./fetch.py --metadata 'https://autify.com' 'https://blog.sulami.xyz' 'https://blog.sulami.xyz/raw/pubkey.txt'
```

Downloads are performed in parallel.

Non-HTML files can also be downloaded, including binary formats such
as images or PDFs.

## Tests

```sh
# Inside the poetry shell:
pytest tests.py
```

## Future Work

There is not a lot of handling for bad user input (e.g. invalid URLs)
or more obscure errors (e.g. broken pipes) due to the time
constraints.

It would be nice to have test coverage for at least the metadata
output, and ideally also the fetching, but again, time constraints.

Recursive fetching for full page archiving was attempted, but the
various ways references can be included in HTML make this more complex
than one would initially assume, at least in a robust manner.
