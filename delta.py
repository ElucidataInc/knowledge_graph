import numpy as np
import pandas as pd
import os
import kg_generator_with_delta

import warnings
warnings.filterwarnings("ignore")


def update_database_versions_from_kg_version(new_version):
    # Get database versions from KG
    kg_versions = pd.read_csv("kg_consolidated_versions.csv")

    geo_version = kg_versions.loc[kg_versions['kg_version']
                                  == new_version, 'geo'].values[0]
    string_version = kg_versions.loc[kg_versions['kg_version']
                                     == new_version, 'string'].values[0]
    lincs_version = kg_versions.loc[kg_versions['kg_version']
                                    == new_version, 'lincs'].values[0]
    disgenet_version = kg_versions.loc[kg_versions['kg_version']
                                       == new_version, 'disgenet'].values[0]
    print("geo_version: ", geo_version)
    print("string_version: ", string_version)
    print("lincs_version: ", lincs_version)
    print("disgenet_version: ", disgenet_version)

    # Get database sub-file versions and update them
    DIR_NAMES = ["GEO", "STRING", "LINCS", "DisGeNET"]

    for DIR_NAME in DIR_NAMES:
        if DIR_NAME == "GEO":
            consolidated_version_df = pd.read_csv(
                "GEO/geo_consolidated_version.csv")
            up_reg = consolidated_version_df.loc[consolidated_version_df['consolidated_version']
                                                 == geo_version, 'version_geo_upregulates_relationship'].values[0]
            down_reg = consolidated_version_df.loc[consolidated_version_df['consolidated_version']
                                                   == geo_version, 'version_geo_downregulates_relationship'].values[0]
            commit_id_df = pd.read_csv(
                "GEO/geo_downregulates_relationship.tsv.csv")
            commit_id_df['current_version'][0] = down_reg
            commit_id_df['commit_id_current'][0] = 'NaN'
            commit_id_df.to_csv(
                "GEO/geo_downregulates_relationship.tsv.csv", index=False)

            commit_id_df = pd.read_csv(
                "GEO/geo_upregulates_relationship.tsv.csv")
            commit_id_df['current_version'][0] = up_reg
            commit_id_df['commit_id_current'][0] = 'NaN'
            commit_id_df.to_csv(
                "GEO/geo_upregulates_relationship.tsv.csv", index=False)
        if DIR_NAME == "STRING":
            consolidated_version_df = pd.read_csv(
                "STRING/string_consolidated_version.csv")
            string_rel = consolidated_version_df.loc[consolidated_version_df['consolidated_version']
                                                     == string_version, 'version_string_interacts-with_relationship'].values[0]
            string_prop = consolidated_version_df.loc[consolidated_version_df['consolidated_version']
                                                      == string_version, 'version_string_protein_node'].values[0]
            commit_id_df = pd.read_csv(
                "STRING/string_interacts-with_relationship.tsv.csv")
            commit_id_df['current_version'][0] = string_rel
            commit_id_df['commit_id_current'][0] = 'NaN'
            commit_id_df.to_csv(
                "STRING/string_interacts-with_relationship.tsv.csv", index=False)

            commit_id_df = pd.read_csv("STRING/string_protein_node.tsv.csv")
            commit_id_df['current_version'][0] = string_prop
            commit_id_df['commit_id_current'][0] = 'NaN'
            commit_id_df.to_csv(
                "STRING/string_protein_node.tsv.csv", index=False)
        if DIR_NAME == "LINCS":
            consolidated_version_df = pd.read_csv(
                "LINCS/lincs_consolidated_version.csv")
            up_reg = consolidated_version_df.loc[consolidated_version_df['consolidated_version']
                                                 == lincs_version, 'version_lincs_upregulates_relationship'].values[0]
            down_reg = consolidated_version_df.loc[consolidated_version_df['consolidated_version']
                                                   == lincs_version, 'version_lincs_downregulates_relationship'].values[0]
            commit_id_df = pd.read_csv(
                "LINCS/lincs_downregulates_relationship.tsv.csv")
            commit_id_df['current_version'][0] = down_reg
            commit_id_df['commit_id_current'][0] = 'NaN'
            commit_id_df.to_csv(
                "LINCS/lincs_downregulates_relationship.tsv.csv", index=False)

            commit_id_df = pd.read_csv(
                "LINCS/lincs_upregulates_relationship.tsv.csv")
            commit_id_df['current_version'][0] = up_reg
            commit_id_df['commit_id_current'][0] = 'NaN'
            commit_id_df.to_csv(
                "LINCS/lincs_upregulates_relationship.tsv.csv", index=False)
        if DIR_NAME == "DisGeNET":
            consolidated_version_df = pd.read_csv(
                "DisGeNET/disgenet_consolidated_version.csv")
            disgenet_assoc = consolidated_version_df.loc[consolidated_version_df['consolidated_version']
                                                         == disgenet_version, 'version_disgenet_association_relationship'].values[0]
            disgenet_disease = consolidated_version_df.loc[consolidated_version_df[
                'consolidated_version'] == disgenet_version, 'version_disgenet_disease_node'].values[0]
            disgenet_gene = consolidated_version_df.loc[consolidated_version_df['consolidated_version']
                                                        == disgenet_version, 'version_disgenet_gene_node'].values[0]
            commit_id_df = pd.read_csv(
                "DisGeNET/disgenet_association_relationship.tsv.csv")
            commit_id_df['current_version'][0] = disgenet_assoc
            commit_id_df['commit_id_current'][0] = 'NaN'
            commit_id_df.to_csv(
                "DisGeNET/disgenet_association_relationship.tsv.csv", index=False)

            commit_id_df = pd.read_csv(
                "DisGeNET/disgenet_disease_node.tsv.csv")
            commit_id_df['current_version'][0] = disgenet_disease
            commit_id_df['commit_id_current'][0] = 'NaN'
            commit_id_df.to_csv(
                "DisGeNET/disgenet_disease_node.tsv.csv", index=False)

            commit_id_df = pd.read_csv("DisGeNET/disgenet_gene_node.tsv.csv")
            commit_id_df['current_version'][0] = disgenet_gene
            commit_id_df['commit_id_current'][0] = 'NaN'
            commit_id_df.to_csv(
                "DisGeNET/disgenet_gene_node.tsv.csv", index=False)


