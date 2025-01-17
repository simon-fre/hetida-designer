"""Component entrypoint registration utilities"""

import asyncio
import functools
from typing import Callable, Dict, Optional

from hetdesrun.component.load import ComponentCodeImportError
from hetdesrun.datatypes import DataType


class ComponentEntryPointRegistrationError(ComponentCodeImportError):
    pass


# pylint: disable=redefined-builtin
def register(
    *,
    inputs: Dict[str, DataType],
    outputs: Dict[str, DataType],
    name: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    id: Optional[str] = None,
    revision_group_id: Optional[str] = None,
    version_tag: Optional[str] = None,
    state: Optional[str] = None,
    released_timestamp: Optional[str] = None,
    disabled_timestamp: Optional[str] = None,
    is_pure_plot_component: Optional[bool] = None  # pylint: disable=unused-argument
) -> Callable[[Callable], Callable]:
    """Additonal features for component entrypoint functions

    This decorator can be used to provide additional features for component entrypoint
    functions which may depend on datatype infos on the inputs and outputs.

    is_pure_plot_component: This is deprecated and only exists for backwards compatibility,
    but it is ignored.
    """

    def wrapper_func(func: Callable) -> Callable:

        if not asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            def return_func_or_coro(*args, **kwargs):  # type: ignore

                return func(*args, **kwargs)

        else:

            @functools.wraps(func)
            async def return_func_or_coro(*args, **kwargs):  # type: ignore

                return await func(*args, **kwargs)

        # add input output infos to function attributes
        return_func_or_coro.inputs = inputs  # type: ignore
        return_func_or_coro.outputs = outputs  # type: ignore
        return_func_or_coro.registered_metadata = {  # type: ignore
            "inputs": inputs,
            "outputs": outputs,
            "name": name,
            "description": description,
            "category": category,
            "version_tag": version_tag,
            "id": id,
            "revision_group_id": revision_group_id,
            "state": state,
            "released_timestamp": released_timestamp,
            "disabled_timestamp": disabled_timestamp,
        }

        return return_func_or_coro

    return wrapper_func
