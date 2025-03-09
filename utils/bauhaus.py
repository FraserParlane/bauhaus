from functools import cached_property
from dataclasses import dataclass
from lxml import etree, builder
from pathlib import Path
import paths


# Initialize some SVG objects
e = builder.ElementMaker()


@dataclass
class Bauhaus:
    frame_width_in: float
    frame_height_in: float
    unit_edge_in: float
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
    def frame_width_px(self) -> int:
        return self.frame_width_in * self.dpi
    
    @cached_property
    def frame_height_px(self) -> int:
        return self.frame_height_in * self.dpi
    
    
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
        
    def _save(self) -> None:
        
        with open(self.file_dir / f'{self.file_name}.svg', 'wb') as f:
            f.write(etree.tostring(self.doc, pretty_print=True))
        
    def run(self) -> None:
        
        self._draw()
        self._save()
    


if __name__ == '__main__':
    b = Bauhaus(
        frame_width_in=8 * 12,
        frame_height_in=3 * 12,
        unit_edge_in=2,
        unit_x=16,
        unit_y=16,
        color_background='#ccddaa',
        file_name='bauhaus',
    )
    b.run()