import pandas as pd

def get_components(disease_id):

    disease_gene = pd.read_csv(f'disease_gene_{disease_id}.tsv', sep = '\t')

    gene_nodes = disease_gene[["gene_symbol", "geneid", "protein_class_name", "uniprotid", "gene_dpi", "gene_dsi"]]
    gene_nodes.columns = ['gene', 'geneID', 'Protein_Class', 'UniProtID', 'DPI', 'DSI']

    disease_nodes = disease_gene[["disease_name", "diseaseid", "disease_class", "disease_class_name", "disease_semantic_type"]]
    disease_nodes.columns = ['disease', 'diseaseID', 'disease_class', 'disease_class_name', 'disease_semantic_type']
            
    relationship_dis_gene = disease_gene[['disease_name', 'gene_symbol', 'score', 'ei', 'year_initial', 'year_final']]
    relationship_dis_gene.columns = ['disease', 'gene', 'score', 'EI', 'year_initial', 'year_final']

    return (gene_nodes, disease_nodes, relationship_dis_gene)