def get_db_version(current_version, new_version):
    """
    Get the database version from KG version
    """
    kg_versions = pd.read_csv("kg_consolidated_versions.csv")
    # print(kg_versions)

    # Database version of the new version
    geo_version_new = kg_versions.loc[kg_versions['kg_version']
                                      == new_version, 'geo'].values[0]
    string_version_new = kg_versions.loc[kg_versions['kg_version']
                                         == new_version, 'string'].values[0]
    lincs_version_new = kg_versions.loc[kg_versions['kg_version']
                                        == new_version, 'lincs'].values[0]
    disgenet_version_new = kg_versions.loc[kg_versions['kg_version']
                                           == new_version, 'disgenet'].values[0]

    # Database versions of current version
    geo_version_current = kg_versions.loc[kg_versions['kg_version']
                                          == current_version, 'geo'].values[0]
    string_version_current = kg_versions.loc[kg_versions['kg_version']
                                             == current_version, 'string'].values[0]
    lincs_version_current = kg_versions.loc[kg_versions['kg_version']
                                            == current_version, 'lincs'].values[0]
    disgenet_version_current = kg_versions.loc[kg_versions['kg_version']
                                               == current_version, 'disgenet'].values[0]
    return geo_version_current, string_version_current, lincs_version_current, \
        disgenet_version_current, string_version_new, geo_version_new, \
        lincs_version_new, disgenet_version_new


