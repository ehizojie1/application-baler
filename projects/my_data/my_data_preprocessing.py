
import uproot

def pre_processing(input_path,output_path):

    Branch = "Events"
    Collection = "recoPFJets_ak5PFJets__RECO."
    Objects = "recoPFJets_ak5PFJets__RECO.obj"
    dropped_variables = [
        "recoPFJets_ak5PFJets__RECO.obj.vertex_.fCoordinates.fX",
        "recoPFJets_ak5PFJets__RECO.obj.vertex_.fCoordinates.fY",
        "recoPFJets_ak5PFJets__RECO.obj.vertex_.fCoordinates.fZ",
        "recoPFJets_ak5PFJets__RECO.obj.qx3_",
        "recoPFJets_ak5PFJets__RECO.obj.pdgId_",
        "recoPFJets_ak5PFJets__RECO.obj.status_",
        "recoPFJets_ak5PFJets__RECO.obj.mJetArea",
        "recoPFJets_ak5PFJets__RECO.obj.mPileupEnergy",
        "recoPFJets_ak5PFJets__RECO.obj.mPassNumber"]
    
    # Load data
    tree = uproot.open(input_path)[Branch][Collection][Objects]
    #Type clearing
    names = type_clearing(tree)
    df = tree.arrays(names, library="pd")
    print(df)
    # Clean data
    df = df.drop(columns=dropped_variables)
    df = df.reset_index(drop=True)
    df = df.dropna()
    global cleared_column_names
    cleared_column_names = list(df)
    df.to_pickle(output_path)

def type_clearing(tt_tree):
    type_names = tt_tree.typenames()
    column_type = []
    column_names = []

    # In order to remove non integers or -floats in the TTree,
    # we separate the values and keys
    for keys in type_names:
        column_type.append(type_names[keys])
        column_names.append(keys)

    # Checks each value of the typename values to see if it isn't an int or
    # float, and then removes it
    for i in range(len(column_type)):
        if column_type[i] != "float[]" and column_type[i] != "int32_t[]":
            # print('Index ',i,' was of type ',Typename_list_values[i],'            # and was deleted from the file')
            del column_names[i]

    # Returns list of column names to use in load_data function
    return column_names
    