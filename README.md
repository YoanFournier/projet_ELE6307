Projet ELE6307 H22 : Analyse energétique d'un processeur vectoriel pour des calculs de DNN

Ce projet utilise le framework Timeloop/Accelergy afin d'analyser l'éfficacité énergétique d'un processeur vectoriel basé sur l'architecture du coprocesseur RISCV vectoriel ARA.

La structure du repo est la suivante:

src/ : Contient l'ensemble des fichiers sources utilisés

  arch/ : Contient l'architecture du processeur vectoriel
  
  map/ : Contient le mapper de Timeloop
  
  mapping/ : Contient des mappings custom
  
  output_22nm/ : Contient les résultats pour 22 nm
  
  output_45nm/ : Contient les résultats pour 45 nm
  
  output_custom_mapping/ : Contient les résultats pour les mappings customs
  
  prob/ : Contient les problèmes (VGG et AlexNet)
  
  graphs.py : Script pour générer les graphiques de résultats
  
  map_and_save.py : Script pour générer les mapping avec Timeloop

tex_final : Fichiers source du rapport final

tex_intermediate : Fichiers source du rapport intermédiaire

tex_proposition : Fichiers souce de la proposition
