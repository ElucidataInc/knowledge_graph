from auth_disgenet import authenticate_user
from get_graph_components import get_components
import yaml

if __name__ == '__main__':

    yaml_file = './config.yml'

    content = None
    with open(yaml_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            raise yaml.YAMLError("The yaml file {} could not be parsed. {}".format(yaml_file, err))

    disease_id = config['DISGENET_CUI']
    auth_email = config['DISGENET_email']
    auth_pass = config['DISGENET_pass']

    gda_result = authenticate_user(disease_id, auth_email, auth_pass)
    
    with open(f'disease_gene_{disease_id}.tsv', 'w') as f:
        f.write(gda_result.text)
    f.close()
    
    gene, disease, relationships = get_components(disease_id)

    gene.to_csv('disgenet_gene_node.tsv', sep = '\t')
    disease.to_csv('disgenet_disease_node.tsv', sep = '\t')
    relationships.to_csv('disgenet_association_relationship.tsv', sep = '\t')
