import os
from neo4j import GraphDatabase
driver = GraphDatabase.driver(
    uri="bolt://localhost:7687", auth=("neo4j", "string_db"))
session = driver.session()

q00 = """Call dbms.listConfig() YIELD name, value
    WHERE name='dbms.directories.import'
    RETURN value"""
results = session.run(q00)
dest = results.data()[0]['value']
print(dest)


def del_dir(dest=dest):
    print(dest)
    os.system(f"rm -R '{dest}'")


def copy(src, dest=dest):
    # if folder doesn't exist, create it
    if not os.path.exists(dest):
        os.makedirs(dest)
    os.system(f"cp '{src}' '{dest}'")


def del_kg():
    q0 = """MATCH(n)
    DETACH DELETE n"""

    results = session.run(q0)
    data = results.data()

    print("KG Cleared")


def str_rel():
    # Load csv without null values in cypher

    q1 = """LOAD CSV WITH HEADERS FROM 'file:///string_interacts-with_relationship.tsv' as row FIELDTERMINATOR '\t'
    WITH row
    WHERE row.combined_score is NOT NULL
    MERGE (k:protein1 {Name: row.Protein1})
    MERGE (j:protein2 {Name: row.Protein2})
    MERGE (k) -[:interacts_with {combined_score:row.combined_score, neighborhood:row.neighborhood, fusion:row.fusion, cooccurence:row.cooccurence, coexpression:row.coexpression, database:row.database, textmining:row.textmining}] -> (j)"""

    results = session.run(q1)
    data = results.data()

    print("Added STRING")


def str_prop():
    q2 = """LOAD CSV WITH HEADERS FROM 'file:///string_protein_node.tsv' as csvLine FIELDTERMINATOR '\t'
    MATCH (k {Name: csvLine.Ensembl_ID})
    SET k.Preferred_name = csvLine.Preferred_name, k.Ensembl_HGNC = csvLine.Ensembl_HGNC, k.Ensembl_gene = csvLine.Ensembl_gene, k.Ensembl_UniProt_AC = csvLine.Ensembl_UniProt_AC"""

    results = session.run(q2)
    data = results.data()

    print("Added STRING properties")


def geo_down_rel():
    q3 = """LOAD CSV WITH HEADERS FROM 'file:///geo_downregulates_relationship.tsv' as row FIELDTERMINATOR '\t'
    MERGE (x:disease {Name: row.Disease})
    MERGE (y:gene {Name: row.Gene})
    MERGE (x) -[:downregulates {metap:row.metap, metafc:row.metafc}] -> (y)
    """

    results = session.run(q3)
    data = results.data()

    print("Added GEO Downregulation relationships")


def geo_up_rel():
    q4 = """LOAD CSV WITH HEADERS FROM 'file:///geo_upregulates_relationship.tsv' as row FIELDTERMINATOR '\t'
    MERGE (x:disease {Name: row.Disease})
    MERGE (z:gene {Name: row.Gene})
    MERGE (x) -[:upregulates {metap:row.metap, metafc:row.metafc}] -> (z)
    """

    results = session.run(q4)
    data = results.data()

    print("Added GEO Upregulation relationships")


def str_geo():
    q5 = """MATCH (a:gene),(b:protein1)
    WHERE a.Name = b.Preferred_name
    CREATE (a)-[r:product]->(b)
    RETURN a,b"""

    results = session.run(q5)
    data = results.data()

    print("STRING-GEO relationships added")
