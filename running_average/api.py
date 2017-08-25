import urllib
from google.cloud.ml.util import _api
from google.cloud.ml.util import _http

# TODO(jlewi): This code should move into the sdk.
class ApiV3Modified(_api.ApiV3):
  
  def delete_model(self, model_name):
    """Delete the specified model."""
    url = '{0}/projects/{1}/models/{2}?'.format(self._endpoint, self._project_id,
                                                model_name)
    data = None
    return _http._Http.request(url, data=data, method="DELETE", credentials=self._credentials)

  def models_list(self, page_token=None, page_size=None):
    """List the models."""
    url = '{0}/projects/{1}/models'.format(self._endpoint, self._project_id)
    url_args = []
    if page_token:
      url_args.append(("pageToken", page_token))
    
    if page_size: 
      url_args.append(("pageSize", page_size))
      
    if url_args:
      url += "?" + urllib.encode(url_args)
   
    return _http._Http.request(url, credentials=self._credentials)
    
  def models_versions_list(self, model_name, page_token=None, page_size=None):
    """List the models."""
    url = '{0}/projects/{1}/models/{2}/versions'.format(self._endpoint, self._project_id, 
        model_name)
    url_args = []
    if page_token:
      url_args.append(("pageToken", page_token))
    
    if page_size: 
      url_args.append(("pageSize", page_size))
      
    if url_args:
      url += "?" + urllib.encode(url_args)
   
    print "url: {0}".format(url)
    return _http._Http.request(url, credentials=self._credentials)