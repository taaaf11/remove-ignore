from __future__ import annotations

import typing
from collections.abc import Callable

if typing.TYPE_CHECKING:
    from typing import TypeAlias

MatcherFunctionType: TypeAlias = Callable[[str], bool]
