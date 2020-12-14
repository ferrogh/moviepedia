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
