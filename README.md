This is a fork of https://github.com/KBNLresearch/topics/,

with an added category, music.


# Topics

Number of multi-class classifiers for news articles (topic) and DBpedia descriptions (topic and type). For further info and training source code see Jupyter notebooks for [topic](https://github.com/KBNLresearch/topics/blob/master/topics.ipynb) and [type](https://github.com/KBNLresearch/topics/blob/master/type.ipynb).

## Web interface

A Bottle web application can be started with `./topics.py` accepting requests with a newspaper article or DBpedia url as parameter, e.g. `http://kbresearch.nl/topics_music/?url=http://nl.dbpedia.org/resource/Albert_Einstein`. The application will work out the type of resource and language for itself and return all available classifier results.
