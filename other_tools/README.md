# Step 1: Convert nbdiff output 

    example: 
    [0, 'modified', ["-os.environ['SAGA_VERBOSE']='ERROR'", "+os.environ['RADICAL_SAGA_VERBOSE']='ERROR'", '+importwarnings', '+warnings.simplefilter(action="ignore")']]
    [2, 'inserted', ['+#severalmethodsexisttoaddadditionalderivedinformationtotherawdataframe.', '+#add_states:fillsoutmissingstateinformationwherethosecanbederived.', "+#italsoaddsa'state_from'columntoshowpreviousstatesontransitions", '+rpu.add_states(uf)', '+printuf.columns.values', '+printuf.dropna()[0:3]', '+', "+#add_infoaddsonemorecolumn,'info'(nameissubjecttochange),", '+#witheventsconsideredinterestinganduniversal', '+#namingscheme:asic_get_u:agent_staging_input_component:getunitfromqueue', '+rpu.add_info(uf)', '+printuf.columns.values', "+printuf['info'].unique()"]]
    [2, 'inserted', ['+', "+#basedonthe'info'entries,wecangetatransposedDFwhichthenisindexedbyunits,", '+#andthusisamenableforplottingoverunitIDs(wherethenon-transposedframesare', '+#allfocusedonplottingovertime)', '+idf=rpu.get_info_df(uf)', '+printsorted(list(idf.columns.values))', "+idf[['awo_get_u_pend','AgentStagingInputPending','usic_get_u','usic_adv_u_pend']][0:5]"]]
    [2, 'inserted', ['+#wecangetasimilartransposedframewhichonlycontainsstatetransitions', '+sdf=rpu.get_state_df(idf)', '+printsorted(list(sdf.columns.values))', '+sdf[0:5]']]
    [2, 'inserted', ['+#backtotheoriginaldataframe:letslookatsomedetail:', '+#herelookatallstateadvancingeventsforasingleunit', "+adv=uf[uf['event'].isin(['advance'])]", "+adv[adv['uid'].isin(['unit.000001'])][['time','state_from','state','info','name']]"]]


# Step 2: Convert nbdiff output into Cell-level mapping 

    example:
    ['0', '0m']
    ['1', '1']
    ['2', None]
    ['3', None]
    ['4', None]
    ['5', None]
    ['6', '8m']
    ['7', '12m']
    ['8', None]
    ['9', '13']
    [None, '2']
    [None, '3']
    [None, '4']
    [None, '5']
    [None, '6']
    [None, '7']
    [None, '9']
    [None, '10']
    [None, '11']

# Step 3: remove all the identical mapping cells 

    example:
    [0, '0m']
    [2, None]
    [3, None]
    [4, None]
    [5, None]
    [6, '8m']
    [None, 9]
    [None, 10]
    [None, 11]
    [7, '12m']
    [8, None]
    [None, 2]
    [None, 3]
    [None, 4]
    [None, 5]
    [None, 6]
    [None, 7]

# Step 4: collect all the reaminder lines in old versions and new versions

# Step 5: Using longest common subsequence algorith to find the lines-mapping

    example:
    [[6, 79], [8, 98]]
    [[6, 80], [8, 99]]
    [[6, 82], [8, 101]]
    [[6, 83], [8, 102]]
    [[6, 85], [8, 104]]
    [[6, 87], [8, 106]]
    [[7, 89], [9, 110]]
    [[7, 90], [12, 139]]
    [[7, 92], [12, 141]]
    [[7, 93], [12, 142]]
    [[7, 95], [12, 144]]
    [[7, 97], [12, 146]]
    [[7, 98], [12, 147]]
    [[7, 100], [12, 149]]
    [[7, 101], [12, 150]]
    [[7, 102], [12, 151]]

# Step 6: Count the lines mapping for each pairs 
# filter by count >= 2
# or by percentage

    example:
    0,0 14 22
    2,2 2 13
    2,3 3 7
    3,5 1 4
    4,7 3 10
    5,7 1 10
    6,8 24 35
    7,9 1 17
    7,12 9 17

# Step 7: format the rest ...