def get_db_files_version(current_version, new_version):
    # Get new and current database versions
    geo_version_current, string_version_current, lincs_version_current, disgenet_version_current, \
        string_version_new, geo_version_new, lincs_version_new, disgenet_version_new = get_db_version(
            current_version, new_version)

    geo = pd.read_csv("GEO/geo_consolidated_version.csv")
    geo_downregulates_relationship_new = geo.loc[geo['consolidated_version']
                                                 == geo_version_new, 'version_geo_downregulates_relationship'].values[0]
    geo_downregulates_relationship_current = geo.loc[geo['consolidated_version']
                                                     == geo_version_current, 'version_geo_downregulates_relationship'].values[0]
    geo_upregulates_relationship_new = geo.loc[geo['consolidated_version']
                                               == geo_version_new, 'version_geo_upregulates_relationship'].values[0]
    geo_upregulates_relationship_current = geo.loc[geo['consolidated_version']
                                                   == geo_version_current, 'version_geo_upregulates_relationship'].values[0]
    print("GEO - Downregulates current version: %s \nGEO - Downregulates new version: %s" %
          (geo_downregulates_relationship_current, geo_downregulates_relationship_new))
    print("GEO - Upregulates current version: %s \nGEO - Upregulates new version: %s" %
          (geo_upregulates_relationship_current, geo_upregulates_relationship_new))

    string = pd.read_csv("STRING/string_consolidated_version.csv")
    string_interacts_with_relationship_new = string.loc[string['consolidated_version']
                                                        == string_version_new, 'version_string_interacts-with_relationship'].values[0]
    string_interacts_with_relationship_current = string.loc[string['consolidated_version']
                                                            == string_version_current, 'version_string_interacts-with_relationship'].values[0]
    string_protein_node_new = string.loc[string['consolidated_version']
                                         == string_version_new, 'version_string_protein_node'].values[0]
    string_protein_node_current = string.loc[string['consolidated_version']
                                             == string_version_current, 'version_string_protein_node'].values[0]
    print("STRING - Relationship current version: %s \nSTRING - Relationship new version: %s" %
          (string_interacts_with_relationship_current, string_interacts_with_relationship_new))
    print("STRING - Protein node current version: %s \nSTRING - Protein node new version: %s" %
          (string_protein_node_current, string_protein_node_new))

    lincs = pd.read_csv("LINCs/lincs_consolidated_version.csv")
    lincs_downregulates_relationship_new = lincs.loc[lincs['consolidated_version']
                                                     == lincs_version_new, 'version_lincs_downregulates_relationship'].values[0]
    lincs_upregulates_relationship_new = lincs.loc[lincs['consolidated_version']
                                                   == lincs_version_new, 'version_lincs_upregulates_relationship'].values[0]
    lincs_downregulates_relationship_current = lincs.loc[lincs['consolidated_version']
                                                         == lincs_version_current, 'version_lincs_downregulates_relationship'].values[0]
    lincs_upregulates_relationship_current = lincs.loc[lincs['consolidated_version']
                                                       == lincs_version_current, 'version_lincs_upregulates_relationship'].values[0]
    print("LINCS - Downregulates current version: %s \nLINCs - Downregulates new version: %s" %
          (lincs_downregulates_relationship_current, lincs_downregulates_relationship_new))
    print("LINCS - Upregulates current version: %s \nLINCs - Upregulates new version: %s" %
          (lincs_upregulates_relationship_current, lincs_upregulates_relationship_new))

    disgenet = pd.read_csv("DisGeNET/disgenet_consolidated_version.csv")
    disgenet_association_relationship_new = disgenet.loc[disgenet['consolidated_version']
                                                         == disgenet_version_new, 'version_disgenet_association_relationship'].values[0]
    disgenet_association_relationship_current = disgenet.loc[disgenet['consolidated_version']
                                                             == disgenet_version_current, 'version_disgenet_association_relationship'].values[0]
    disgenet_disease_node_new = disgenet.loc[disgenet['consolidated_version']
                                             == disgenet_version_new, 'version_disgenet_disease_node'].values[0]
    disgenet_disease_node_current = disgenet.loc[disgenet['consolidated_version']
                                                 == disgenet_version_current, 'version_disgenet_disease_node'].values[0]
    disgenet_gene_node_current = disgenet.loc[disgenet['consolidated_version']
                                              == disgenet_version_current, 'version_disgenet_gene_node'].values[0]
    disgenet_gene_node_new = disgenet.loc[disgenet['consolidated_version']
                                          == disgenet_version_new, 'version_disgenet_gene_node'].values[0]
    print("DisGeNET - Association current version: %s \nDisGeNET - Association new version: %s" %
          (disgenet_association_relationship_current, disgenet_association_relationship_new))
    print("DisGeNET - Disease node current version: %s \nDisGeNET - Disease node new version: %s" %
          (disgenet_disease_node_current, disgenet_disease_node_new))
    print("DisGeNET - Gene node current version: %s \nDisGeNET - Gene node new version: %s" %
          (disgenet_gene_node_current, disgenet_gene_node_new))

    get_intermediate_versions("GEO/geo_downregulates_relationship.tsv",
                              geo_downregulates_relationship_current, geo_downregulates_relationship_new)
    get_intermediate_versions("GEO/geo_upregulates_relationship.tsv",
                              geo_upregulates_relationship_current, geo_upregulates_relationship_new)
    # get_intermediate_versions("STRING/string_interacts-with_relationship.tsv",
    #                           string_interacts_with_relationship_current, string_interacts_with_relationship_new)
    get_intermediate_versions("STRING/string_protein_node.tsv",
                              string_protein_node_current, string_protein_node_new)
    get_intermediate_versions("LINCS/lincs_downregulates_relationship.tsv",
                              lincs_downregulates_relationship_current, lincs_downregulates_relationship_new)
    get_intermediate_versions("LINCS/lincs_upregulates_relationship.tsv",
                              lincs_upregulates_relationship_current, lincs_upregulates_relationship_new)
    get_intermediate_versions("DisGeNET/disgenet_association_relationship.tsv",
                              disgenet_association_relationship_current, disgenet_association_relationship_new)
    get_intermediate_versions("DisGeNET/disgenet_disease_node.tsv",
                              disgenet_disease_node_current, disgenet_disease_node_new)
    get_intermediate_versions("DisGeNET/disgenet_gene_node.tsv",
                              disgenet_gene_node_current, disgenet_gene_node_new)
    current_kg_versions = pd.read_csv("current_kg_version.csv")
    current_kg_versions.loc[0] = new_version
    current_kg_versions.to_csv("current_kg_version.csv", index=False)
    update_database_versions_from_kg_version(new_version)


