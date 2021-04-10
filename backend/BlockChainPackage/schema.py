from .Block import Block as BlockModel

import graphene
from graphene.relay import Node

from graphene_mongo import MongoengineObjectType

class BlockQuery(MongoengineObjectType):
    class Meta:
        model = BlockModel

class Query(graphene.ObjectType):
    blocks = graphene.List(BlockQuery)

    def resolve_blocks(self, info):
    	return list( BlockModel.objects.all() )

schema = graphene.Schema(query=Query, types=[BlockQuery])