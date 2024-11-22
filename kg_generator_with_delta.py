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


def del_file(filepath, dest=dest):
    try:
        os.remove(dest + "/" + os.path.basename(filepath))
        os.remove(filepath)
    except:
        pass


def copy(src, dest=dest):
    # if folder doesn't exist, create it
    try:
        if not os.path.exists(dest):
            os.makedirs(dest)
        os.system(f"cp '{src}' '{dest}'")
    except:
        print("Version not copied for ", src)


def del_kg():
    q0 = """MATCH(n)
    DETACH DELETE n"""

    results = session.run(q0)
    data = results.data()

    print("KG Cleared")


def string_rel():
    # Load csv without null values in cypher

    try:
        q1 = """LOAD CSV WITH HEADERS FROM 'file:///string_interacts-with_relationship.tsv' as row FIELDTERMINATOR '\t'
        WITH row
        WHERE row.combined_score is NOT NULL
        MERGE (k:protein {Name: row.Protein1})
        MERGE (j:protein {Name: row.Protein2})
        MERGE (k) -[:interacts_with {combined_score:row.combined_score, neighborhood:row.neighborhood, fusion:row.fusion, cooccurence:row.cooccurence, coexpression:row.coexpression, database:row.database, textmining:row.textmining}] -> (j)"""

        results = session.run(q1)
        data = results.data()

        print("Added STRING")
    except:
        print("STRING already added")


def string_prop():
    try:
        q2 = """LOAD CSV WITH HEADERS FROM 'file:///string_protein_node.tsv' as csvLine FIELDTERMINATOR '\t'
        MATCH (k {Name: csvLine.Ensembl_ID})
        SET k.Preferred_name = csvLine.Preferred_name, k.Ensembl_HGNC = csvLine.Ensembl_HGNC, k.Ensembl_gene = csvLine.Ensembl_gene, k.Ensembl_UniProt_AC = csvLine.Ensembl_UniProt_AC"""

        results = session.run(q2)
        data = results.data()

        print("Added STRING properties")
    except:
        print("STRING properties already added")


def geo_down_rel():
    try:
        q3 = """LOAD CSV WITH HEADERS FROM 'file:///geo_downregulates_relationship.tsv' as row FIELDTERMINATOR '\t'
        MERGE (x:disease {Name: row.Disease})
        MERGE (y:gene {Name: row.Gene})
        MERGE (x) -[:downregulates {metap:row.metap, metafc:row.metafc}] -> (y)
        """

        results = session.run(q3)
        data = results.data()

        print("Added GEO Downregulation relationships")
    except:
        print("GEO Downregulation relationships already added")


def geo_up_rel():
    try:
        q4 = """LOAD CSV WITH HEADERS FROM 'file:///geo_upregulates_relationship.tsv' as row FIELDTERMINATOR '\t'
        MERGE (x:disease {Name: row.Disease})
        MERGE (z:gene {Name: row.Gene})
        MERGE (x) -[:upregulates {metap:row.metap, metafc:row.metafc}] -> (z)
        """

        results = session.run(q4)
        data = results.data()

        print("Added GEO Upregulation relationships")
    except:
        print("GEO Upregulation relationships already added")


def lincs_up_rel():
    try:
        q5 = """LOAD CSV WITH HEADERS FROM 'file:///lincs_upregulates_relationship.tsv' as row FIELDTERMINATOR '\t'
        MERGE (x:drug {Name: row.drug})
        MERGE (y:gene {Name: row.gene})
        MERGE (x) -[:upregulates {zvalue:row.zvalue, pvalue:row.pvalue}] -> (y)
        """

        results = session.run(q5)
        data = results.data()

        print("Added Lincs Upregulation relationships")
    except:
        print("Lincs Upregulation relationships already added")


def lincs_down_rel():
    try:
        q6 = """LOAD CSV WITH HEADERS FROM 'file:///lincs_downregulates_relationship.tsv' as row FIELDTERMINATOR '\t'
        MERGE (x:drug {Name: row.drug})
        MERGE (y:gene {Name: row.gene})
        MERGE (x) -[:downregulates {zvalue:row.zvalue, pvalue:row.pvalue}] -> (y)
        """

        results = session.run(q6)
        data = results.data()

        print("Added Lincs Downregulation relationships")
    except:
        print("Lincs Downregulation relationships already added")


