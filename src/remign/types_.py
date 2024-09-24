from __future__ import annotations

import typing
from collections.abc import Callable
from os import PathLike

if typing.TYPE_CHECKING:
    from typing import TypeAlias

StrOrPathLike: TypeAlias = str | PathLike
MatcherFunctionType: TypeAlias = Callable[[StrOrPathLike], bool]
