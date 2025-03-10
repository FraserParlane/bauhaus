from abc import ABC, abstractmethod
from typing import Literal, Tuple
from dataclasses import dataclass
from enum import Enum, auto


class Axis(Enum):
    X = auto()
    Y = auto()


def hemi_path(
    x_idx: float,
    y_idx: float,
    unit_px: float,
    axis: Axis,
    offset: bool,
    invert: bool,
) -> str:
    """Generate a CSS string that describes a closed hemispherical arc,
    enscribed in the unit square (unit_px, unit_px).

    x positive is left to right
    y positive is top to bottom

    Args:
        x_idx (float): The left-most value.
        y_idx (float): The top-most value.
        unit_px (float): The dimensions of the unit square.
        axis (Axis): The axis the flat edge of the hemisphere is parallel to.
        offset (bool): If offset, then hemisphere is drawn in right or lower
        half of unit box.
        invert (bool): If False, arc of hemisphere aligns with nominal circle in
        box. If True, mirror image.

    Returns:
        str: _description_
    """

    # Radius of arc
    r = unit_px / 2
    
    # Define the start and end points at the top left (x_idx, y_idx).
    ix = fx = x_idx
    iy = fy = y_idx
    
    # Move the final point
    match axis:
        case Axis.X:
            fx += unit_px
        case Axis.Y:
            fy += unit_px
    
    # Determine if sweep or not
    sweep = False
    match axis:
        case Axis.X:
            if (not offset) ^ invert:
                sweep = True
        case Axis.Y:
            if (not offset) == invert:
                sweep = True
        
    
    # Offset starting point based on axis.
    if offset:
        match axis:
            case Axis.X:
                iy += r
                fy += r
            case Axis.Y:
                ix += r
                fx += r
                
    # Offset starting point based on flip.
    if invert == offset:
        match axis:
            case Axis.X:
                iy += r
                fy += r
            case Axis.Y:
                ix += r
                fx += r
                

    return f'M {ix} {iy} A {r} {r} 0 0 {int(sweep)} {fx} {fy} Z'
    



@dataclass
class Unit(ABC):
    
    x_idx: float
    y_idx: float
    unit_px: float
    
    
    @abstractmethod
    def draw() -> Tuple[str]:
        pass
    
    @abstractmethod
    def width(self) -> float:
        pass
    
    def hemi_path(
        self,
        axis: Axis,
        offset: Offset,
        flip: bool,
    ) -> str:
        
        return hemi_path(
            x_idx=self.x_idx,
            y_idx=self.y_idx,
            unit_px=self.width,
            axis=axis,
            offset=offset,
            invert=flip,
        )
    

class HalfUnit(Unit):

    @property
    def width(self) -> float:
        return self.unit_px / 2
    

class FullUnit(Unit):

    @property
    def width(self) -> float:
        return self.unit_px


class HalfXNeg(HalfUnit):
    
    def draw(self) -> Tuple[str]:
        
        return (
            self.hemi_path(
                axis=Axis.X,
                offset=Offset.NEG,
                flip=False,
            ),
        )
        
class HalfXPos(HalfUnit):
    
    def draw(self) -> Tuple[str]:
        
        return (
            self.hemi_path(
                axis=Axis.X,
                offset=Offset.POS,
                flip=False,
            ),
        )
        

class FullXInv(FullUnit):
    
    def draw(self) -> Tuple[str]:
    
        return (
            self.hemi_path(
                axis=Axis.X,
                offset=Offset.NEG,
                flip=False,
            ),
            self.hemi_path(
                axis=Axis.X,
                offset=Offset.NEG,
                flip=False,
            ),
        )



class CircleUnit(FullUnit):
    
    def draw(
        cls,
        x_idx: float,
        y_idx: float,
    ) -> Tuple[str]:
        pass



VALID_UNITS = Literal[
    HalfXNeg,
    HalfXPos,
    FullXInv,
    
]