from pptx import Presentation
from pptx.util import Inches
import os
import time
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def create_report(image_path, result, filename):
    # Create a PowerPoint presentation object
    prs = Presentation()

    # Add title slide
    slide_layout = prs.slide_layouts[0]  # 0 is the title slide layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = "Plastic Detection Report"
    subtitle.text = f"Analysis for {filename}"

    # Add slide for image
    slide_layout = prs.slide_layouts[5]  # 5 is a blank slide layout
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.add_picture(image_path, Inches(0.5), Inches(1), height=Inches(4.5))

    # Add slide for analysis result
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # 1 is the Title and Content layout
    title = slide.shapes.title
    title.text = "Analysis Result"

    content = slide.shapes.placeholders[1]
    content.text = result

    # Ensure the reports folder exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Create a unique filename for the report
    timestamp = int(time.time())
    report_filename = f"{timestamp}_{filename.split('.')[0]}_report.pptx"

    # Save the presentation to a file in the 'reports' folder
    report_path = os.path.join('reports', report_filename)
    prs.save(report_path)

    return report_path


def create_report_2(image_path, result, filename):
    # Create a PowerPoint presentation object
    prs = Presentation()

    # Add title slide
    slide_layout = prs.slide_layouts[0]  # 0 is the title slide layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Plastic Detection Report"
    subtitle.text = f"Analysis for {filename}"

    # Add slide for image
    slide_layout = prs.slide_layouts[5]  # 5 is a blank slide layout
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.add_picture(image_path, Inches(0.5), Inches(1), height=Inches(4.5))

    # Add slide for analysis description
    slide_layout = prs.slide_layouts[1]  # Title and Content layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Analysis Overview"
    content = slide.shapes.placeholders[1]
    content.text = result["description"]

    # Add slides for each object detected
    for obj in result['objects']:
        slide_layout = prs.slide_layouts[1]  # Title and Content layout
        slide = prs.slides.add_slide(slide_layout)
        title = slide.shapes.title
        title.text = f"Object: {obj['type']}"

        content = slide.shapes.placeholders[1]
        content.text = (
            f"Shape (Aspect Ratio): {obj['shape']}\n"
            f"Color: {obj['color']}\n"
            f"Confidence: {obj['confidence']:.2f}"
        )

    # Ensure the reports folder exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Create a unique filename for the report
    timestamp = int(time.time())
    report_filename = f"{timestamp}_{filename.split('.')[0]}_report.pptx"

    # Save the presentation to a file in the 'reports' folder
    report_path = os.path.join('reports', report_filename)
    prs.save(report_path)

    return report_path