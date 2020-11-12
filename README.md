# Datamining_for_ligands


Datamining and ranking of nanoparticle ligands for antiviral properties

The purpose of this notebook is to scrape the literature for references to nanoparticles, look in those articles for mentions of coordinating solvents, ligands, surfactants etc. Those chemicals will then be associated with a CIDS number, a SMILES formula, and then that SMILES will be turned into a 3D structure. That 3D structure will be docked with the spike glycoprotein of the Sars-COV-2 virus, which and the dockings will be scored. These scores will tell us the best ligands to coat nanoparticles with so that the nanoparticles bind effectively with the virus, and they can deactivate the virus.
