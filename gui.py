from flask import Flask, render_template, request, current_app as app, redirect
import os
import numpy as np
import glob
import itertools
import pandas as pd
from os.path import exists
import subprocess
from gevent.pywsgi import WSGIServer
import delta

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Add AWS keys every 24 hours
aws_access_key_id = "ASIAXRH5YCHGUMLIKYGP"
aws_secret_access_key = "C1T9oip8ZluWtsFAxszeIWqb43SZ1zrpCvRbu7eq"
aws_session_token = "IQoJb3JpZ2luX2VjECUaDmFwLXNvdXRoZWFzdC0xIkgwRgIhAPkRJ0S5Az5BinPPLXSs//aDPAgI95fbSNCeNHL3UhpuAiEAlgYytn7g5WX6K9nUS4TpoMZl2FuiGqxlW9UjUz1TdHsqqQMIzv//////////ARABGgw1MTgwNzU3MTYwNDUiDC6kYkifsgCDEC3zBCr9AoFg95+zJTV3+b+om8/3AEGzrmsMy18qQOps2zO++e/ShUULapEvwmMIaiKPWQQGbBB8rt6tcPK9j+SupRUGMWTVkjNRxhO2EB+VDwIAswXzFffgjGVMFbWmT5OUo1d+qsfECxBKO/IC7iVlAjVBEDD9EnZ7zaWsFBQFnc+rlSwFjobqpHM5xrx0ITKysfcy20f0/A9RwB+DnwUDKfztfVAD0zS1Jw3hY23tcOntImhxOR6F1ypIKHUQGAB8HvLAjoYJH3zfy76kzK4+FDj/ovjqvBM/Scp1weBIWFHBY6xoUQhQb/gqruXrTsgnkn3hvlBs6I4phvCw2TG1GeBmovUmOvHFe7vjBoJ7oPpXTkYjzPxc4SCDVQkvaXrbOdgq22MeT+7+HFeBAHtVDZtbt4bmAKQkRzbn/HRvwmVCr70DnO45VBscpQdh56J28I7EiHk9MW/RTj8ibQYKPFnj2hbLHusdQQFHWhxUpuYyZM+91fwJnqlEaT0eyNTBVzCI1vOSBjqlAVnMTDUZldHYh/A/9JJYQUbSScv4XZM6OhqHc+BqkOSgIH0gfH5H5pSONk1VElrtpiAbjPwsWUiJTFz/ie7iPkD/+1cheAaYwMQURIcHgNWek9Xp6tH16GFEgN9+Vp2Ed4N+RB+zVo+Cgt0Vv4h2MyySX/rQ/FaRMVTJSA1oXx7wERuL48Mqr8yr5eKCFJHHcWxlcWE097h1alBJb/Ko8MAZTFa3qA=="

# Set AWS creds
print("1")
os.system(f"dvc remote modify storage access_key_id {aws_access_key_id}")
print("2")
os.system(
    f"dvc remote modify storage secret_access_key {aws_secret_access_key}")
print("3")
os.system(f"dvc remote modify storage session_token {aws_session_token}")


@app.route('/upload1', methods=['POST'])
def upload1():
    """
    Add new version of the database
    """
    global filename, DIR_NAME, filepath
    DIR_NAME = request.form.get("database")
    print(DIR_NAME)

    for file in request.files.getlist('file'):
        print("File received")
        filename = file.filename
        filepath = DIR_NAME + "/" + filename
        print(filepath)

    if (exists(filepath + ".csv")):
        new_version_df = pd.read_csv(filepath+".csv")
        # Get max value from a column of a dataframe
        new_version = new_version_df['version'].max() + 1
    else:
        new_version = 1

    git_message = "Added version " + str(new_version) + \
        " of the " + filename + " in " + DIR_NAME + " database"
    print(git_message)

    # Push the doubled data to S3 bucket & log the details in BitBucket & DVC
    print("1")
    os.system(f"dvc add {filepath}")
    print("2")
    os.system(f"git add {filepath}.dvc")
    print("3")
    os.system(f"git commit -m '{git_message}'")
    print("4")
    os.system(f"dvc push")
    print("5")
    os.system(f"git push -u origin dvc")

    commit_id = subprocess.getoutput(["git log -n 1 dvc --pretty=format:'%H'"])
    print(commit_id)
    print(filepath)

    # Update current db version with the commit id
    if (exists(filepath + ".csv")):
        print("6.1")
        commit_id_df = pd.read_csv(filepath + ".csv")
        commit_id_df.fillna('NaN', inplace=True)
        commit_id_df.loc[len(commit_id_df.index)] = [
            commit_id, new_version, 'NaN', 'NaN']
        commit_id_df['current_version'][0] = new_version
        commit_id_df['commit_id_current'][0] = commit_id
        print(commit_id_df)
    else:
        print("6.2")
        commit_id_dict = {'commit_id': [commit_id], 'version': [
            new_version], 'commit_id_current': [commit_id], 'current_version': [new_version]}
        commit_id_df = pd.DataFrame(commit_id_dict)
    commit_id_df.to_csv(filepath + ".csv", index=False)

    print("7")

    update_version_number(DIR_NAME)

    # return jsonify(final_info)
    return redirect(request.referrer)


