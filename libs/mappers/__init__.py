"""Mappers for various data types.

This module provides mappers for converting between DTOs and other representations
such as dictionaries, for different parts of the game.
"""
from .save import SaveMapper

from .entity import AttributeLayerEntityMapper
from .player import ClientPlayerMapper
from .connects import ConnectServerMapper, ConnectClientMapper, GameDataToServerMapper, GameDataToClientMapper
from .animator import AnimatorDataMapper

from .dimension import DimensionSaveMapper
from .map_block import MapBlockSaveMapper
from .map_chunk import MapChunkSaveMapper
from .map_plate import MapPlateSaveMapper

from .dimension import DimensionConfigMapper
from .map_block import MapBlockConfigMapper
from .map_chunk import MapChunkConfigMapper
from .map_plate import MapPlateConfigMapper

from .tile_map import TileMapMapper
