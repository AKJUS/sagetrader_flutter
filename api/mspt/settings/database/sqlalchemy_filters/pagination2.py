import math
from collections import namedtuple
from starlette.requests import Request

from .exceptions import InvalidPage

req =  Request


def apply_pagination(query, *, page_number=None, page_size=None, request):
    total_results = query.count()
    query = _limit(query, page_size)

    # Page size defaults to total results
    if page_size is None or (page_size > total_results and total_results > 0):
        page_size = total_results

    # Page number defaults to 1
    if page_number is None or page_number < 1:
        page_number = 1

    query = _offset(query, page_number, page_size)

    num_pages = _calculate_num_pages(page_number, page_size, total_results)
    
    next_url = _get_next(request.url, page_number, page_size, num_pages)
    prev_url = _get_prev(request.url, page_number, page_size)
        
    return {
        'count': total_results, 
        'page': page_number, 
        'items': query, 
        'pages': num_pages, 
        'size': page_size, 
        'next_url': next_url,
        'prev_url': prev_url,
        }


def _get_prev(url, page, size):
    _minus_query_params = str(url).split('?')[0]
    
    if page == 1:
        return None
    
    return f"{_minus_query_params}?page={page-1}&size={size}"

def _get_next(url, page, size, pages):
    _minus_query_params = str(url).split('?')[0]
    
    if page >= pages:
        return None
    
    return f"{_minus_query_params}?page={page+1}&size={size}"
    

def _limit(query, page_size):
    if page_size is not None:
        if page_size < 0:
            raise InvalidPage(
                'Page size should not be negative: {}'.format(page_size)
            )

        query = query.limit(page_size)

    return query


def _offset(query, page_number, page_size):
    query = query.offset((page_number - 1) * page_size)
    return query


def _calculate_num_pages(page_number, page_size, total_results):
    if page_size == 0:
        return 0

    return math.ceil(float(total_results) / float(page_size))