def update_version_number(DIR_NAME):
    """
    Update the consolidated version number of a specific database
    """
    consolidated_df = pd.read_csv(
        DIR_NAME.lower() + f"/{DIR_NAME.lower()}_consolidated_version.csv")

    result = glob.glob(f'{DIR_NAME}*/**.tsv')

    lister = []

    for tsv in result:
        try:
            df = pd.read_csv(tsv + '.csv')
            lister.append(list(np.arange(1, df['version'].max()+1)))
            print(lister)
        except:
            pass

    print(len(lister))
    version_combination = list(itertools.product(*lister))
    # print(version_combination)

    # print(consolidated_df.columns[:-1])
    df = pd.DataFrame(version_combination,
                      columns=consolidated_df.columns[:-1])
    print(df)
    df['consolidated_version'] = np.arange(1, len(df)+1)
    df.to_csv(DIR_NAME.lower() +
              f"/{DIR_NAME.lower()}_consolidated_version.csv", index=False)


@app.route('/switch_kg_version', methods=['POST'])
def switch_kg_version():
    """
    Switch the version of the database
    """

    new_version = str(request.form.get("kg_switch_version"))
    current_version = pd.read_csv("current_kg_version.csv")[
        'kg_current_version'].values[0]

    delta.get_db_files_version(current_version, new_version)

    # return redirect(request.referrer)
    return render_template('index.html', new_version=new_version)


@app.route('/switch_kg_version_to_latest', methods=['POST'])
def switch_kg_version_to_latest():
    """
    Switch the version of the database to latest version
    """
    # Get latest version of the KG
    latest_version = max(pd.read_csv("kg_consolidated_versions.csv")[
        'kg_version'], key=lambda x: int(x.split(".")[-1]))
    current_version = pd.read_csv("current_kg_version.csv")[
        'kg_current_version'].values[0]

    delta.get_db_files_version(current_version, latest_version)

    # return redirect(request.referrer)
    return render_template('index.html')


@app.route('/kg_db_mapping')
def kg_db_mapping_refresh1():
    return render_template('index.html')


@app.route('/kg_db_versions')
def kg_db_mapping_refresh():
    return render_template('kg_db_versions.html')


@app.route('/kg_db_versions', methods=["POST"])
def kg_db_versions():
    """
    Get the database version from KG version
    """
    def get_db_version(new_version):
        """
        Get the database version from KG version
        """
        print('Version: ', new_version)
        kg_versions = pd.read_csv("kg_consolidated_versions.csv")
        print(kg_versions)
        print(new_version)
        geo_version = kg_versions.loc[kg_versions['kg_version']
                                      == new_version, 'geo'].values[0]
        string_version = kg_versions.loc[kg_versions['kg_version']
                                         == new_version, 'string'].values[0]
        lincs_version = kg_versions.loc[kg_versions['kg_version']
                                        == new_version, 'lincs'].values[0]
        disgenet_version = kg_versions.loc[kg_versions['kg_version']
                                           == new_version, 'disgenet'].values[0]
        return string_version, geo_version, lincs_version, disgenet_version

    new_version = str(request.form.get("kg_version_for_db"))
    string_version, geo_version, lincs_version, disgenet_version = get_db_version(
        new_version)
    print(string_version)
    print(geo_version)
    print(lincs_version)
    print(disgenet_version)

    return render_template("kg_db_versions.html",
                           string_version=string_version, geo_version=geo_version, lincs_version=lincs_version, disgenet_version=disgenet_version)


@app.route('/table')
def update_version_number_kg():
    """
    Display Table
    Update the kg version & visualize all the versions and their corresponding databases
    """

    max_consolidated_version_geo = pd.read_csv(
        "GEO/geo_consolidated_version.csv")['consolidated_version'].max()
    max_consolidated_version_string = pd.read_csv(
        "STRING/string_consolidated_version.csv")['consolidated_version'].max()
    max_consolidated_version_lincs = pd.read_csv(
        "LINCS/lincs_consolidated_version.csv")['consolidated_version'].max()
    max_consolidated_version_disgenet = pd.read_csv(
        "DisGeNET/disgenet_consolidated_version.csv")['consolidated_version'].max()

    geo_versions = np.arange(1, max_consolidated_version_geo + 1)
    string_versions = np.arange(1, max_consolidated_version_string + 1)
    lincs_versions = np.arange(1, max_consolidated_version_lincs + 1)
    disgenet_versions = np.arange(1, max_consolidated_version_disgenet + 1)

    print('Got version numbers of each database')

    version_combination = list(
        itertools.product(geo_versions, string_versions, lincs_versions, disgenet_versions))

    df = pd.DataFrame(version_combination,
                      columns=["geo", "string", "lincs", "disgenet"])

    for i in range(len(df)):
        # print(i)
        df.loc[df.index[i], 'kg_version'] = f"1.0.{int((i+1))}"
    print(df)
    # df.index.name = 'kg_version'
    df.to_csv("kg_consolidated_versions.csv", index=False)
    print('Done')

    return render_template('kg_versions.html', tables=[df.to_html()], titles=[''])


