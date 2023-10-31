from typing import Awaitable, cast

from asgiref.sync import iscoroutinefunction, sync_to_async
from django.utils.decorators import sync_and_async_middleware
from whitenoise.middleware import WhiteNoiseMiddleware


@sync_and_async_middleware
def whitenoise_middleware(get_response):
    mid = WhiteNoiseMiddleware(get_response)

    def get_static_file(request):
        # This is copied from WhiteNoiseMiddleware.__call__
        if mid.autorefresh:
            static_file = mid.find_file(request.path_info)
        else:
            static_file = mid.files.get(request.path_info)

        return mid.serve(static_file, request) if static_file is not None else None

    if iscoroutinefunction(get_response):
        aget_static_file = sync_to_async(get_static_file, thread_sensitive=False)

        async def middleware(request):  # type: ignore
            response = await aget_static_file(request)
            if response is not None:
                return response

            return await cast(Awaitable, get_response(request))

    else:

        def middleware(request):
            response = get_static_file(request)
            if response is not None:
                return response

            return get_response(request)

    return middleware
