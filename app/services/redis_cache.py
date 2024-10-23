import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)
CACHE_EXPIRY = 60 * 5  # 5 minutes

def convert_objectid_to_str(paper_data):
    if '_id' in paper_data:
        paper_data['_id'] = str(paper_data['_id'])
    return paper_data

def get_cached_paper(paper_id):
    cached_paper = redis_client.get(paper_id)
    if cached_paper:
        return json.loads(cached_paper)
    return None

def set_cached_paper(paper_id, paper_data):
    # import pdb; pdb.set_trace()
    paper_data = convert_objectid_to_str(paper_data)
    redis_client.set(paper_id, json.dumps(paper_data), ex=CACHE_EXPIRY)
