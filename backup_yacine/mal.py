import logging

import maltoolbox
from maltoolbox.language import classes_factory
from maltoolbox.language import specification, LanguageGraph
from maltoolbox import attackgraph
from maltoolbox.model import Model
from maltoolbox.ingestors import neo4j
from maltoolbox.attackgraph import AttackGraph


from os import path

exp = "exp5"

logger = logging.getLogger(__name__)

lang = path.join('langs','lang_spec.json')
model_path = path.join(exp,'model.json')

tmp = path.join(exp, 'tmp','attack_graph.json')

lang_spec = specification.load_language_specification_from_json(lang)

lang_classes_factory = classes_factory.LanguageClassesFactory(lang_spec)
lang_classes_factory.create_classes()

lang_graph = LanguageGraph(lang_spec)

model = Model("Test Model", lang_spec, lang_classes_factory)
model.load_from_file(model_path)



attack_graph = AttackGraph(lang_spec, model)
attack_graph.attach_attackers(model)
attack_graph.save_to_file(tmp)

'''
if maltoolbox.neo4j_configs['uri'] != "":
    neo4j.ingest_model(model,
        maltoolbox.neo4j_configs['uri'],
        maltoolbox.neo4j_configs['username'],
        maltoolbox.neo4j_configs['password'],
        maltoolbox.neo4j_configs['dbname'],
        delete=True)
'''