def get_intermediate_versions(filepath, current_version, new_version):
    # Check if the new version is greater than the current version
    print("\nDatabase File: ", filepath)
    if new_version > current_version:
        # Find out the difference between the new version and the current version
        diff = new_version - current_version
        # Get the versions that need to be incorporated into the KG
        versions = np.arange(current_version + 1, new_version + 1)
        print("Intermediate versions to be incorporated into the KG: ", versions)
        for i in range(len(versions)):
            print("Switched to version: ", versions[i])
            switch_version(filepath, versions[i])
            add_version_to_kg(filepath)

    if new_version < current_version:
        # Find out the difference between the new version and the current version
        diff = current_version - new_version
        # Get the versions that need to be removed from the KG
        versions = np.arange(new_version + 1, current_version + 1)
        print("Intermediate versions to be removed from the KG: ", versions)
        for i in range(len(versions)):
            print("Switched to version: ", versions[i])
            switch_version(filepath, versions[i])
            delete_version_from_kg(filepath)

    if new_version == current_version:
        print("No change in version")


def switch_version(filepath, new_version):
    """
    This function switches the version of the database file.
    """
    DIR_NAME = filepath.split("/")[0]
    print(DIR_NAME)
    print(filepath)

    commit_id_df = pd.read_csv(filepath + ".csv")
    commit_id = commit_id_df.loc[commit_id_df['version']
                                 == new_version, 'commit_id'].values[0]
    print('Version Available')
    print("Commit ID: ", commit_id)

    git_message = "Switched to version " + \
        str(new_version) + " of " + (os.path.basename(filepath)) + \
        " of the " + DIR_NAME + " database"

    print("\nGit message : \n", git_message)

    print("1")
    os.system(f"git checkout '{commit_id}' '{filepath}.dvc'")
    print("2")
    os.system(f"dvc checkout")
    print("3")
    os.system(f"git commit -m '{git_message}'")
    print("4")
    os.system(f"dvc push")
    print("5")
    os.system(f"git push -u origin dvc")

    commit_id_df['current_version'][0] = new_version
    commit_id_df['commit_id_current'][0] = commit_id
    commit_id_df.to_csv(filepath + ".csv", index=False)