@ app.route('/kg_specific', methods=['GET'])
def kg_specific():
    """
    Get the latest & current version of databases loaded in the KG
    """

    def current_specific_version(database):
        try:
            commit_id_df = pd.read_csv(database + ".csv")
            current_version = int(commit_id_df.loc[commit_id_df['current_version']
                                                   == commit_id_df['current_version'].max(), 'current_version'].values[0])
            # print(current_version)
            return current_version
        except:
            return 0

    def latest_specific_version(database):
        try:
            commit_id_df = pd.read_csv(database + ".csv")
            latest_version = int(commit_id_df['version'].max())
            # print(latest_version)
            return latest_version
        except:
            print("No version available")
            return 0

    geo_downregulates_relationship_latest = latest_specific_version(
        "GEO/geo_downregulates_relationship.tsv")
    geo_upregulates_relationship_latest = latest_specific_version(
        "GEO/geo_upregulates_relationship.tsv")
    string_interacts_with_relationship_latest = latest_specific_version(
        "STRING/string_interacts-with_relationship.tsv")
    string_protein_node_latest = latest_specific_version(
        "STRING/string_protein_node.tsv")
    disgenet_association_relationship_latest = latest_specific_version(
        "DisGeNET/disgenet_association_relationship.tsv")
    disgenet_disease_node_latest = latest_specific_version(
        "DisGeNET/disgenet_disease_node.tsv")
    disgenet_gene_node_latest = latest_specific_version(
        "DisGeNET/disgenet_gene_node.tsv")
    lincs_downregulates_relationship_latest = latest_specific_version(
        "LINCS/lincs_downregulates_relationship.tsv")
    lincs_upregulates_relationship_latest = latest_specific_version(
        "LINCS/lincs_upregulates_relationship.tsv")

    geo_downregulates_relationship_current = current_specific_version(
        "GEO/geo_downregulates_relationship.tsv")
    geo_upregulates_relationship_current = current_specific_version(
        "GEO/geo_upregulates_relationship.tsv")
    string_interacts_with_relationship_current = current_specific_version(
        "STRING/string_interacts-with_relationship.tsv")
    string_protein_node_current = current_specific_version(
        "STRING/string_protein_node.tsv")
    disgenet_association_relationship_current = current_specific_version(
        "DisGeNET/disgenet_association_relationship.tsv")
    disgenet_disease_node_current = current_specific_version(
        "DisGeNET/disgenet_disease_node.tsv")
    disgenet_gene_node_current = current_specific_version(
        "DisGeNET/disgenet_gene_node.tsv")
    lincs_downregulates_relationship_current = current_specific_version(
        "LINCS/lincs_downregulates_relationship.tsv")
    lincs_upregulates_relationship_current = current_specific_version(
        "LINCS/lincs_upregulates_relationship.tsv")

    return render_template('kg_specific.html',
                           geo_downregulates_relationship_latest=geo_downregulates_relationship_latest,
                           geo_upregulates_relationship_latest=geo_upregulates_relationship_latest,
                           string_interacts_with_relationship_latest=string_interacts_with_relationship_latest,
                           string_protein_node_latest=string_protein_node_latest,
                           geo_downregulates_relationship_current=geo_downregulates_relationship_current,
                           geo_upregulates_relationship_current=geo_upregulates_relationship_current,
                           string_interacts_with_relationship_current=string_interacts_with_relationship_current,
                           string_protein_node_current=string_protein_node_current,
                           disgenet_association_relationship_latest=disgenet_association_relationship_latest,
                           disgenet_disease_node_latest=disgenet_disease_node_latest,
                           disgenet_gene_node_latest=disgenet_gene_node_latest,
                           disgenet_association_relationship_current=disgenet_association_relationship_current,
                           disgenet_disease_node_current=disgenet_disease_node_current,
                           disgenet_gene_node_current=disgenet_gene_node_current,
                           lincs_downregulates_relationship_latest=lincs_downregulates_relationship_latest,
                           lincs_upregulates_relationship_latest=lincs_upregulates_relationship_latest,
                           lincs_downregulates_relationship_current=lincs_downregulates_relationship_current,
                           lincs_upregulates_relationship_current=lincs_upregulates_relationship_current)


