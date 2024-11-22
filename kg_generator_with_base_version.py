import os
from neo4j import GraphDatabase
driver = GraphDatabase.driver(
    uri="bolt://localhost:7687", auth=("neo4j", "biomedical_kg"))
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

    q1 = """LOAD CSV WITH HEADERS FROM 'file:///string_interacts-with_relationship_base.tsv' as row FIELDTERMINATOR '\t'
    WITH row
    WHERE row.combined_score is NOT NULL
    MERGE (k:protein {Name: row.Protein1})
    MERGE (j:protein {Name: row.Protein2})
    MERGE (k) -[:interacts_with {combined_score:row.combined_score, neighborhood:row.neighborhood, fusion:row.fusion, cooccurence:row.cooccurence, coexpression:row.coexpression, database:row.database, textmining:row.textmining}] -> (j)"""

    results = session.run(q1)
    data = results.data()

    print("Added STRING")


def str_prop():
    q2 = """LOAD CSV WITH HEADERS FROM 'file:///string_protein_node_base.tsv' as csvLine FIELDTERMINATOR '\t'
    MATCH (k {Name: csvLine.Ensembl_ID})
    SET k.Preferred_name = csvLine.Preferred_name, k.Ensembl_HGNC = csvLine.Ensembl_HGNC, k.Ensembl_gene = csvLine.Ensembl_gene, k.Ensembl_UniProt_AC = csvLine.Ensembl_UniProt_AC"""

    results = session.run(q2)
    data = results.data()

    print("Added STRING properties")


def geo_down_rel():
    q3 = """LOAD CSV WITH HEADERS FROM 'file:///geo_downregulates_relationship_base.tsv' as row FIELDTERMINATOR '\t'
    MERGE (x:disease {Name: row.Disease})
    MERGE (y:gene {Name: row.Gene})
    MERGE (x) -[:downregulates {metap:row.metap, metafc:row.metafc}] -> (y)
    """

    results = session.run(q3)
    data = results.data()

    print("Added GEO Downregulation relationships")


def geo_up_rel():
    q4 = """LOAD CSV WITH HEADERS FROM 'file:///geo_upregulates_relationship_base.tsv' as row FIELDTERMINATOR '\t'
    MERGE (x:disease {Name: row.Disease})
    MERGE (z:gene {Name: row.Gene})
    MERGE (x) -[:upregulates {metap:row.metap, metafc:row.metafc}] -> (z)
    """

    results = session.run(q4)
    data = results.data()

    print("Added GEO Upregulation relationships")


def lincs_up_rel():
    q5 = """LOAD CSV WITH HEADERS FROM 'file:///lincs_upregulates_relationship_base.tsv' as row FIELDTERMINATOR '\t'
    MERGE (x:drug {Name: row.drug})
    MERGE (y:gene {Name: row.gene})
    MERGE (x) -[:upregulates {zvalue:row.zvalue, pvalue:row.pvalue}] -> (y)
    """

    results = session.run(q5)
    data = results.data()

    print("Added Lincs Upregulation relationships")


def lincs_down_rel():
    q6 = """LOAD CSV WITH HEADERS FROM 'file:///lincs_downregulates_relationship_base.tsv' as row FIELDTERMINATOR '\t'
    MERGE (x:drug {Name: row.drug})
    MERGE (y:gene {Name: row.gene})
    MERGE (x) -[:downregulates {zvalue:row.zvalue, pvalue:row.pvalue}] -> (y)
    """

    results = session.run(q6)
    data = results.data()

    print("Added Lincs Downregulation relationships")


def disgenet_association_relationships():
    q7 = """LOAD CSV WITH HEADERS FROM 'file:///disgenet_association_relationship_base.tsv' as row FIELDTERMINATOR '\t'
    MERGE (x:disease {Name: row.disease})
    MERGE (y:gene {Name: row.gene})
    MERGE (x) -[:associated_with {score:row.score, ei:row.EI, year_initial:row.year_initial, year_final:row.year_final}] -> (y)"""

    results = session.run(q7)
    data = results.data()

    print("Added Disgenet Relationships")


def disgenet_disease_prop():
    q8 = """LOAD CSV WITH HEADERS FROM 'file:///disgenet_disease_node_base.tsv' as csvLine FIELDTERMINATOR '\t'
    MATCH (k {Name: csvLine.disease})
    SET k.diseaseID = csvLine.diseaseID, k.disease_class = csvLine.disease_class, k.disease_class_name = csvLine.disease_class_name, k.disease_semantic_type = csvLine.disease_semantic_type"""

    results = session.run(q8)
    data = results.data()

    print("Added Disgenet Disease properties")


def disgenet_gene_prop():
    q9 = """LOAD CSV WITH HEADERS FROM 'file:///disgenet_gene_node_base.tsv' as csvLine FIELDTERMINATOR '\t'
    MATCH (k {Name: csvLine.gene})
    SET k.geneID = csvLine.geneID, k.Protein_Class = csvLine.Protein_Class, k.UniProtID = csvLine.UniProtID, k.DPI = csvLine.DPI, k.DSI = csvLine.DSI"""

    results = session.run(q9)
    data = results.data()

    print("Added Disgenet Gene properties")


def heterogeneous_graph():
    q10 = """MATCH (a:gene),(b:protein)
        WHERE a.Name = b.Preferred_name
        CREATE (a)-[r:product]->(b)"""

    results = session.run(q10)
    data = results.data()

    print("Heterogenous graph")


# Call all functions
str_rel()
str_prop()
geo_down_rel()
geo_up_rel()
lincs_up_rel()
lincs_down_rel()
disgenet_association_relationships()
disgenet_disease_prop()
disgenet_gene_prop()
heterogeneous_graph()
