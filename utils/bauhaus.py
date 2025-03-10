from functools import cached_property
from dataclasses import dataclass
from lxml import etree, builder
from pathlib import Path
import paths, units


# Initialize some SVG objects
e = builder.ElementMaker()


@dataclass
class Bauhaus:
    
    """
    frame: the total image
    box: the container of the units
    buffer: the top, left, right spacing between frame and box.
    """
    
    
    frame_width_in: float
    frame_height_in: float
    unit_dim_in: float
    unit_x: int
    unit_y: int
    
    color_background: str
    
    file_name: str
    
    dpi: float = 300
    file_dir: Path = paths.output_dir
    
    
    def __post_init__(self) -> None:
        
        # Make the SVG object
        self.doc = e.svg(
            xmlns='http://www.w3.org/2000/svg',
            height=str(self.frame_height_px),
            width=str(self.frame_width_px),
        )
        
    @cached_property
    def frame_width_px(self) -> float:
        return self.frame_width_in * self.dpi
    
    @cached_property
    def frame_height_px(self) -> float:
        return self.frame_height_in * self.dpi
    
    @cached_property
    def unit_dim_px(self) -> float:
        return self.unit_dim_in * self.dpi
    
    @cached_property
    def box_width_px(self) -> float:
        return self.unit_x * self.unit_dim_px
    
    @cached_property
    def box_height_px(self) -> float:
        return self.unit_y * self.unit_dim_px
    
    @cached_property
    def buffer_px(self) -> float:
        return (self.frame_width_px - self.box_width_px) / 2
    
    @cached_property
    def box_x_min_px(self) -> float:
        return self.buffer_px
    
    @cached_property
    def box_x_max_px(self) -> float:
        return self.buffer_px + self.box_width_px
    
    @cached_property
    def box_y_min_px(self) -> float:
        return self.buffer_px
    
    @cached_property
    def box_y_max_px(self) -> float:
        return self.buffer_px + self.box_height_px
    
    
    
    
    def _draw(self) -> None:
                
        # Background
        self.doc.append(
            e.rect(
                x='0',
                y='0',
                width=str(self.frame_width_px),
                height=str(self.frame_height_px),
                fill=self.color_background,
            )
        )
        
        path_str = units.hemi_path(
            x_idx=1,
            y_idx=1,
            unit_px=self.unit_dim_px,
            axis=units.Axis.Y,
            offset=True,
            invert=True,
        )
        
        print(path_str)
        self.doc.append(
            e.path(
                d=path_str,
                fill='red',
            )
        )

        
        
    def _save(self) -> None:
        
        with open(self.file_dir / f'{self.file_name}.svg', 'wb') as f:
            f.write(etree.tostring(self.doc, pretty_print=True))
            
        
    def run(self) -> None:
        
        self._draw()
        self._save()
    


if __name__ == '__main__':
    b = Bauhaus(
        frame_width_in=2,
        frame_height_in=2,
        unit_dim_in=1,
        unit_x=16,
        unit_y=16,
        color_background='#E6E0CE',
        file_name='bauhaus',
        dpi=100
    )
    b.run()