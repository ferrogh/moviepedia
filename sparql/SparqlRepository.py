from sparql.SparqlQueryEngine import SparqlQueryEngine


class SparqlRepository:
    def __init__(self):
        self.sparql = SparqlQueryEngine()

    # Retrieve all semantic triples from knowledge base
    def get_all_triples(self, limit=1000):
        query = """
            PREFIX fss: <http://www.semanticweb.org/raneeshgomez/ontologies/2020/fyp-solar-system#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT *
            WHERE {
              ?subject ?predicate ?object .
            }
            LIMIT %s
        """
        query = query % limit
        return self.sparql.query_dbpedia(query)

    # Retrieve semantic triples based on query
    def get_triples(self, inputs, limit=10):
        filters = self.filter_builder(inputs)
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dbp: <http://dbpedia.org/property/>

            SELECT ?title (group_concat(distinct ?cast;separator=", ") as ?casts) (group_concat(distinct ?director;separator=", ") as ?directors) (group_concat(distinct ?writer;separator=", ") as ?writers) ?description ?genre ?rating ?releaseDate ?company ?runtime
            WHERE {{
                ?movie rdf:type dbo:movie ;
                rdfs:label ?title ;
                dbo:starring [rdfs:label ?cast] ;
                dbo:director [rdfs:label ?director] ;
                dbo:writer [rdfs:label ?writer] ;
                dbo:description ?description ;
                dbo:genre ?genre ;
                dbp:rating ?rating ;
                dbo:releaseDate ?releaseDate ;
                dbo:company [rdfs:label ?company] ;
                dbo:Work\/runtime ?runtime .
                filter( !(regex(lcase(?cast), "not available")) && !(regex(lcase(?director), "not available")) && !(regex(lcase(?writer), "not available")) {})
            }}
            group by ?title ?description ?genre ?rating ?releaseDate ?company ?runtime
            LIMIT {}
        """.format(filters,limit)
        # return query
        return self.sparql.query_fuseki(query)
    
    # Create filter for SPARQL query
    def filter_builder(self, query):
        filters = ""
        for key,value in query.items():
            if value != None:
                value = value.lower()
                filters += " && "

                if key == 'title':
                    filters += '(regex(lcase(?title), "{}" ))'.format(value)
                elif key == 'cast':
                    filters += '(regex(lcase(?cast), "{}" ))'.format(value)
                elif key == 'director':
                    filters += '(regex(lcase(?director), "{}" ))'.format(value)
                elif key == 'writer':
                    filters += '(regex(lcase(?writer), "{}" ))'.format(value)
                elif key == 'genre':
                    filters += '(regex(lcase(?genre), "{}" ))'.format(value)
                elif key == 'rating':
                    filters += '(regex(lcase(?rating), "{}" ))'.format(value)
                elif key == 'company':
                    filters += '(regex(lcase(?company), "{}" ))'.format(value)

        return filters