def disgenet_association_relationships():
    try:
        q7 = """LOAD CSV WITH HEADERS FROM 'file:///disgenet_association_relationship.tsv' as row FIELDTERMINATOR '\t'
        MERGE (x:disease {Name: row.disease})
        MERGE (y:gene {Name: row.gene})
        MERGE (x) -[:associated_with {score:row.score, ei:row.EI, year_initial:row.year_initial, year_final:row.year_final}] -> (y)"""

        results = session.run(q7)
        data = results.data()

        print("Added Disgenet Relationships")
    except:
        print("Disgenet Relationships already added")


def disgenet_disease_prop():
    try:
        q8 = """LOAD CSV WITH HEADERS FROM 'file:///disgenet_disease_node.tsv' as csvLine FIELDTERMINATOR '\t'
            MATCH (k {Name: csvLine.disease})
            SET k.diseaseID = csvLine.diseaseID, k.disease_class = csvLine.disease_class, k.disease_class_name = csvLine.disease_class_name, k.disease_semantic_type = csvLine.disease_semantic_type"""

        results = session.run(q8)
        data = results.data()

        print("Added Disgenet Disease properties")
    except:
        print("Disgenet Disease properties already added")


def disgenet_gene_prop():
    try:
        q9 = """LOAD CSV WITH HEADERS FROM 'file:///disgenet_gene_node.tsv' as csvLine FIELDTERMINATOR '\t'
        MATCH (k {Name: csvLine.gene})
        SET k.geneID = csvLine.geneID, k.Protein_Class = csvLine.Protein_Class, k.UniProtID = csvLine.UniProtID, k.DPI = csvLine.DPI, k.DSI = csvLine.DSI"""

        results = session.run(q9)
        data = results.data()

        print("Added Disgenet Gene properties")
    except:
        print("Disgenet Gene properties already added")


def del_lincs_down_rel():
    try:
        q9 = """LOAD CSV WITH HEADERS FROM 'file:///lincs_downregulates_relationship.tsv' as row FIELDTERMINATOR '\t'
        MATCH (n:drug {Name: row.drug})
        MATCH (k:gene {Name: row.gene})
        DETACH DELETE k"""

        results = session.run(q9)
        data = results.data()

        print("Delete Lincs Downregulation relationships")
    except:
        print("Lincs Downregulation relationships already deleted")


def del_lincs_up_rel():
    try:
        q10 = """LOAD CSV WITH HEADERS FROM 'file:///lincs_upregulates_relationship.tsv' as row FIELDTERMINATOR '\t'
        MATCH (n:drug {Name: row.drug})
        MATCH (k:gene {Name: row.gene})
        DETACH DELETE k"""

        results = session.run(q10)
        data = results.data()

        print("Delete Lincs Upregulation relationships")
    except:
        print("Lincs Upregulation relationships already deleted")


def del_geo_down_rel():
    try:
        q11 = """LOAD CSV WITH HEADERS FROM 'file:///geo_downregulates_relationship.tsv' as row FIELDTERMINATOR '\t'
        MATCH (n:disease {Name: row.Disease})
        MATCH (k:gene {Name: row.Gene})
        DETACH DELETE k"""

        results = session.run(q11)
        data = results.data()

        print("Delete GEO Downregulation relationships")
    except:
        print("GEO Downregulation relationships already deleted")


def del_geo_up_rel():
    try:
        q12 = """LOAD CSV WITH HEADERS FROM 'file:///geo_upregulates_relationship.tsv' as row FIELDTERMINATOR '\t'
        MATCH (n:disease {Name: row.Disease})
        MATCH (k:gene {Name: row.Gene})
        DETACH DELETE k"""

        results = session.run(q12)
        data = results.data()

        print("Delete GEO Upregulation relationships")
    except:
        print("GEO Upregulation relationships already deleted")


def del_disgenet_association_relationships():
    try:
        q13 = """LOAD CSV WITH HEADERS FROM 'file:///disgenet_association_relationship.tsv' as row FIELDTERMINATOR '\t'
        MATCH (n:disease {Name: row.disease})
        MATCH (k:gene {Name: row.gene})
        DETACH DELETE k"""

        results = session.run(q13)
        data = results.data()

        print("Delete Disgenet Relationships")
    except:
        print("Disgenet Relationships already deleted")


def del_string_rel():
    try:
        q14 = """LOAD CSV WITH HEADERS FROM 'file:///string_interacts-with_relationship.tsv' as row FIELDTERMINATOR '\t'
        MATCH (n:protein {Name: row.Protein1})
        MATCH (k:protein {Name: row.Protein2})
        DETACH DELETE n, k"""

        results = session.run(q14)
        data = results.data()

        print("Delete STR relationships")
    except:
        print("STR relationships already deleted")
