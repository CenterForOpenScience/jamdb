# Limitations

Due to some of the underlying technologies, limits exist on the amount and types of data that may be stored.

## Imposed by JamDB
* Namespace, collection, and document IDs may not excede 64 characters


## [Elasticsearch](https://www.elastic.co/products/elasticsearch)
* String values may not exceed 32766 [bytes](https://en.wikipedia.org/wiki/Byte)
* The string values `Infinity` and `-Infinity` may not be used where other documents would have a numeric value

## [MongoDB](https://mongodb.org)
* [Integer values may not exceed 8 bytes](http://bsonspec.org/spec.html)
* [Floating point values may not exceed 8 bytes](http://bsonspec.org/spec.html)
* [Object keys may not start with `$`s](https://docs.mongodb.org/manual/reference/limits/#Restriction-on-Collection-Names)
* [Object keys may not contain `.`s](https://docs.mongodb.org/manual/reference/limits/#Restriction-on-Collection-Names)
* [Documents may not exceed 16 megabytes](https://docs.mongodb.org/manual/reference/limits/#BSON-Document-Size)
* [Documents may not exceed 100 levels of nesting](https://docs.mongodb.org/manual/reference/limits/#Nested-Depth-for-BSON-Documents)
