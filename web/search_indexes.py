from haystack import indexes
from web.document import Post

class PostIndex(indexes.SearchIndex,indexes.Indexable):
    body = indexes.CharField(document=True)
    post_id = indexes.IntegerField(model_attr= 'id')
    
    def get_model(self):
        return Post
    

