import pandas as pd

def fix_data(df):
    """
    To apply after organization to fix missing labels for sex of children.
    :param file_path:
    :return: none, updates .csv file
    """

    tmp = pd.isnull(df["sex"])
    idx = tmp[tmp].index

    #specific corpora dict
    chp_dict = {'g':'female','b':'male'}
    ehs_dict = {'0156':'female','0347':'female','0509':'male','0538':'female','1223':'female','1252':'female','1304':'male','0949':"unknown"}
    elw_dict = {'22118':'male','22120':'male','22128':'male','22148':'male','22180':'male'}
    mcc_dict = {'aurie':'female','rick':'male','vito':'male'}
    wei_dict = {'ben':'male','emily':'female','emma':'female','jillian':'female','matt':'male','roman':'male'}

    for ii in idx:
        if df["role"][ii] == "target_child":
            tname = df["name"][ii]

            #fix champaign data
            if tname.startswith("champaign"):
                df.loc[ii,"sex"] = chp_dict[tname[-1]]

            elif tname.startswith("macwhinney_rossmark"):
                df.loc[ii,"sex"] = "male"

            elif tname.startswith("weist"):
                df.loc[ii,"sex"] = wei_dict[tname[6:]]

            elif tname.startswith("ehs"):
                df.loc[ii,"sex"] = ehs_dict[tname[-4:]]

            elif tname.startswith("ellisweismer"):
                df.loc[ii,"sex"] = elw_dict[tname[-5:]]

            elif tname.startswith("mccune"):
                df.loc[ii,"sex"] = mcc_dict[tname[7:]]

            elif tname.startswith("rollins"):
                df.loc[ii,"sex"] = 'unknown'

            elif tname.startswith("bloom_Peter"):
                df.loc[ii,"sex"] = "male"

    return df