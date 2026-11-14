#!/usr/bin/env python3
"""
SAM Video Series - Slide Generator
Converts YAML content definitions to styled PowerPoint presentations.
"""

import yaml
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import copy

# ─── Color Palette ───
COLORS = {
    'sn_green': RGBColor(0x00, 0x6B, 0x3F),      # ServiceNow green
    'sn_green_light': RGBColor(0x00, 0x9B, 0x5A),
    'dark_slate': RGBColor(0x1E, 0x2A, 0x3A),
    'medium_slate': RGBColor(0x2D, 0x3E, 0x50),
    'light_slate': RGBColor(0x3D, 0x4E, 0x60),
    'white': RGBColor(0xFF, 0xFF, 0xFF),
    'off_white': RGBColor(0xF8, 0xF9, 0xFA),
    'accent_orange': RGBColor(0xE6, 0x7E, 0x22),
    'accent_red': RGBColor(0xE7, 0x4C, 0x3C),
    'accent_blue': RGBColor(0x34, 0x98, 0xDB),
    'accent_yellow': RGBColor(0xF3, 0x9C, 0x12),
    'text_primary': RGBColor(0x1E, 0x2A, 0x3A),
    'text_secondary': RGBColor(0x5D, 0x6D, 0x7E),
    'code_bg': RGBColor(0x2C, 0x3E, 0x50),
}

# ─── Slide Dimensions (16:9) ───
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)
MARGIN = Inches(0.6)
CONTENT_WIDTH = SLIDE_WIDTH - 2 * MARGIN

# ─── Font Settings ───
FONTS = {
    'title': ('Inter', Pt(44), True),
    'subtitle': ('Inter', Pt(24), False),
    'section_title': ('Inter', Pt(32), True),
    'body': ('Source Sans Pro', Pt(22), False),
    'body_bold': ('Source Sans Pro', Pt(22), True),
    'bullet': ('Source Sans Pro', Pt(20), False),
    'bullet_bold': ('Source Sans Pro', Pt(20), True),
    'code': ('JetBrains Mono', Pt(16), False),
    'small': ('Source Sans Pro', Pt(16), False),
    'caption': ('Source Sans Pro', Pt(14), False),
    'mnemonic': ('JetBrains Mono', Pt(18), True),
}