def add_version_to_kg(filepath):
    """
    Add version to KG in Neo4J environment using Python connector for CYPHER
    """
    if filepath == "GEO/geo_downregulates_relationship.tsv":
        print("Add to KG: ", filepath)
        kg_generator_with_delta.copy("GEO/geo_downregulates_relationship.tsv")
        kg_generator_with_delta.geo_down_rel()
    if filepath == "GEO/geo_upregulates_relationship.tsv":
        print("Add to KG: ", filepath)
        kg_generator_with_delta.copy("GEO/geo_upregulates_relationship.tsv")
        kg_generator_with_delta.geo_up_rel()
    if filepath == "STRING/string_interacts-with_relationship.tsv":
        print("Add to KG: ", filepath)
        kg_generator_with_delta.copy(
            "STRING/string_interacts-with_relationship.tsv")
        kg_generator_with_delta.string_rel()
    if filepath == "STRING/string_protein_node.tsv":
        print("Add to KG: ", filepath)
        kg_generator_with_delta.copy("STRING/string_protein_node.tsv")
        kg_generator_with_delta.string_prop()
    if filepath == "LINCS/lincs_downregulates_relationship.tsv":
        print("Add to KG: ", filepath)
        kg_generator_with_delta.copy(
            "LINCS/lincs_downregulates_relationship.tsv")
        kg_generator_with_delta.lincs_down_rel()
    if filepath == "LINCS/lincs_upregulates_relationship.tsv":
        print("Add to KG: ", filepath)
        kg_generator_with_delta.copy(
            "LINCS/lincs_upregulates_relationship.tsv")
        kg_generator_with_delta.lincs_up_rel()
    if filepath == "DisGeNET/disgenet_association_relationship.tsv":
        print("Add to KG: ", filepath)
        kg_generator_with_delta.copy(
            "DisGeNET/disgenet_association_relationship.tsv")
        kg_generator_with_delta.disgenet_association_relationships()
    if filepath == "DisGeNET/disgenet_disease_node.tsv":
        print("Add to KG: ", filepath)
        kg_generator_with_delta.copy("DisGeNET/disgenet_disease_node.tsv")
        kg_generator_with_delta.disgenet_disease_prop()
    if filepath == "DisGeNET/disgenet_gene_node.tsv":
        print("Add to KG: ", filepath)
        kg_generator_with_delta.copy("DisGeNET/disgenet_gene_node.tsv")
        kg_generator_with_delta.disgenet_gene_prop()


def delete_version_from_kg(filepath):
    """
    Delete version from KG in Neo4J environment using Python connector for CYPHER
    """
    # check if the NSCLC disease gets deleted in below functions
    if filepath == "GEO/geo_downregulates_relationship.tsv":
        kg_generator_with_delta.copy("GEO/geo_downregulates_relationship.tsv")
        kg_generator_with_delta.del_geo_down_rel()
    if filepath == "GEO/geo_upregulates_relationship.tsv":
        kg_generator_with_delta.copy("GEO/geo_upregulates_relationship.tsv")
        kg_generator_with_delta.del_geo_up_rel()
    if filepath == "STRING/string_interacts-with_relationship.tsv":
        kg_generator_with_delta.copy(
            "STRING/string_interacts-with_relationship.tsv")
        kg_generator_with_delta.del_string_rel()
    if filepath == "LINCS/lincs_downregulates_relationship.tsv":
        kg_generator_with_delta.copy(
            "LINCS/lincs_downregulates_relationship.tsv")
        kg_generator_with_delta.del_lincs_down_rel()
    if filepath == "LINCS/lincs_upregulates_relationship.tsv":
        kg_generator_with_delta.copy(
            "LINCS/lincs_upregulates_relationship.tsv")
        kg_generator_with_delta.del_lincs_up_rel()
    if filepath == "DisGeNET/disgenet_association_relationship.tsv":
        kg_generator_with_delta.copy(
            "DisGeNET/disgenet_association_relationship.tsv")
        kg_generator_with_delta.del_disgenet_association_relationships()
