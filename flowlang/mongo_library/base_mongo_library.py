from ..core import ExecutableNode, VarParam, Variable
from ..library import register_type


from pymongo import MongoClient
from bson import ObjectId


@register_type
class MakeMongoClient(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'address': VarParam('str', str, str())
            },
            output_params =
            {
                'client': VarParam('client', object, None)
            })

    def _execute(self, **kwargs):
        address = self.get_input_value('address').get_value()
        self.output_values['client'].set_value(MongoClient(address))


@register_type
class GetDatabaseByName(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'client': VarParam('client', object, None),
                'name': VarParam('str', str, str())
            },
            output_params =
            {
                'db': VarParam('db', object, None)
            })

    def _execute(self, **kwargs):
        client = self.get_input_value('client').get_value()
        name = self.get_input_value('name').get_value()
        self.output_values['db'].set_value(client[name])


@register_type
class GetCollectionByName(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'db': VarParam('db', object, None),
                'name': VarParam('str', str, str())
            },
            output_params =
            {
                'collection': VarParam('collection', object, None)
            })

    def _execute(self, **kwargs):
        db = self.get_input_value('db').get_value()
        name = self.get_input_value('name').get_value()
        self.output_values['collection'].set_value(db[name])


@register_type
class ClearCollection(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'collection': VarParam('collection', object, None)
            })

    def _execute(self, **kwargs):
        collection = self.get_input_value('collection').get_value()
        collection.drop()


@register_type
class InsertOneDocument(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'collection': VarParam('collection', object, None),
                'document': VarParam('document', dict, {})
            })

    def _execute(self, **kwargs):
        collection = self.get_input_value('collection').get_value()
        document = self.get_input_value('document').get_value()
        collection.insert_one(document)


@register_type
class InsertManyDocuments(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'collection': VarParam('collection', object, None),
                'documents': VarParam('documents', list, [])
            })

    def _execute(self, **kwargs):
        collection = self.get_input_value('collection').get_value()
        documents = self.get_input_value('documents').get_value()
        collection.insert_many(documents)

@register_type
class DeleteOneDocument(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'collection': VarParam('collection', object, None),
                'document': VarParam('document', dict, {})
            })

    def _execute(self, **kwargs):
        collection = self.get_input_value('collection').get_value()
        document = self.get_input_value('document').get_value()
        collection.delete_one(document)


@register_type
class DeleteManyDocuments(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'collection': VarParam('collection', object, None),
                'documents': VarParam('documents', list, [])
            })

    def _execute(self, **kwargs):
        collection = self.get_input_value('collection').get_value()
        documents = self.get_input_value('documents').get_value()
        collection.delete_many(documents)

@register_type
class FindDocuments(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'collection': VarParam('collection', object, None),
                'params': VarParam('params', dict, {})
            },
            output_params={
                'objects': VarParam('objects', list, [])
            })

    def _execute(self, **kwargs):
        collection = self.get_input_value('collection').get_value()
        params = self.get_input_value('params').get_value()
        result = list(collection.find(params))
        self.get_output_value('objects').set_value(result)


@register_type
class FindDocuments2(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'collection': VarParam('collection', object, None),
                'params': VarParam('params', dict, {}),
                'skip': VarParam('skip', int, 0),
                'limit': VarParam('limit', dict, 1)
            },
            output_params={
                'objects': VarParam('objects', list, [])
            })

    def _execute(self, **kwargs):
        collection = self.get_input_value('collection').get_value()
        params = self.get_input_value('params').get_value()
        skip = self.get_input_value('skip').get_value()
        limit = self.get_input_value('limit').get_value()
        result = list(collection.find(params).skip(skip).limit(limit))
        self.get_output_value('objects').set_value(result)