class SlideGenerator:
    def __init__(self, template_path=None):
        self.prs = Presentation()
        self.prs.slide_width = SLIDE_WIDTH
        self.prs.slide_height = SLIDE_HEIGHT
        self.slide_layouts = self._create_custom_layouts()
        
    def _create_custom_layouts(self):
        """Create blank layouts we'll build programmatically."""
        # Use blank layout (index 6) as base
        return {'blank': 6}
    
    def _add_background(self, slide, color=COLORS['dark_slate']):
        """Set slide background color."""
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color
    
    def _add_shape(self, slide, left, top, width, height, fill_color=None, line_color=None):
        """Add a rectangle shape."""
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        shape.line.fill.background()
        if fill_color:
            shape.fill.solid()
            shape.fill.fore_color.rgb = fill_color
        else:
            shape.fill.background()
        return shape
    
    def _add_textbox(self, slide, left, top, width, height, text, font_key='body', 
                     color=COLORS['white'], alignment=PP_ALIGN.LEFT, line_spacing=1.15):
        """Add a text box with formatting."""
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.name, p.font.size, p.font.bold = FONTS[font_key]
        p.font.color.rgb = color
        p.alignment = alignment
        p.space_after = Pt(0)
        # line_spacing in points, not EMU
        p.line_spacing = Pt(p.font.size.pt * line_spacing)
        return txBox
    
    def _add_multiline_textbox(self, slide, left, top, width, height, lines, 
                                font_key='body', color=COLORS['white'], 
                                alignment=PP_ALIGN.LEFT, line_spacing=1.2,
                                highlight_words=None, highlight_color=COLORS['accent_yellow']):
        """Add textbox with multiple paragraphs, optional word highlighting."""
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        
        for i, line in enumerate(lines):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.space_after = Pt(6)
            p.line_spacing = Pt(FONTS[font_key][1].pt * line_spacing)
            
            if highlight_words and any(hw in line for hw in highlight_words):
                # Split line and highlight
                parts = line.split()
                for part in parts:
                    run = p.add_run()
                    run.text = part + ' '
                    run.font.name, run.font.size, run.font.bold = FONTS[font_key]
                    if any(hw.lower() in part.lower() for hw in highlight_words):
                        run.font.color.rgb = highlight_color
                        run.font.bold = True
                    else:
                        run.font.color.rgb = color
            else:
                run = p.add_run()
                run.text = line
                run.font.name, run.font.size, run.font.bold = FONTS[font_key]
                run.font.color.rgb = color
            p.alignment = alignment
        return txBox
    
    def _add_bullet_list(self, slide, left, top, width, height, bullets, 
                          font_key='bullet', color=COLORS['white'], spacing=Pt(8)):
        """Add a bulleted list."""
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        
        for i, bullet in enumerate(bullets):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = f"▸  {bullet}"
            p.font.name, p.font.size, p.font.bold = FONTS[font_key]
            p.font.color.rgb = color
            p.space_after = spacing
            p.level = 0
        return txBox
    
    def _add_table(self, slide, left, top, width, height, headers, rows, 
                    highlight_row=None, font_key='body'):
        """Add a formatted table."""
        table_shape = slide.shapes.add_table(len(rows) + 1, len(headers), left, top, width, height)
        table = table_shape.table
        
        # Set column widths evenly
        col_width = int(width / len(headers))
        for col in table.columns:
            col.width = col_width
        
        # Header row
        for j, header in enumerate(headers):
            cell = table.cell(0, j)
            cell.text = header
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.name, paragraph.font.size, paragraph.font.bold = FONTS['body_bold']
                paragraph.font.color.rgb = COLORS['white']
                paragraph.alignment = PP_ALIGN.CENTER
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLORS['sn_green']
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        # Data rows
        for i, row in enumerate(rows):
            row_idx = i + 1
            is_highlight = (highlight_row is not None and row_idx == highlight_row)
            for j, cell_text in enumerate(row):
                cell = table.cell(row_idx, j)
                cell.text = str(cell_text)
                for paragraph in cell.text_frame.paragraphs:
                    paragraph.font.name, paragraph.font.size, paragraph.font.bold = FONTS[font_key]
                    paragraph.font.color.rgb = COLORS['white'] if not is_highlight else COLORS['dark_slate']
                    paragraph.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
                if is_highlight:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = COLORS['accent_yellow']
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = COLORS['medium_slate'] if i % 2 == 0 else COLORS['light_slate']
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        return table_shape
    
    def _add_accent_bar(self, slide, left, top, width, height, color=COLORS['sn_green']):
        """Add a thin accent bar."""
        return self._add_shape(slide, left, top, width, height, fill_color=color)
    
    def _add_video_number(self, slide, number):
        """Add video number badge in corner."""
        badge = self._add_shape(
            slide, 
            SLIDE_WIDTH - Inches(1.2), Inches(0.3), 
            Inches(0.9), Inches(0.5), 
            fill_color=COLORS['sn_green']
        )
        tf = badge.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = f"#{number}"
        p.font.name, p.font.size, p.font.bold = ('Inter', Pt(18), True)
        p.font.color.rgb = COLORS['white']
        p.alignment = PP_ALIGN.CENTER
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # ─── Slide Type Builders ───
    
    def build_title_slide(self, slide, data):
        self._add_background(slide)
        
        # Top accent bar
        self._add_accent_bar(slide, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.08))
        
        # Title
        self._add_textbox(slide, MARGIN, Inches(1.5), CONTENT_WIDTH, Inches(1.5),
                          data['text'], 'title', COLORS['white'], PP_ALIGN.CENTER)
        
        # Subtitle
        if data.get('subtitle'):
            self._add_textbox(slide, MARGIN, Inches(3.0), CONTENT_WIDTH, Inches(1.0),
                              data['subtitle'], 'subtitle', COLORS['sn_green_light'], PP_ALIGN.CENTER)
        
        # Bottom accent bar
        self._add_accent_bar(slide, Inches(0), SLIDE_HEIGHT - Inches(0.08), SLIDE_WIDTH, Inches(0.08))
        
        if data.get('show_number'):
            self._add_video_number(slide, data.get('number', 1))
    
    def build_statement_slide(self, slide, data):
        self._add_background(slide)
        self._add_accent_bar(slide, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.06))
        
        # Parse emphasis words
        emphasis = data.get('emphasis', '').split(', ')
        
        self._add_multiline_textbox(slide, MARGIN, Inches(1.5), CONTENT_WIDTH, Inches(4.5),
                                     data['text'].strip().split('\n'), 'body', COLORS['white'],
                                     PP_ALIGN.CENTER, 1.4, emphasis, COLORS['accent_yellow'])
        
        self._add_accent_bar(slide, Inches(0), SLIDE_HEIGHT - Inches(0.06), SLIDE_WIDTH, Inches(0.06))
    
    def build_definition_slide(self, slide, data):
        self._add_background(slide)
        self._add_accent_bar(slide, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.06))
        
        # Title
        self._add_textbox(slide, MARGIN, Inches(0.5), CONTENT_WIDTH, Inches(0.8),
                          data.get('title', ''), 'section_title', COLORS['sn_green_light'], PP_ALIGN.CENTER)
        
        # Definition text
        emphasis = data.get('highlight', '').split(', ')
        self._add_multiline_textbox(slide, MARGIN, Inches(1.5), CONTENT_WIDTH, Inches(4.5),
                                     data['text'].strip().split('\n'), 'body', COLORS['white'],
                                     PP_ALIGN.CENTER, 1.3, emphasis, COLORS['accent_yellow'])
        
        self._add_accent_bar(slide, Inches(0), SLIDE_HEIGHT - Inches(0.06), SLIDE_WIDTH, Inches(0.06))
    
    def build_comparison_slide(self, slide, data):
        self._add_background(slide)
        self._add_accent_bar(slide, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.06))
        
        # Title
        self._add_textbox(slide, MARGIN, Inches(0.3), CONTENT_WIDTH, Inches(0.7),
                          data.get('title', ''), 'section_title', COLORS['sn_green_light'], PP_ALIGN.CENTER)
        
        # Highlight row text
        highlight_text = data.get('highlight_text', '')
        if highlight_text:
            self._add_textbox(slide, MARGIN, Inches(1.0), CONTENT_WIDTH, Inches(0.5),
                              highlight_text, 'caption', COLORS['accent_yellow'], PP_ALIGN.CENTER)
        
        # Table
        table_top = Inches(1.5) if not highlight_text else Inches(1.7)
        self._add_table(slide, MARGIN, table_top, CONTENT_WIDTH, Inches(4.5),
                        data['headers'], data['rows'],
                        highlight_row=data.get('highlight_row'))
        
        self._add_accent_bar(slide, Inches(0), SLIDE_HEIGHT - Inches(0.06), SLIDE_WIDTH, Inches(0.06))
    
    def build_diagram_slide(self, slide, data):
        self._add_background(slide)
        self._add_accent_bar(slide, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.06))
        
        # Title
        self._add_textbox(slide, MARGIN, Inches(0.3), CONTENT_WIDTH, Inches(0.7),
                          data.get('title', ''), 'section_title', COLORS['sn_green_light'], PP_ALIGN.CENTER)
        
        # Main chain text
        self._add_textbox(slide, MARGIN, Inches(1.2), CONTENT_WIDTH, Inches(1.0),
                          data['text'].split('\n')[0], 'body_bold', COLORS['white'], PP_ALIGN.CENTER)
        
        # Mnemonic breakdown
        if data.get('mnemonic'):
            self._add_textbox(slide, MARGIN, Inches(2.3), CONTENT_WIDTH, Inches(3.5),
                              data['mnemonic'], 'mnemonic', COLORS['accent_yellow'], PP_ALIGN.CENTER)
        
        self._add_accent_bar(slide, Inches(0), SLIDE_HEIGHT - Inches(0.06), SLIDE_WIDTH, Inches(0.06))
    
    def build_key_concept_slide(self, slide, data):
        self._add_background(slide)
        self._add_accent_bar(slide, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.06))
        
        # Title
        self._add_textbox(slide, MARGIN, Inches(0.3), CONTENT_WIDTH, Inches(0.7),
                          data.get('title', ''), 'section_title', COLORS['sn_green_light'], PP_ALIGN.CENTER)
        
        # Bullets
        self._add_bullet_list(slide, MARGIN, Inches(1.3), CONTENT_WIDTH, Inches(4.0),
                              data['bullets'], 'bullet', COLORS['white'], Pt(10))
        
        # Rule/emphasis at bottom
        if data.get('rule'):
            self._add_textbox(slide, MARGIN, Inches(5.5), CONTENT_WIDTH, Inches(1.0),
                              data['rule'], 'caption', COLORS['accent_orange'], PP_ALIGN.CENTER)
        
        self._add_accent_bar(slide, Inches(0), SLIDE_HEIGHT - Inches(0.06), SLIDE_WIDTH, Inches(0.06))
    
    def build_next_video_slide(self, slide, data):
        self._add_background(slide)
        self._add_accent_bar(slide, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.06))
        
        # "Next Video" label
        self._add_textbox(slide, MARGIN, Inches(2.0), CONTENT_WIDTH, Inches(0.6),
                          "NEXT UP", 'caption', COLORS['sn_green_light'], PP_ALIGN.CENTER)
        
        # Next video title
        self._add_textbox(slide, MARGIN, Inches(2.8), CONTENT_WIDTH, Inches(1.5),
                          data['text'], 'body_bold', COLORS['white'], PP_ALIGN.CENTER)
        
        # Video number
        if data.get('next_video'):
            self._add_textbox(slide, MARGIN, Inches(4.5), CONTENT_WIDTH, Inches(1.0),
                              f"Video #{data['next_video']}", 'title', COLORS['accent_yellow'], PP_ALIGN.CENTER)
        
        self._add_accent_bar(slide, Inches(0), SLIDE_HEIGHT - Inches(0.06), SLIDE_WIDTH, Inches(0.06))
    
    def generate_from_yaml(self, yaml_path, output_path):
        """Main entry point: load YAML and generate PPTX."""
        with open(yaml_path, 'r') as f:
            content = yaml.safe_load(f)
        
        meta = content['meta']
        slides_data = content['slides']
        
        # Map slide types to builders
        builders = {
            'title': self.build_title_slide,
            'statement': self.build_statement_slide,
            'definition': self.build_definition_slide,
            'comparison_table': self.build_comparison_slide,
            'diagram_placeholder': self.build_diagram_slide,
            'key_concept': self.build_key_concept_slide,
            'next_video': self.build_next_video_slide,
        }
        
        for i, slide_data in enumerate(slides_data):
            slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])  # Blank layout
            slide_type = slide_data['type']
            
            if slide_type in builders:
                builders[slide_type](slide, slide_data)
            else:
                print(f"Warning: Unknown slide type '{slide_type}' at slide {i+1}")
            
            # Add video number to all slides
            self._add_video_number(slide, meta.get('number', 1))
        
        # Save
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(str(output_path))
        print(f"Generated: {output_path} ({len(slides_data)} slides)")
        return output_path


def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python generate_slides.py <input.yaml> <output.pptx>")
        sys.exit(1)
    
    generator = SlideGenerator()
    generator.generate_from_yaml(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()