@ app.route('/kg', methods=['GET'])
def kg():
    """
    Loads the KG page - kg.html
    """

    def current_specific_version(database):
        try:
            commit_id_df = pd.read_csv(database + ".csv")
            current_version = int(commit_id_df.loc[commit_id_df['current_version']
                                                   == commit_id_df['current_version'].max(), 'current_version'].values[0])
            # print(current_version)
            return current_version
        except:
            return 0

    def current_version():
        consolidated_df = pd.read_csv("kg_consolidated_versions.csv")
        geo_downregulates_relationship_current = current_specific_version(
            "GEO/geo_downregulates_relationship.tsv")
        geo_upregulates_relationship_current = current_specific_version(
            "GEO/geo_upregulates_relationship.tsv")
        string_interacts_with_relationship_current = current_specific_version(
            "STRING/string_interacts-with_relationship.tsv")
        string_protein_node_current = current_specific_version(
            "STRING/string_protein_node.tsv")
        lincs_downregulates_relationship_current = current_specific_version(
            "LINCS/lincs_downregulates_relationship.tsv")
        lincs_upregulates_relationship_current = current_specific_version(
            "LINCS/lincs_upregulates_relationship.tsv")
        disgenet_association_relationship_current = current_specific_version(
            "DisGeNET/disgenet_association_relationship.tsv")
        disgenet_disease_node_current = current_specific_version(
            "DisGeNET/disgenet_disease_node.tsv")
        disgenet_gene_node_current = current_specific_version(
            "DisGeNET/disgenet_gene_node.tsv")

        geo_current = pd.read_csv("GEO/geo_consolidated_version.csv")
        string_current = pd.read_csv("STRING/string_consolidated_version.csv")
        lincs_current = pd.read_csv("LINCS/lincs_consolidated_version.csv")
        disgenet_current = pd.read_csv(
            "DisGeNET/disgenet_consolidated_version.csv")

        geo_current_no = geo_current.loc[(geo_current['version_geo_upregulates_relationship'] == geo_upregulates_relationship_current) &
                                         (geo_current['version_geo_downregulates_relationship'] == geo_downregulates_relationship_current), "consolidated_version"].iloc[0]

        string_current_no = string_current.loc[(string_current['version_string_interacts-with_relationship'] == string_interacts_with_relationship_current) &
                                               (string_current['version_string_protein_node'] == string_protein_node_current), 'consolidated_version'].iloc[0]

        lincs_current_no = lincs_current.loc[(lincs_current['version_lincs_upregulates_relationship'] == lincs_upregulates_relationship_current) &
                                             (lincs_current['version_lincs_downregulates_relationship'] == lincs_downregulates_relationship_current), "consolidated_version"].iloc[0]

        disgenet_current_no = disgenet_current.loc[(disgenet_current['version_disgenet_association_relationship'] == disgenet_association_relationship_current) &
                                                   (disgenet_current['version_disgenet_disease_node'] == disgenet_disease_node_current) &
                                                   (disgenet_current['version_disgenet_gene_node'] == disgenet_gene_node_current), "consolidated_version"].iloc[0]

        return geo_current_no, string_current_no, lincs_current_no, disgenet_current_no

    def latest_version(database):
        try:
            consolidated_df = pd.read_csv(database + ".csv")
            latest_version = int(consolidated_df['consolidated_version'].max())
            # print(latest_version)
            return latest_version
        except:
            print("No version available")
            return 0

    geo_latest = latest_version(
        "GEO/geo_consolidated_version")
    string_latest = latest_version(
        "STRING/string_consolidated_version")
    lincs_latest = latest_version("LINCS/lincs_consolidated_version")
    disgenet_latest = latest_version(
        "DisGeNET/disgenet_consolidated_version")

    geo_current, string_current, lincs_current, disgenet_current = current_version()

    return render_template('kg.html',
                           geo_latest=geo_latest,
                           string_latest=string_latest,
                           lincs_latest=lincs_latest,
                           disgenet_latest=disgenet_latest,
                           geo_current=geo_current,
                           string_current=string_current,
                           lincs_current=lincs_current,
                           disgenet_current=disgenet_current)


@ app.route('/dvc', methods=['GET'])
def dvc():
    latest_version = max(pd.read_csv("kg_consolidated_versions.csv")[
        'kg_version'], key=lambda x: int(x.split(".")[-1]))
    current_version = pd.read_csv("current_kg_version.csv")[
        'kg_current_version'].values[0]
    return render_template('index.html', current_version=current_version, latest_version=latest_version)


if __name__ == '__main__':
    # app.run(debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 4000), app)
    http_server.serve_forever()
