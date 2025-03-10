from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto



class Axis(Enum):
    X = auto()
    Y = auto()

    
class Offset(Enum):
    POS = auto()
    NEG = auto()


def hemi_path(
    x_idx: float,
    y_idx: float,
    unit_px: float,
    axis: Axis,
    offset: Offset,
    flip: bool,
) -> str:

    # Radius of arc
    r = unit_px / 2
    
    # Define the start and end points at the top left (x_idx, y_idx).
    ix = fx = x_idx
    iy = fy = y_idx
    
    # Offset starting point based on axis.
    if offset == Offset.POS:
        match axis:
            case Axis.X:
                iy += r
                fy += r
            case Axis.Y:
                ix += r
                fx += r
                
    # Offset starting point based on flip.
    if flip:
        match axis:
            case Axis.X:
                ix += r
                fx += r
            case Axis.Y:
                iy += r
                fy += r
                
    # Finally, move the final point
    match axis:
        case Axis.X:
            fx += unit_px
        case Axis.Y:
            fy += unit_px
    
    # If flipped, sweep in opposite direction
    sweep = int(flip)
    
    return f'M {ix} {iy} A {r} {r} 0 0 {sweep} {fx} {fy} Z'
    



@dataclass
class Unit(ABC):
    
    x: float
    y: float
    unit_px: float
    
    
    @abstractmethod
    def draw(
        cls,
        x_idx: float,
        y_idx: float,
        
    ) -> None:
        pass


@dataclass
class CircleUnit(Unit):
    
    def draw(
        cls,
        x_idx: float,
        y_idx: float,
    ) -> None:
        pass

